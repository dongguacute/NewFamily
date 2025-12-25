import flet as ft
from config import config
from i18n import t

class SettingsView(ft.Column):
    def __init__(self, on_language_change=None):
        super().__init__()
        self.on_language_change = on_language_change
        
        self.expand = True
        self.spacing = 30
        self.padding = ft.padding.symmetric(horizontal=40, vertical=30)
        self.scroll = ft.ScrollMode.AUTO
        
        # 定义输入控件
        self.api_url = ft.TextField(
            label=t("api_url_label"),
            value=config.openapiurl,
            border_radius=12,
        )
        self.api_url.on_change = self.save_settings

        self.api_key = ft.TextField(
            label=t("api_key_label"),
            value=config.apikey,
            password=True,
            can_reveal_password=True,
            border_radius=12,
        )
        self.api_key.on_change = self.save_settings

        self.model_name = ft.TextField(
            label=t("model_name_label"),
            value=config.modelname,
            border_radius=12,
            hint_text=t("model_name_hint"),
        )
        self.model_name.on_change = self.save_settings

        # 个人资料控件
        self.username_field = ft.TextField(
            label=t("username_label"),
            value=config.username,
            border_radius=12,
        )
        self.username_field.on_change = self.save_settings

        # 界面设置控件
        self.dark_mode_switch = ft.Switch(
            label=t("dark_mode_label"),
            value=config.dark_mode,
        )
        self.dark_mode_switch.on_change = self.save_settings

        self.show_avatar_switch = ft.Switch(
            label=t("show_avatar_label"),
            value=config.show_avatar,
        )
        self.show_avatar_switch.on_change = self.save_settings
        
        # 语言设置
        self.language_dropdown = ft.Dropdown(
            label=t("language_label"),
            value=config.language,
            options=[
                ft.dropdown.Option("zh", t("language_zh")),
                ft.dropdown.Option("en", t("language_en")),
            ],
            border_radius=12,
        )
        self.language_dropdown.on_change = self.change_language

        self.test_api_button = ft.ElevatedButton(
            content=ft.Text(t("test_api_button"), color=ft.Colors.WHITE),
            on_click=self.test_api,
            bgcolor=ft.Colors.BLUE_GREY_700,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
        )
        
        self.controls = [
            ft.Text(t("settings_title"), size=32, weight="bold"),
            
            # AI 配置部分
            self.create_section(
                t("ai_config_section"),
                [
                    self.api_url,
                    self.api_key,
                    self.model_name,
                    self.test_api_button,
                ]
            ),
            
            # 个人资料部分
            self.create_section(
                t("profile_section"),
                [
                    self.username_field,
                ]
            ),
            
            # 界面设置
            self.create_section(
                t("ui_customization_section"),
                [
                    self.language_dropdown,
                    self.dark_mode_switch,
                    self.show_avatar_switch,
                ]
            ),
            
            # 关于
            self.create_section(
                t("about_section"),
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED),
                        title=ft.Text(t("version_label")),
                        subtitle=ft.Text("NewFamily v0.1.0"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.DESCRIPTION_OUTLINED),
                        title=ft.Text(t("license_label")),
                        on_click=lambda _: print("License"),
                    ),
                ]
            ),
        ]

    def create_section(self, title, controls):
        return ft.Column(
            [
                ft.Text(title, size=16, weight="bold", color="#1a73e8"),
                ft.Container(
                    content=ft.Column(controls, spacing=5),
                    bgcolor="#F0F4F9",
                    border_radius=16,
                    padding=ft.padding.all(10),
                ),
            ],
            spacing=10,
        )

    def change_language(self, e):
        new_lang = self.language_dropdown.value
        if new_lang:
            config.language = new_lang
            config.save()
            if self.on_language_change:
                self.on_language_change()
            else:
                # Fallback if no callback provided
                self.controls.clear()
                self.__init__(on_language_change=self.on_language_change)
                self.update()

    def test_api(self, e):
        from config import testapi
        # 禁用按钮，显示正在测试
        self.test_api_button.disabled = True

        self.test_api_button.content = ft.Text(t("testing_api"), color=ft.Colors.WHITE)
        self.update()
        
        success = testapi(self.api_url.value, self.api_key.value, self.model_name.value)
        
        # 恢复按钮
        self.test_api_button.disabled = False
        self.test_api_button.content = ft.Text(t("test_api_button"), color=ft.Colors.WHITE)
        
        # 显示结果
        if success:
            color = ft.Colors.GREEN
            message = t("api_success")
        else:
            color = ft.Colors.RED
            message = t("api_failure")
            
        # 使用 SnackBar 显示结果
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            action=t("ok"),
        )
        self.page.snack_bar.open = True
        self.page.update()

    def save_settings(self, e):
        config.openapiurl = self.api_url.value
        config.apikey = self.api_key.value
        config.modelname = self.model_name.value
        config.username = self.username_field.value
        config.dark_mode = self.dark_mode_switch.value
        config.show_avatar = self.show_avatar_switch.value
        # DO NOT update config.language here, it should only be updated in change_language
        config.save()

