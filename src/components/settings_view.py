import flet as ft
from config import config

class SettingsView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 30
        self.padding = ft.padding.symmetric(horizontal=40, vertical=30)
        self.scroll = ft.ScrollMode.AUTO
        
        # 定义输入控件
        self.api_url = ft.TextField(
            label="OpenAI API URL",
            value=config.openapiurl,
            border_radius=12,
            on_change=self.save_settings,
        )
        self.api_key = ft.TextField(
            label="API Key",
            value=config.apikey,
            password=True,
            can_reveal_password=True,
            border_radius=12,
            on_change=self.save_settings,
        )
        self.model_name = ft.TextField(
            label="模型名称",
            value=config.modelname,
            border_radius=12,
            on_change=self.save_settings,
            hint_text="例如: gpt-3.5-turbo",
        )

        # 个人资料控件
        self.username_field = ft.TextField(
            label="用户名",
            value=config.username,
            border_radius=12,
            on_change=self.save_settings,
        )

        # 界面设置控件
        self.dark_mode_switch = ft.Switch(
            label="深色模式",
            value=config.dark_mode,
            on_change=self.save_settings,
        )
        self.show_avatar_switch = ft.Switch(
            label="显示头像",
            value=config.show_avatar,
            on_change=self.save_settings,
        )

        self.test_api_button = ft.ElevatedButton(
            content=ft.Text("测试 API", color=ft.Colors.WHITE),
            on_click=self.test_api,
            bgcolor=ft.Colors.BLUE_GREY_700,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
        )
        
        self.controls = [
            ft.Text("设置", size=32, weight="bold", color="#1f1f1f"),
            
            # AI 配置部分
            self.create_section(
                "AI 服务配置",
                [
                    self.api_url,
                    self.api_key,
                    self.model_name,
                    self.test_api_button,
                ]
            ),
            
            # 个人资料部分
            self.create_section(
                "个人资料",
                [
                    self.username_field,
                ]
            ),
            
            # 界面设置
            self.create_section(
                "界面定制",
                [
                    self.dark_mode_switch,
                    self.show_avatar_switch,
                ]
            ),
            
            # 关于
            self.create_section(
                "关于",
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED),
                        title=ft.Text("版本"),
                        subtitle=ft.Text("NewFamily v0.1.0"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.DESCRIPTION_OUTLINED),
                        title=ft.Text("开源许可"),
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

    def test_api(self, e):
        from config import testapi
        # 禁用按钮，显示正在测试
        self.test_api_button.disabled = True

        self.test_api_button.content = ft.Text("正在测试...", color=ft.Colors.WHITE)
        self.update()
        
        success = testapi(self.api_url.value, self.api_key.value, self.model_name.value)
        
        # 恢复按钮
        self.test_api_button.disabled = False
        self.test_api_button.content = ft.Text("测试 API", color=ft.Colors.WHITE)
        
        # 显示结果
        if success:
            color = ft.Colors.GREEN
            message = "API 连接成功！"
        else:
            color = ft.Colors.RED
            message = "API 连接失败，请检查配置。"
            
        # 使用 SnackBar 显示结果
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            action="知道了",
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
        config.save()
