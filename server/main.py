from aiohttp import web

from db import try_make_db, init_db, fetch_user


async def login_handler(request: web.Request) -> web.Response:
    post = await request.json()
    username = post['username']
    password = post['password']
    print(username, password)
    # await fetch_user
    return web.Response(text="Hello world")


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.post("/api/login", login_handler)])
    app.cleanup_ctx.append(init_db)
    return app


try_make_db()
web.run_app(init_app())