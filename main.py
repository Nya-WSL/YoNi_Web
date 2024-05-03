import os
import re
import json
import hashlib
from uuid import uuid4
from router import Router
from nicegui import ui, app
from typing import Optional
from fastapi.responses import RedirectResponse

version = "v1.4.2"
pages = []
app.add_static_files('/static', 'static')

@ui.page('/login')
def index() -> Optional[RedirectResponse]:
    with open("user.json", "r", encoding="utf-8") as f:
        user = json.load(f)
    def try_login() -> None:
        if user[username.value] == hashlib.sha256(str(password.value).encode('utf-8')).hexdigest():
            app.storage.user.update({'user': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/admin'))
        else:
            ui.notify('账号密码错误，请重试！', color='negative')

    ui.query('body').style('background: url("static/bg1.png") 0px 0px/cover')
    with ui.card().classes('absolute-center'):
        # ui.badge('YoNi登记处', outline=True, color='', text_color='#E6354F').classes('text-xl')
        username = ui.input('账号').on('keydown.enter', try_login)
        password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        with ui.row():
            ui.button('登陆', on_click=try_login)
            ui.button('返回', on_click=lambda: ui.open("/"))

@ui.page('/admin')
def index():
    def add_text():
        with open(f"data/{add_list_select.value}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if add_name.value == "":
            ui.notify('歌名为空！', color='negative')
        else:
            if add_name.value in data:
                ui.notify(f'在歌单[{add_list_select.value}文]中已存在"{add_name.value}"！', color='negative')
            else:
                data.append(f"{add_name.value}")
                try:
                    with open(f"data/{add_list_select.value}.json", "w+", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    ui.notify(f'已成功在歌单[{add_list_select.value}文]中添加"{add_name.value}"！', color='positive')
                except:
                    ui.notify(f'在歌单[{add_list_select.value}文]中添加"{add_name.value}"失败！', color='negative')

    def del_text():
        with open(f"data/{del_list_select.value}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if del_name.value == "":
            ui.notify('歌名为空！', color='negative')
        else:
            if not del_name.value in data:
                ui.notify(f'在歌单[{del_list_select.value}文]中不存在"{del_name.value}"！', color='negative')
            else:
                data.remove(del_name.value)
                try:
                    with open(f"data/{del_list_select.value}.json", "w+", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    ui.notify(f'已成功在歌单[{del_list_select.value}文]中删除"{del_name.value}"！', color='positive')
                except:
                    ui.notify(f'在歌单[{del_list_select.value}文]中删除"{del_name.value}"失败！', color='negative')

    def change_text():
        with open(f"data/{change_list_select.value}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if old_name.value == "":
            ui.notify('旧歌名为空！', color='negative')
        if change_name.value == "":
            ui.notify('新歌名为空！', color='negative')
        else:
            if not old_name.value in data:
                ui.notify(f'在歌单[{change_list_select.value}文]中不存在"{old_name.value}"！', color='negative')
            else:
                try:
                    index = 0
                    for i in data:
                        index += 1
                        if i == old_name.value:
                            print(index)
                            data[index - 1] = change_name.value
                    with open(f"data/{change_list_select.value}.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    ui.notify(f'已成功修改歌单[{change_list_select.value}文]中的"{old_name.value}"为"{change_name.value}"！', color='positive')
                except:
                    ui.notify(f'修改歌单[{change_list_select.value}文]中的"{old_name.value}"为"{change_name.value}"失败！', color='negative')

    def back() -> None:
        app.storage.user.update({'authenticated': False})
        ui.open('/')

    if not app.storage.user.get('authenticated'):
        return RedirectResponse('/login')

    ui.query('body').style('background: url("static/bg1.png") 0px 0px/cover')
    ui.button("返回", on_click=back)

    with ui.card().classes('absolute-center'):
        ui.badge('YoNi歌单管理处', outline=True, color='', text_color='#E6354F').classes('text-xl')
        with ui.row():
            add_list_select = ui.select(["中", "日", "英"], value="中")
            add_name = ui.input(label="歌名")
            ui.button("添加", on_click=lambda: add_text())
        with ui.row():
            del_list_select = ui.select(["中", "日", "英"], value="中")
            del_name = ui.input(label="歌名")
            ui.button("删除", on_click=lambda: del_text())
        with ui.row():
            change_list_select = ui.select(["中", "日", "英"], value="中")
            old_name = ui.input(label="旧歌名").style("width: 78px")
            change_name = ui.input(label="新歌名").style("width: 79px")
            ui.button("修改", on_click=lambda: change_text())

for dir in os.walk("data"):
    for file in dir[2]:
        if file.endswith(".json"):
            page = str(file).replace(".json", "")
            pages.append(page)

def main():
    router = Router()
    page_id = str(uuid4())
    search_id = str(uuid4()) + "/s"

    @router.add('/')
    def index():
        ui.button("管理", on_click=lambda: ui.open('/admin'))
        router.open(f'/{page_id}')

    @router.add('/nicegui/')
    def index():
        ui.button("管理", on_click=lambda: ui.open('/admin'))
        router.open(f'/nicegui/{page_id}')

    @router.add(f'/{page_id}')
    def index():
        ui.button("管理", on_click=lambda: ui.open('/admin'))
        with ui.card().classes("absolute-center"):
            ui.query('body').style('background: url("/static/bg1.png") 0px 0px')
            ui.badge(f"岚枳的歌单 | {version}", outline=False)
            with ui.row():
                ui.button("刷新", on_click=lambda: ui.open('/'))
                ui.button("搜索", on_click=lambda: router.open(f"/{search_id}"))
            for page in pages:
                _page = ""
                if page == "中":
                    _page = "zh"
                if page == "日":
                    _page = "jp"
                if page == "英":
                    _page = "en"
                ui.button(page, on_click=lambda _page = _page : ui.open(_page)).classes("w-full")
                @ui.page(f"/{_page}")
                def page_view(page = page):
                    ui.query('body').style('background: url("/static/bg.png") 0px 0px')
                    file = f"data/{page}.json"
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    ui.button("返回", on_click=lambda: ui.open('/'))
                    ui.badge(f"岚枳的歌单 | {page} | {version}", outline=False)
                    for text in data:
                        ui.chat_message(text, avatar='/static/YoNi.jpg').props('bg-color="green-1"')

    @router.add(f'/{search_id}')
    def index():
        def search():
            with open(f"data/{target_list_select.value}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            match = [value for value in data if re.search(name.value, value)]
            @router.add(f'/{search_id}/result')
            def index():
                with ui.row():
                    ui.button("管理", on_click=lambda: ui.open('/admin'))
                    ui.button("返回", on_click=lambda: router.open(f"/{search_id}"))
                with ui.element():
                    ui.html(f"""<br>
关键词：{name.value}<br>
搜索结果：从{len(data)}个歌名中找到{len(match)}个匹配项<br><br>""")
                    for i in match:
                        ui.chat_message(i, name="YoNi", avatar='/static/YoNi.jpg').props('bg-color="deep-purple-3"')
            router.open(f'/{search_id}/result')

        with ui.card().classes("absolute-center") as card:
            ui.query('body').style('background: url("/static/bg1.png") 0px 0px')
            ui.badge(f"岚枳的歌单 | {version}", outline=False)
            with ui.row():
                target_list_select = ui.select(["中", "日", "英"], value="中").style("width: 30px")
                name = ui.input(label="关键词")
                ui.button("搜索", on_click=lambda: search())

    @router.add(f'/nicegui/{search_id}')
    def index():
        def search():
            ui.query('body').style('background: url("/nicegui/static/bg1.png") 0px 0px')
            with open(f"data/{target_list_select.value}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            match = [value for value in data if re.search(name.value, value)]
            @router.add(f'/nicegui/{search_id}/result')
            def index():
                with ui.row():
                    ui.button("管理", on_click=lambda: ui.open('/admin'))
                    ui.button("返回", on_click=lambda: router.open(f"/nicegui/{search_id}"))
                with ui.element():
                    ui.html(f"""<br>
关键词：{name.value}<br>
搜索结果：从{len(data)}个歌名中找到{len(match)}个匹配项<br><br>""")
                    for i in match:
                        ui.chat_message(i, name="YoNi", avatar='/nicegui/static/YoNi.jpg').props('bg-color="deep-purple-3"')
            router.open(f'/nicegui/{search_id}/result')

        ui.query('body').style('background: url("/nicegui/static/bg1.png") 0px 0px')
        with ui.card().classes("absolute-center") as card:
            ui.badge(f"岚枳的歌单 | {version}", outline=False)
            with ui.row():
                target_list_select = ui.select(["中", "日", "英"], value="中").style("width: 30px")
                name = ui.input(label="关键词")
                ui.button("搜索", on_click=lambda: search())

    @router.add(f'/nicegui/{page_id}')
    def index():
        ui.button("管理", on_click=lambda: ui.open('/admin'))
        with ui.card().classes("absolute-center"):
            ui.query('body').style('background: url("/nicegui/static/bg1.png") 0px 0px')
            ui.badge(f"岚枳的歌单 | {version}", outline=False)
            with ui.row():
                ui.button("刷新", on_click=lambda: ui.open('/'))
                ui.button("搜索", on_click=lambda: router.open(f"/nicegui/{search_id}"))
            for page in pages:
                _page = ""
                if page == "中":
                    _page = "zh"
                if page == "日":
                    _page = "jp"
                if page == "英":
                    _page = "en"
                ui.button(page, on_click=lambda _page = _page : ui.open(_page)).classes("w-full")
                @ui.page(f"/{_page}")
                def page_view(page = page):
                    ui.query('body').style('background: url("/nicegui/static/bg.png") 0px 0px')
                    file = f"data/{page}.json"
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    ui.button("返回", on_click=lambda: ui.open('/'))
                    ui.badge(f"岚枳的歌单 | {page} | {version}", outline=False)
                    for text in data:
                        ui.chat_message(text, avatar='/nicegui/static/YoNi.jpg').props('bg-color="green-1"')

    router.frame().classes('w-full')

@ui.page('/')
def index():
    main()

ui.run(title="岚枳的歌单", favicon="static/icon.png", host="0.0.0.0", port=11455, language="zh-CN", show=False, storage_secret='c2b95787b44c084fc7c7d2c8422917913e0b1a673892f7d1f644bcf73c133410')