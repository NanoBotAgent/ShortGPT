import locale
import os
from typing import Any

from shortGPT.database.db_document import TinyMongoDocument


SUPPORTED_UI_LANGUAGES = ["English", "简体中文"]
LANGUAGE_LABEL_TO_CODE = {
    "English": "en",
    "简体中文": "zh",
}
LANGUAGE_CODE_TO_LABEL = {value: key for key, value in LANGUAGE_LABEL_TO_CODE.items()}
DEFAULT_UI_LANGUAGE = "简体中文"

_ui_language_doc = TinyMongoDocument("ui_db", "settings", "ui_settings", create=True)


TRANSLATIONS = {
    "en": {
        "content_automation_tab": "Content Automation",
        "content_automation_title": "# Automate your video creation",
        "content_automation_subtitle": "Choose a workflow to generate shorts, create full videos, or translate existing videos.",
        "content_choice_label": "Workflow",
        "content_choice_shorts": "Shorts Automation",
        "content_choice_video": "Video Automation",
        "content_choice_translation": "Video Translation",
        "config_tab": "Configuration",
        "ui_language": "UI Language",
        "language_saved": "Language saved. Refresh the page if some texts did not update immediately.",
        "config_saved_notice": "Configuration saved successfully.",
        "show": "Show",
        "hide": "Hide",
        "save": "Save",
        "keys_saved": "Saved",
        "openai_api_key": "OpenAI API Key",
        "openai_base_url": "OpenAI API Base URL",
        "eleven_api_key": "ElevenLabs API Key",
        "characters_remaining": "Characters Remaining",
        "pexels_key": "Pexels API Key",
        "gemini_api_key": "Gemini API Key",
        "header_join_discord": "Join Discord",
        "header_star_github": "Star on GitHub",
        "error_title": "Error: {error_message}",
        "error_traceback": "Traceback: {stack_trace}",
        "error_help": "If the issue persists, please ask for help in the community.",
        "error_help_button": "Get Help",
        "browser_not_support_video": "Your browser does not support the video tag.",
        "download_video": "Download Video",
        "free_edge_tts": "Free EdgeTTS",
        "eleven_tts": "ElevenLabs",
        "choose_background_video": "Choose background video",
        "choose_background_music": "Choose background music",
        "eleven_voice": "ElevenLabs Voice",
        "youtube_link": "YouTube Link",
        "video_file": "Video File",
        "input_video": "Input Video",
        "youtube_link_input": "YouTube URL",
        "tts_engine": "Text-to-Speech Engine",
        "language": "Language",
        "caption_video": "Add captions",
        "translate_video": "Translate Video",
        "translating_video": "Translating video {index}/{total} - {message}",
        "rendering_progress": "Rendering... {current}",
        "error_invalid_youtube_url": "Invalid YouTube URL. Please provide a valid URL.",
        "error_invalid_video_file": "Invalid video file. Please upload a valid video file.",
        "error_invalid_video_extension": "Invalid video extension. Supported extensions: {extensions}",
        "error_select_target_languages": "Please select at least one target language.",
        "short_num": "Number of shorts",
        "short_type": "Short type",
        "short_type_reddit": "Reddit Story Shorts",
        "short_type_historical": "Historical Facts Shorts",
        "short_type_scientific": "Scientific Facts Shorts",
        "short_type_custom": "Custom Facts Shorts",
        "facts_subject": "Facts subject (example: Football facts)",
        "use_images": "Use images",
        "num_images": "Number of images per short",
        "add_watermark": "Add watermark",
        "watermark": "Watermark (your channel name)",
        "create_shorts": "Create Shorts",
        "making_short": "Making short {current}/{total} - {message}",
        "error_facts_subject_required": "Please write down your facts short subject.",
        "error_select_background_video": "Please select at least one background video.",
        "error_select_background_music": "Please select at least one background music.",
        "error_watermark_alnum": "Watermark should only contain letters and numbers.",
        "error_watermark_max": "Watermark should not exceed 25 characters.",
        "error_watermark_min": "Watermark should be at least 3 characters long.",
        "error_missing_llm_key": "GEMINI or OPENAI API key is missing. Please go to the configuration tab and enter the API key.",
        "error_missing_eleven_key": "ELEVENLABS_API_KEY is missing. Please go to the configuration tab and enter the API key.",
        "error_invalid_short_type": "Short type does not have a valid engine: {short_type}",
        "asset_library_tab": "Asset Library",
        "asset_add_local_or_youtube": "➕ Add your own local assets or from YouTube",
        "asset_remote": "Add YouTube video / audio",
        "asset_local": "Add local video / audio / image",
        "name_required": "Name (required)",
        "type": "Type",
        "url_youtube": "URL (https://youtube.com/xyz)",
        "add": "Add",
        "preview": "Preview",
        "delete": "Delete",
        "background_video": "Background Video",
        "background_music": "Background Music",
        "image": "Image",
        "invalid_asset_name": "Invalid asset name. Please provide a valid name using only letters, numbers, spaces, underscores, or hyphens.",
        "asset_exists": "An asset already exists with this name. Please choose a different name.",
        "file_not_exist": "The file does not exist at the given path.",
        "unsupported_file_type": "Unsupported file type",
        "restart": "Restart",
        "chat_welcome": "🤖 Welcome to ShortGPT! 🚀 I'm a Python framework that helps automate video creation.\nLet's get started! 🎥🎬\n\nDo you want your video to be landscape or vertical? (landscape / vertical)",
        "chat_missing_llm_key": "Your Gemini or OpenAI key is missing. Please go to the configuration tab and enter the API key.",
        "chat_missing_pexels_key": "Your Pexels API key is missing. Please go to the configuration tab and enter the API key.",
        "chat_ask_voice_module": "Which voice module do you want to use? Type 'ElevenLabs' for higher quality or 'EdgeTTS' for a free voice.",
        "chat_invalid_voice_module": "Invalid voice module. Please type 'ElevenLabs' or 'EdgeTTS'.",
        "chat_missing_eleven_key": "Your ELEVENLABS_API_KEY is missing. Please go to the configuration tab and enter the API key.",
        "chat_ask_language": "What language should be used in the video? Choose from: {languages}",
        "chat_ask_description": "Great! Please describe the subject of your video in detail, and I will generate a script.",
        "chat_generated_script": "📝 Here is your generated script:\n\n--------------\n{script}\n\nAre you satisfied and ready to create the video? Reply with YES or NO.",
        "chat_video_making": "Your video is being created now! 🎬",
        "chat_video_completed": "Your video is complete! 🎬 Scroll down to open its file location.",
        "chat_video_error": "We encountered an error while making this video ❌",
        "chat_ask_correction": "Tell me what you want to change in the script.",
        "chat_corrected_script": "📝 Here is your corrected script:\n\n--------------\n{script}\n\nAre you satisfied and ready to create the video? Reply with YES or NO.",
        "chat_creating_video": "Creating video - {message}",
        "chat_yes_values": "yes,y,ok,okay,sure,continue,go",
    },
    "zh": {
        "content_automation_tab": "内容自动化",
        "content_automation_title": "# 自动化创建视频",
        "content_automation_subtitle": "选择工作流来生成短视频、创建完整视频，或翻译已有视频。",
        "content_choice_label": "工作流",
        "content_choice_shorts": "短视频自动化",
        "content_choice_video": "视频自动化",
        "content_choice_translation": "视频翻译",
        "config_tab": "配置",
        "ui_language": "界面语言",
        "language_saved": "语言已保存。如果有少量文本未立即更新，请刷新页面。",
        "config_saved_notice": "配置已成功保存。",
        "show": "显示",
        "hide": "隐藏",
        "save": "保存",
        "keys_saved": "已保存",
        "openai_api_key": "OpenAI API Key",
        "openai_base_url": "OpenAI API 地址",
        "eleven_api_key": "ElevenLabs API Key",
        "characters_remaining": "剩余字符数",
        "pexels_key": "Pexels API Key",
        "gemini_api_key": "Gemini API Key",
        "header_join_discord": "加入 Discord",
        "header_star_github": "GitHub 点星",
        "error_title": "错误：{error_message}",
        "error_traceback": "堆栈：{stack_trace}",
        "error_help": "如果问题持续存在，请到社区寻求帮助。",
        "error_help_button": "获取帮助",
        "browser_not_support_video": "你的浏览器不支持 video 标签。",
        "download_video": "下载视频",
        "free_edge_tts": "免费 EdgeTTS",
        "eleven_tts": "ElevenLabs",
        "choose_background_video": "选择背景视频",
        "choose_background_music": "选择背景音乐",
        "eleven_voice": "ElevenLabs 声音",
        "youtube_link": "YouTube 链接",
        "video_file": "视频文件",
        "input_video": "输入视频",
        "youtube_link_input": "YouTube 地址",
        "tts_engine": "文本转语音引擎",
        "language": "语言",
        "caption_video": "添加字幕",
        "translate_video": "翻译视频",
        "translating_video": "正在翻译视频 {index}/{total} - {message}",
        "rendering_progress": "渲染中... {current}",
        "error_invalid_youtube_url": "无效的 YouTube 链接，请提供正确地址。",
        "error_invalid_video_file": "无效的视频文件，请上传正确的视频文件。",
        "error_invalid_video_extension": "无效的视频扩展名，支持：{extensions}",
        "error_select_target_languages": "请至少选择一种目标语言。",
        "short_num": "短视频数量",
        "short_type": "短视频类型",
        "short_type_reddit": "Reddit 故事短视频",
        "short_type_historical": "历史事实短视频",
        "short_type_scientific": "科学事实短视频",
        "short_type_custom": "自定义事实短视频",
        "facts_subject": "事实主题（例如：足球冷知识）",
        "use_images": "使用图片",
        "num_images": "每个短视频的图片数量",
        "add_watermark": "添加水印",
        "watermark": "水印（你的频道名称）",
        "create_shorts": "创建短视频",
        "making_short": "正在制作短视频 {current}/{total} - {message}",
        "error_facts_subject_required": "请填写事实短视频主题。",
        "error_select_background_video": "请至少选择一个背景视频。",
        "error_select_background_music": "请至少选择一个背景音乐。",
        "error_watermark_alnum": "水印只能包含字母和数字。",
        "error_watermark_max": "水印长度不能超过 25 个字符。",
        "error_watermark_min": "水印长度不能少于 3 个字符。",
        "error_missing_llm_key": "缺少 GEMINI 或 OPENAI API Key，请到配置页填写。",
        "error_missing_eleven_key": "缺少 ELEVENLABS_API_KEY，请到配置页填写。",
        "error_invalid_short_type": "短视频类型没有对应的有效引擎：{short_type}",
        "asset_library_tab": "素材库",
        "asset_add_local_or_youtube": "➕ 添加本地素材或 YouTube 素材",
        "asset_remote": "添加 YouTube 视频 / 音频",
        "asset_local": "添加本地视频 / 音频 / 图片",
        "name_required": "名称（必填）",
        "type": "类型",
        "url_youtube": "地址（https://youtube.com/xyz）",
        "add": "添加",
        "preview": "预览",
        "delete": "删除",
        "background_video": "背景视频",
        "background_music": "背景音乐",
        "image": "图片",
        "invalid_asset_name": "素材名称无效。请只使用字母、数字、空格、下划线或连字符。",
        "asset_exists": "已存在同名素材，请换一个名称。",
        "file_not_exist": "给定路径下的文件不存在。",
        "unsupported_file_type": "不支持的文件类型",
        "restart": "重新开始",
        "chat_welcome": "🤖 欢迎使用 ShortGPT！🚀 我可以帮助你自动化创建视频。\n现在开始吧！🎥🎬\n\n你想要横屏还是竖屏视频？（landscape / vertical，或输入 横屏 / 竖屏）",
        "chat_missing_llm_key": "缺少 Gemini 或 OpenAI Key，请到配置页填写。",
        "chat_missing_pexels_key": "缺少 Pexels API Key，请到配置页填写。",
        "chat_ask_voice_module": "你想使用哪种配音模块？输入 'ElevenLabs' 可获得更高质量，输入 'EdgeTTS' 可使用免费语音。",
        "chat_invalid_voice_module": "无效的配音模块，请输入 'ElevenLabs' 或 'EdgeTTS'。",
        "chat_missing_eleven_key": "缺少 ELEVENLABS_API_KEY，请到配置页填写。",
        "chat_ask_language": "视频要使用什么语言？可选：{languages}",
        "chat_ask_description": "很好！请详细描述你想制作的视频主题，我会为你生成脚本。",
        "chat_generated_script": "📝 这是为你生成的脚本：\n\n--------------\n{script}\n\n如果满意并准备开始生成视频，请回复 YES / NO，也可以回复 是 / 否。",
        "chat_video_making": "正在为你生成视频！🎬",
        "chat_video_completed": "视频已生成完成！🎬 向下滚动可打开文件所在位置。",
        "chat_video_error": "生成视频时遇到错误 ❌",
        "chat_ask_correction": "请告诉我你希望脚本做哪些修改。",
        "chat_corrected_script": "📝 这是修正后的脚本：\n\n--------------\n{script}\n\n如果满意并准备开始生成视频，请回复 YES / NO，也可以回复 是 / 否。",
        "chat_creating_video": "正在创建视频 - {message}",
        "chat_yes_values": "yes,y,ok,okay,sure,continue,go,是,好,可以,继续,确认",
    },
}


def _normalize_language_code(code: str | None) -> str:
    if not code:
        return LANGUAGE_LABEL_TO_CODE[DEFAULT_UI_LANGUAGE]
    code = code.lower()
    if code.startswith("zh"):
        return "zh"
    return "en"


def _detect_language_label() -> str:
    env_lang = os.environ.get("SHORTGPT_UI_LANGUAGE")
    if env_lang:
        if env_lang in LANGUAGE_LABEL_TO_CODE:
            return env_lang
        return LANGUAGE_CODE_TO_LABEL.get(_normalize_language_code(env_lang), DEFAULT_UI_LANGUAGE)
    try:
        saved = _ui_language_doc._get("language")
        if saved in SUPPORTED_UI_LANGUAGES:
            return saved
    except Exception:
        pass
    try:
        system_locale = locale.getdefaultlocale()[0]
    except Exception:
        system_locale = None
    return LANGUAGE_CODE_TO_LABEL.get(_normalize_language_code(system_locale), DEFAULT_UI_LANGUAGE)


def get_ui_language() -> str:
    language = _detect_language_label()
    if language not in SUPPORTED_UI_LANGUAGES:
        return DEFAULT_UI_LANGUAGE
    return language


def get_ui_language_code() -> str:
    return LANGUAGE_LABEL_TO_CODE.get(get_ui_language(), "zh")


def set_ui_language(language: str) -> str:
    if language not in SUPPORTED_UI_LANGUAGES:
        language = DEFAULT_UI_LANGUAGE
    _ui_language_doc._save({"language": language})
    return language


def t(key: str, **kwargs: Any) -> str:
    code = get_ui_language_code()
    text = TRANSLATIONS.get(code, {}).get(key) or TRANSLATIONS["en"].get(key) or key
    if kwargs:
        return text.format(**kwargs)
    return text
