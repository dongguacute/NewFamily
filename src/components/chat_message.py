import flet as ft
from config import config

class ChatMessage(ft.Row):
    def __init__(self, text, user, is_me=False):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.spacing = 12
        
        controls = []
        
        if config.show_avatar:
            avatar = ft.Container(
                content=ft.Text(user[0].upper() if user else "?", color="#FFFFFF", size=14, weight="bold"),
                width=32,
                height=32,
                bgcolor="#1a73e8" if is_me else "#5f6368",
                border_radius=16,
                alignment=ft.alignment.Alignment(0, 0),
            )
            controls.append(avatar)
            
        bubble = ft.Container(
            content=ft.Text(
                text, 
                size=16,
                color="#1f1f1f",
            ),
            bgcolor="#D3E3FD" if is_me else "#F0F4F9",
            padding=ft.padding.only(left=20, right=20, top=12, bottom=12),
            border_radius=ft.border_radius.only(
                top_left=24,
                top_right=24,
                bottom_left=4 if is_me else 24,
                bottom_right=24 if is_me else 4,
            ),
        )
        
        self.controls = [
            ft.Column(
                [
                    ft.Row(
                        [
                            *controls,
                            ft.Text(user, size=13, weight="w500", color="#5f6368"),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.END if is_me else ft.MainAxisAlignment.START,
                    ),
                    bubble,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.END if is_me else ft.CrossAxisAlignment.START,
                spacing=4,
            )
        ]
        
        self.alignment = ft.MainAxisAlignment.END if is_me else ft.MainAxisAlignment.START
