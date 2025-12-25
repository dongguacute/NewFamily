import flet as ft
from .chat_message import ChatMessage
from config import config

class ChatBox(ft.Column):
    def __init__(self):
        super().__init__()
        self.messages = ft.ListView(
            expand=True,
            spacing=20,
            auto_scroll=True,
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )
        self.new_message = ft.TextField(
            hint_text="问问 NewFamily...",
            expand=True,
            on_submit=self.send_click,
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            text_size=16,
            cursor_color="#1a73e8",
        )
        
        input_container = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE_ROUNDED, icon_color="#444746"),
                    self.new_message,
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        tooltip="发送",
                        on_click=self.send_click,
                        icon_color="#1a73e8",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#F0F4F9",
            border_radius=32,
            padding=ft.padding.symmetric(horizontal=8),
            margin=ft.padding.only(left=40, right=40, bottom=20),
        )

        self.controls = [
            ft.Container(
                content=self.messages,
                expand=True,
            ),
            input_container,
        ]
        self.expand = True
        self.spacing = 0

    def send_click(self, e):
        if self.new_message.value:
            self.messages.controls.append(
                ChatMessage(self.new_message.value, config.username, is_me=True)
            )
            self.new_message.value = ""
            self.update()
            # 模拟自动回复
            self.messages.controls.append(
                ChatMessage("收到你的消息了！", "NewFamily", is_me=False)
            )
            self.update()
