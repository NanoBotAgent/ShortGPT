import time
import gradio as gr

from gui.ui_tab_short_automation import ShortAutomationUI
from gui.ui_tab_video_automation import VideoAutomationUI
from gui.ui_tab_video_translation import VideoTranslationUI
from gui.ui_texts import t


class GradioContentAutomationUI:
    def __init__(self, shortGPTUI):
        self.shortGPTUI = shortGPTUI
        self.content_automation_ui = None

    def create_ui(self):
        with gr.Tab(t("content_automation_tab")) as self.content_automation_ui:
            gr.Markdown(t("content_automation_title"))
            gr.Markdown(t("content_automation_subtitle"))
            choices = [
                t("content_choice_shorts"),
                t("content_choice_video"),
                t("content_choice_translation"),
            ]
            choice = gr.Radio(choices, label=t("content_choice_label"))
            video_automation_ui = VideoAutomationUI(self.shortGPTUI).create_ui()
            short_automation_ui = ShortAutomationUI(self.shortGPTUI).create_ui()
            video_translation_ui = VideoTranslationUI(self.shortGPTUI).create_ui()

            def onChange(x):
                showShorts = x == choices[0]
                showVideo = x == choices[1]
                showTranslation = x == choices[2]
                return gr.update(visible=showShorts), gr.update(visible=showVideo), gr.update(visible=showTranslation)

            choice.change(onChange, [choice], [short_automation_ui, video_automation_ui, video_translation_ui])
        return self.content_automation_ui
