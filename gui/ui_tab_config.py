import time

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_texts import SUPPORTED_UI_LANGUAGES, get_ui_language, set_ui_language, t
from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager


class ConfigUI(AbstractComponentUI):
    def __init__(self):
        self.api_key_manager = ApiKeyManager()
        eleven_key = self.api_key_manager.get_api_key('ELEVENLABS_API_KEY')
        self.eleven_labs_api = ElevenLabsAPI(eleven_key) if eleven_key else None

    def _masked_value(self, value):
        return "●●●●●●●●" if value else ""

    def _normalize_secret_input(self, value, key_name):
        value = (value or "").strip()
        saved_value = self.api_key_manager.get_api_key(key_name).strip()
        if value == self._masked_value(saved_value):
            return saved_value
        return value

    def toggle_secret(self, button_text, key_name, current_value):
        saved_value = self.api_key_manager.get_api_key(key_name).strip()
        current_value = (current_value or "").strip()

        if button_text == t("show"):
            if current_value and current_value != self._masked_value(saved_value):
                reveal_value = current_value
            else:
                reveal_value = saved_value
            return gr.update(value=reveal_value, type="text"), gr.update(value=t("hide"))

        if current_value and current_value != saved_value:
            masked_value = self._masked_value(current_value)
        else:
            masked_value = self._masked_value(saved_value)
        return gr.update(value=masked_value, type="text"), gr.update(value=t("show"))

    def verify_eleven_key(self, eleven_key, remaining_chars):
        normalized_eleven_key = self._normalize_secret_input(eleven_key, 'ELEVENLABS_API_KEY')
        if normalized_eleven_key and self.api_key_manager.get_api_key('ELEVENLABS_API_KEY') != normalized_eleven_key:
            try:
                self.eleven_labs_api = ElevenLabsAPI(normalized_eleven_key)
                return self.eleven_labs_api.get_remaining_characters()
            except Exception as e:
                raise gr.Error(e.args[0])
        return remaining_chars

    def save_keys(self, openai_key, openai_base_url, eleven_key, pexels_key, gemini_key):
        openai_key = self._normalize_secret_input(openai_key, "OPENAI_API_KEY")
        openai_base_url = (openai_base_url or "").strip()
        eleven_key = self._normalize_secret_input(eleven_key, "ELEVENLABS_API_KEY")
        pexels_key = self._normalize_secret_input(pexels_key, "PEXELS_API_KEY")
        gemini_key = self._normalize_secret_input(gemini_key, "GEMINI_API_KEY")

        if self.api_key_manager.get_api_key("OPENAI_API_KEY") != openai_key:
            self.api_key_manager.set_api_key("OPENAI_API_KEY", openai_key)
        if self.api_key_manager.get_api_key("OPENAI_BASE_URL") != openai_base_url:
            self.api_key_manager.set_api_key("OPENAI_BASE_URL", openai_base_url)
        if self.api_key_manager.get_api_key("PEXELS_API_KEY") != pexels_key:
            self.api_key_manager.set_api_key("PEXELS_API_KEY", pexels_key)
        if self.api_key_manager.get_api_key('ELEVENLABS_API_KEY') != eleven_key:
            self.api_key_manager.set_api_key("ELEVENLABS_API_KEY", eleven_key)
            self.eleven_labs_api = ElevenLabsAPI(eleven_key) if eleven_key else None
        if self.api_key_manager.get_api_key("GEMINI_API_KEY") != gemini_key:
            self.api_key_manager.set_api_key("GEMINI_API_KEY", gemini_key)

        new_eleven_voices = AssetComponentsUtils.getElevenlabsVoices() if eleven_key else gr.update()
        eleven_remaining = self.get_eleven_remaining()
        save_notice = t("config_saved_notice")
        return (
            gr.update(value=self._masked_value(openai_key), type="text"),
            gr.update(value=openai_base_url),
            gr.update(value=self._masked_value(eleven_key), type="text"),
            gr.update(value=self._masked_value(pexels_key), type="text"),
            gr.update(value=self._masked_value(gemini_key), type="text"),
            gr.update(value=eleven_remaining),
            gr.update(value=save_notice, visible=True),
            new_eleven_voices,
            new_eleven_voices,
        )

    def load_config_values(self):
        openai_value = self.api_key_manager.get_api_key("OPENAI_API_KEY")
        openai_base_url = self.api_key_manager.get_api_key("OPENAI_BASE_URL")
        eleven_value = self.api_key_manager.get_api_key("ELEVENLABS_API_KEY")
        pexels_value = self.api_key_manager.get_api_key("PEXELS_API_KEY")
        gemini_value = self.api_key_manager.get_api_key("GEMINI_API_KEY")

        return (
            gr.update(value=self._masked_value(openai_value), type="text"),
            gr.update(value=openai_base_url),
            gr.update(value=self._masked_value(eleven_value), type="text"),
            gr.update(value=self.get_eleven_remaining()),
            gr.update(value=self._masked_value(pexels_value), type="text"),
            gr.update(value=self._masked_value(gemini_value), type="text"),
            gr.update(value=t("show")),
            gr.update(value=t("show")),
            gr.update(value=t("show")),
            gr.update(value=t("show")),
            gr.update(visible=False),
        )

    def get_eleven_remaining(self):
        if self.eleven_labs_api:
            try:
                return self.eleven_labs_api.get_remaining_characters()
            except Exception as e:
                return e.args[0]
        return ""

    def save_ui_language(self, language):
        saved_language = set_ui_language(language)
        return gr.update(value=saved_language), gr.update(value=t("language_saved"), visible=True)

    def back_to_normal(self):
        time.sleep(3)
        return gr.update(value=t("save"))

    def hide_notice(self):
        time.sleep(3)
        return gr.update(visible=False)

    def create_ui(self):
        with gr.Tab(t("config_tab")) as config_ui:
            with gr.Row():
                with gr.Column():
                    ui_language = gr.Dropdown(choices=SUPPORTED_UI_LANGUAGES, value=get_ui_language(), label=t("ui_language"), interactive=True)
                    language_notice = gr.Textbox(value="", visible=False, interactive=False, show_label=False)
                    save_notice = gr.Textbox(value="", visible=False, interactive=False, show_label=False)
                    ui_language.change(self.save_ui_language, [ui_language], [ui_language, language_notice])
                    ui_language.change(self.hide_notice, [], [language_notice])
                    with gr.Row():
                        openai_value = self.api_key_manager.get_api_key("OPENAI_API_KEY")
                        openai_textbox = gr.Textbox(value=self._masked_value(openai_value), label=t("openai_api_key"), show_label=True, interactive=True, show_copy_button=True, type="text", scale=40)
                        show_openai_key = gr.Button(t("show"), size="sm", scale=1)
                        show_openai_key.click(self.toggle_secret, [show_openai_key, gr.State("OPENAI_API_KEY"), openai_textbox], [openai_textbox, show_openai_key])
                    with gr.Row():
                        openai_base_url_textbox = gr.Textbox(value=self.api_key_manager.get_api_key("OPENAI_BASE_URL"), label=t("openai_base_url"), show_label=True, interactive=True, show_copy_button=True, type="text", scale=40)
                    with gr.Row():
                        eleven_value = self.api_key_manager.get_api_key("ELEVENLABS_API_KEY")
                        eleven_labs_textbox = gr.Textbox(value=self._masked_value(eleven_value), label=t("eleven_api_key"), show_label=True, interactive=True, show_copy_button=True, type="text", scale=40)
                        eleven_characters_remaining = gr.Textbox(value=self.get_eleven_remaining(), label=t("characters_remaining"), show_label=True, interactive=False, type="text", scale=40)
                        show_eleven_key = gr.Button(t("show"), size="sm", scale=1)
                        show_eleven_key.click(self.toggle_secret, [show_eleven_key, gr.State("ELEVENLABS_API_KEY"), eleven_labs_textbox], [eleven_labs_textbox, show_eleven_key])
                    with gr.Row():
                        pexels_value = self.api_key_manager.get_api_key("PEXELS_API_KEY")
                        pexels_textbox = gr.Textbox(value=self._masked_value(pexels_value), label=t("pexels_key"), show_label=True, interactive=True, show_copy_button=True, type="text", scale=40)
                        show_pexels_key = gr.Button(t("show"), size="sm", scale=1)
                        show_pexels_key.click(self.toggle_secret, [show_pexels_key, gr.State("PEXELS_API_KEY"), pexels_textbox], [pexels_textbox, show_pexels_key])
                    with gr.Row():
                        gemini_value = self.api_key_manager.get_api_key("GEMINI_API_KEY")
                        gemini_textbox = gr.Textbox(value=self._masked_value(gemini_value), label=t("gemini_api_key"), show_label=True, interactive=True, show_copy_button=True, type="text", scale=40)
                        show_gemini_key = gr.Button(t("show"), size="sm", scale=1)
                        show_gemini_key.click(self.toggle_secret, [show_gemini_key, gr.State("GEMINI_API_KEY"), gemini_textbox], [gemini_textbox, show_gemini_key])
                    save_button = gr.Button(t("save"), size="sm", scale=1)
                    save_button.click(self.verify_eleven_key, [eleven_labs_textbox, eleven_characters_remaining], [eleven_characters_remaining]).success(self.save_keys, [openai_textbox, openai_base_url_textbox, eleven_labs_textbox, pexels_textbox, gemini_textbox], [openai_textbox, openai_base_url_textbox, eleven_labs_textbox, pexels_textbox, gemini_textbox, eleven_characters_remaining, save_notice, AssetComponentsUtils.voiceChoice(), AssetComponentsUtils.voiceChoiceTranslation()])
                    save_button.click(lambda: gr.update(value=t("keys_saved")), [], [save_button])
                    save_button.click(self.back_to_normal, [], [save_button])
                    save_button.click(self.hide_notice, [], [save_notice])
                    config_ui.select(
                        self.load_config_values,
                        [],
                        [
                            openai_textbox,
                            openai_base_url_textbox,
                            eleven_labs_textbox,
                            eleven_characters_remaining,
                            pexels_textbox,
                            gemini_textbox,
                            show_openai_key,
                            show_eleven_key,
                            show_pexels_key,
                            show_gemini_key,
                            save_notice,
                        ],
                        show_progress="hidden",
                    )
        return config_ui
