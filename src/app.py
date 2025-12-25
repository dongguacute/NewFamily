import flet as ft
import sys
import os

# 将 src 目录添加到模块搜索路径中，确保可以导入 components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components import ChatBox, Sidebar, SettingsView
from config import config
from i18n import t

def main(page: ft.Page):
    page.title = "NewFamily Chat"
    
    # 根据配置设置主题
    def update_theme():
        page.theme_mode = ft.ThemeMode.DARK if config.dark_mode else ft.ThemeMode.LIGHT
        page.bgcolor = "#1a1a1a" if config.dark_mode else "#FFFFFF"
        page.update()

    def refresh_app():
        # Clear page and rebuild layout
        page.controls.clear()
        
        # Completely recreate the layout components
        new_chat_container = ft.Container(expand=True)
        new_chat_container.content = SettingsView(on_language_change=refresh_app) if current_chat_id[0] == "settings" else ChatBox()
        
        # Update global reference if needed, but here we just rebuild the whole layout
        nonlocal chat_container
        chat_container = new_chat_container
        
        new_sidebar = Sidebar(on_change_chat=change_chat)
        if current_chat_id[0] == "settings":
            new_sidebar.build_items("settings")
        else:
            new_sidebar.build_items(current_chat_id[0])
        
        layout = ft.Row(
            [
                new_sidebar,
                chat_container,
            ],
            expand=True,
            spacing=0,
        )
        page.add(layout)
        update_theme()
        page.update()

    update_theme()
    
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.STANDARD,
    )
    page.padding = 0
    page.window_width = 1000
    page.window_height = 750
    
    chat_container = ft.Container(expand=True)
    current_chat_id = ["1"] # Use a list to make it mutable in closures

    def change_chat(chat_id):
        current_chat_id[0] = chat_id
        if chat_id == "settings":
            # 传递一个回调函数，以便在设置更改时更新主题
            chat_container.content = SettingsView(on_language_change=refresh_app)
            # 监听设置页面的变化（由于 settings_view 直接修改 config，
            # 我们可能需要一种方式让 app.py 知道什么时候更新）
            # 这里简单处理：每次切换回聊天或设置时都更新一次主题
            update_theme()
        else:
            # 根据对话 ID 切换内容
            chat_container.content = ChatBox()
            update_theme()
        page.update()

    # 初始化显示
    chat_container.content = ChatBox()
    
    # 左右布局：侧边栏 + 聊天区域
    layout = ft.Row(
        [
            Sidebar(on_change_chat=change_chat),
            # 移除物理分割线，改用颜色区分
            chat_container,
        ],
        expand=True,
        spacing=0,
    )
    
    page.add(layout)

if __name__ == "__main__":
    # 使用官方推荐的 run() 方法以消除弃用警告
    try:
        ft.run(main)
    except AttributeError:
        # 如果版本过旧没有 run()，回退到 app()
        ft.app(target=main)
