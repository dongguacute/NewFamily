import flet as ft
from i18n import t

class SidebarItem(ft.Container):
    def __init__(self, title, subtitle, icon, on_click, selected=False):
        super().__init__()
        self.padding = ft.padding.symmetric(horizontal=16, vertical=10)
        self.border_radius = 24
        self.on_click = on_click
        self.bgcolor = "#E1EBFD" if selected else ft.Colors.TRANSPARENT
        
        self.content = ft.Row(
            [
                ft.Icon(
                    icon, 
                    color="#1a73e8" if selected else "#444746",
                    size=20
                ),
                ft.Text(
                    title, 
                    weight="w500" if selected else "normal", 
                    size=14,
                    color="#1a73e8" if selected else "#444746",
                    no_wrap=True,
                ),
            ],
            spacing=12,
        )

class Sidebar(ft.Container):
    def __init__(self, on_change_chat):
        super().__init__()
        self.width = 280
        self.padding = ft.padding.all(12)
        self.bgcolor = "#F0F4F9"
        self.on_change_chat = on_change_chat
        self.items_list = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO)
        
        self.chats = [
            {"id": "1", "title": t("chat_assistant"), "icon": ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED},
            {"id": "2", "title": t("chat_planning"), "icon": ft.Icons.AUTO_AWESOME_OUTLINED},
            {"id": "3", "title": t("chat_code_review"), "icon": ft.Icons.CODE_ROUNDED},
        ]
        
        self.settings_item = SidebarItem(
            t("settings_menu"), 
            "", 
            ft.Icons.SETTINGS_OUTLINED, 
            lambda _: self.on_change_chat("settings"),
            selected=False
        )
        
        self.new_chat_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD_ROUNDED, color="#1a73e8"),
                    ft.Text(t("new_chat"), color="#1a73e8", weight="w500"),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=16,
            bgcolor="#D3E3FD",
        )
        self.new_chat_btn.on_click = lambda _: print("New Chat")
        
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.MENU_ROUNDED, color="#444746"),
                            ft.Text("NewFamily", size=18, weight="bold", color="#1a73e8"),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.only(left=12, top=8, bottom=24),
                    alignment=ft.alignment.Alignment(-1, 0),
                ),
                self.new_chat_btn,
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text(t("recent"), size=12, weight="bold", color="#444746"),
                    padding=ft.padding.only(left=16)
                ),
                self.items_list,
                ft.Container(expand=True),
                ft.Divider(height=1),
                self.settings_item,
            ],
            expand=True,
        )
        self.build_items("1")


    def build_items(self, selected_id):
        self.items_list.controls.clear()
        # 更新设置按钮的状态
        self.settings_item.selected = selected_id == "settings"
        self.settings_item.bgcolor = "#E1EBFD" if selected_id == "settings" else ft.Colors.TRANSPARENT
        # 注意：SidebarItem 内部的颜色也需要更新，但这里简单处理背景色
        
        for chat in self.chats:
            is_selected = chat["id"] == selected_id
            self.items_list.controls.append(
                SidebarItem(
                    chat["title"], 
                    "", 
                    chat["icon"], 
                    lambda e, cid=chat["id"]: self.handle_click(cid),
                    selected=is_selected
                )
            )

    def handle_click(self, chat_id):
        self.build_items(chat_id)
        self.update()
        self.on_change_chat(chat_id)
