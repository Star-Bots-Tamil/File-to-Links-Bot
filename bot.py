import logging
import logging.config
import sys
import glob
import importlib
from pathlib import Path
from pyrogram import idle
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)
from pyrogram import __version__
from info import *
from aiohttp import web
from plugins import web_server
import asyncio
from pyrogram import idle
from stream.bot import StarMoviessBot
from stream.utils.keepalive import ping_server
from stream.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
StarMoviessBot.start()
loop = asyncio.get_event_loop()

async def Star_start():
    print('\n')
    print('Initalizing Star Movies Bot')
    bot_info = await StarMoviessBot.get_me()
    StarMoviessBot.username = bot_info.username
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
    if WEBHOOK:
        asyncio.create_task(ping_server())
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(Star_start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')

