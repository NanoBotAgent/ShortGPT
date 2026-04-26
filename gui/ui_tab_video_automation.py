import os
import traceback
from enum import Enum

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from gui.ui_texts import t
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import EDGE_TTS_VOICENAME_MAPPING, ELEVEN_SUPPORTED_LANGUAGES, Language
from shortGPT.engine.content_video_engine import ContentVideoEngine
from shortGPT.gpt import gpt_chat_video


class Chatstate(Enum):
    ASK_ORIENTATION = 1
    ASK_VOICE_MODULE = 2
    ASK_LANGUAGE = 3
    ASK_DESCRIPTION = 4
    GENERATE_SCRIPT = 5
    ASK_SATISFACTION = 6
    MAKE_VIDEO = 7
    ASK_CORRECTION = 8


class VideoAutomationUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.voice_module = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False
        self.video_automation = None
        self.chatbot = None
        self.msg = None
        self.restart_button = None
        self.video_folder = None
        self.errorHTML = None
        self.outHTML = None

    def is_key_missing(self):
        openai_key = ApiKeyManager.get_api_key("OPENAI_API_KEY")
        gemini_key = ApiKeyManager.get_api_key("GEMINI_API_KEY")
        if not openai_key and not gemini_key:
            return t("chat_missing_llm_key")
        pexels_api_key = ApiKeyManager.get_api_key("PEXELS_API_KEY")
        if not pexels_api_key:
            return t("chat_missing_pexels_key")
        return None

    def generate_script(self, message, language):
        return gpt_chat_video.generateScript(message, language)

    def correct_script(self, script, correction):
        return gpt_chat_video.correctScript(script, correction)

    def make_video(self, script, voice_module, isVertical, progress):
        videoEngine = ContentVideoEngine(voiceModule=voice_module, script=script, isVerticalFormat=isVertical)
        num_steps = videoEngine.get_total_steps()
        progress_counter = 0

        def logger(prog_str):
            progress(progress_counter / num_steps, t("chat_creating_video", message=prog_str))

        videoEngine.set_logger(logger)
        for step_num, step_info in videoEngine.makeContent():
            progress(progress_counter / num_steps, t("chat_creating_video", message=step_info))
            progress_counter += 1
        return videoEngine.get_video_output_path()

    def reset_components(self):
        return gr.update(value=self.initialize_conversation()), gr.update(visible=True), gr.update(value="", visible=False), gr.update(value="", visible=False)

    def chatbot_conversation(self):
        yes_values = {value.strip().lower() for value in t("chat_yes_values").split(",") if value.strip()}

        def respond(message, chat_history, progress=gr.Progress()):
            error_html = ""
            errorVisible = False
            inputVisible = True
            folderVisible = False
            normalized_message = (message or "").strip().lower()
            if self.state == Chatstate.ASK_ORIENTATION:
                errorMessage = self.is_key_missing()
                if errorMessage:
                    bot_message = errorMessage
                else:
                    self.isVertical = any(token in normalized_message for token in ["vertical", "short", "竖", "直屏"])
                    self.state = Chatstate.ASK_VOICE_MODULE
                    bot_message = t("chat_ask_voice_module")
            elif self.state == Chatstate.ASK_VOICE_MODULE:
                if "elevenlabs" in normalized_message:
                    eleven_labs_key = ApiKeyManager.get_api_key("ELEVENLABS_API_KEY")
                    if not eleven_labs_key:
                        bot_message = t("chat_missing_eleven_key")
                        chat_history.append((message, bot_message))
                        yield gr.update(value="", visible=inputVisible), gr.update(value=chat_history), gr.update(value=self.video_html, visible=self.videoVisible), gr.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=True)
                        return
                    self.voice_module = ElevenLabsVoiceModule
                    language_choices = [lang.value for lang in ELEVEN_SUPPORTED_LANGUAGES]
                elif "edgetts" in normalized_message or "edge" in normalized_message:
                    self.voice_module = EdgeTTSVoiceModule
                    language_choices = [lang.value for lang in Language]
                else:
                    bot_message = t("chat_invalid_voice_module")
                    chat_history.append((message, bot_message))
                    yield gr.update(value="", visible=inputVisible), gr.update(value=chat_history), gr.update(value=self.video_html, visible=self.videoVisible), gr.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=True)
                    return
                self.state = Chatstate.ASK_LANGUAGE
                bot_message = t("chat_ask_language", languages=", ".join(language_choices))
            elif self.state == Chatstate.ASK_LANGUAGE:
                self.language = next((lang for lang in Language if lang.value.lower() in normalized_message), None)
                self.language = self.language if self.language else Language.ENGLISH
                if self.voice_module == ElevenLabsVoiceModule:
                    self.voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key("ELEVENLABS_API_KEY"), "Chris", checkElevenCredits=True)
                elif self.voice_module == EdgeTTSVoiceModule:
                    self.voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[self.language]["male"])
                self.state = Chatstate.ASK_DESCRIPTION
                bot_message = t("chat_ask_description")
            elif self.state == Chatstate.ASK_DESCRIPTION:
                self.script = self.generate_script(message, self.language.value)
                self.state = Chatstate.ASK_SATISFACTION
                bot_message = t("chat_generated_script", script=self.script)
            elif self.state == Chatstate.ASK_SATISFACTION:
                if normalized_message in yes_values:
                    self.state = Chatstate.MAKE_VIDEO
                    inputVisible = False
                    yield gr.update(visible=False), gr.update(value=[[None, t("chat_video_making")]]), gr.update(value="", visible=False), gr.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=False)
                    try:
                        video_path = self.make_video(self.script, self.voice_module, self.isVertical, progress=progress)
                        file_name = video_path.split("/")[-1].split("\\")[-1]
                        current_url = self.shortGptUI.share_url + "/" if self.shortGptUI.share else self.shortGptUI.local_url
                        file_url_path = f"{current_url}gradio_api/file={video_path}"
                        self.video_html = GradioComponentsHTML.get_html_video_template(file_url_path, file_name, width=600, height=300)
                        self.videoVisible = True
                        folderVisible = True
                        bot_message = t("chat_video_completed")
                    except Exception as e:
                        traceback_str = "".join(traceback.format_tb(e.__traceback__))
                        error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
                        errorVisible = True
                        error_html = GradioComponentsHTML.get_html_error_template().format(error_message=error_name, stack_trace=traceback_str)
                        bot_message = t("chat_video_error")
                        yield gr.update(visible=False), gr.update(value=[[None, t("chat_video_making")]]), gr.update(value="", visible=False), gr.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=True)
                else:
                    self.state = Chatstate.ASK_CORRECTION
                    bot_message = t("chat_ask_correction")
            elif self.state == Chatstate.ASK_CORRECTION:
                self.script = self.correct_script(self.script, message)
                self.state = Chatstate.ASK_SATISFACTION
                bot_message = t("chat_corrected_script", script=self.script)
            chat_history.append((message, bot_message))
            yield gr.update(value="", visible=inputVisible), gr.update(value=chat_history), gr.update(value=self.video_html, visible=self.videoVisible), gr.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=True)

        return respond

    def initialize_conversation(self):
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False
        return [[None, t("chat_welcome")]]

    def reset_conversation(self):
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False

    def create_ui(self):
        with gr.Row(visible=False) as self.video_automation:
            with gr.Column():
                self.chatbot = gr.Chatbot(self.initialize_conversation, height=365)
                self.msg = gr.Textbox()
                self.restart_button = gr.Button(t("restart"))
                self.video_folder = gr.Button("📁", visible=False)
                self.video_folder.click(lambda _: AssetComponentsUtils.start_file(os.path.abspath("videos/")))
                respond = self.chatbot_conversation()
            self.errorHTML = gr.HTML(visible=False)
            self.outHTML = gr.HTML('<div style="min-height: 80px;"></div>')
            self.restart_button.click(self.reset_components, [], [self.chatbot, self.msg, self.errorHTML, self.outHTML])
            self.restart_button.click(self.reset_conversation, [])
            self.msg.submit(respond, [self.msg, self.chatbot], [self.msg, self.chatbot, self.outHTML, self.errorHTML, self.video_folder, self.restart_button])
        return self.video_automation
