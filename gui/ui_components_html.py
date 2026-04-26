from gui.ui_texts import t


class GradioComponentsHTML:

    @staticmethod
    def get_html_header() -> str:
        return f'''
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px;">
            <h1 style="margin-left: 0px; font-size: 35px;">ShortGPT</h1>
            <div style="flex-grow: 1; text-align: right;">
                <a href="https://discord.gg/bWreuAyRaj" target="_blank" style="text-decoration: none;">
                <button style="margin-right: 10px; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #7289DA; border: none; border-radius: 5px; cursor: pointer;">{t("header_join_discord")}</button>
                </a>
                <a href="https://github.com/RayVentura/ShortGPT" target="_blank" style="text-decoration: none;">
                <button style="padding: 10px 20px; font-size: 16px; color: #fff; background-color: #333; border: none; border-radius: 5px; cursor: pointer;">{t("header_star_github")}</button>
                </a>
            </div>
            </div>
        '''

    @staticmethod
    def get_html_error_template() -> str:
        return f'''
        <div style='text-align: center; background: #ff7f7f; color: #a94442; padding: 20px; border-radius: 5px; margin: 10px;'>
          <h2 style='margin: 0; color: black'>{t("error_title", error_message="{error_message}")}</h2>
          <p style='margin: 10px 0; color: black'>{t("error_traceback", stack_trace="{stack_trace}")}</p>
          <p style='margin: 10px 0; color: black'>{t("error_help")}</p>
          <a href='https://discord.gg/qn2WJaRH' target='_blank' style='background: #a94442; color: #fff; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-decoration: none;'>{t("error_help_button")}</a>
        </div>
        '''

    @staticmethod
    def get_html_video_template(file_url_path, file_name, width="auto", height="auto"):
        html = f'''
            <div style="display: flex; flex-direction: column; align-items: center;">
                <video width="{width}" height="{height}" style="max-height: 100%;" controls>
                    <source src="{file_url_path}" type="video/mp4">
                    {t("browser_not_support_video")}
                </video>
                <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                    <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">{t("download_video")}</button>
                </a>
            </div>
        '''
        return html
