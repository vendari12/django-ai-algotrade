"""
ASGI config for stockze project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application



# This allows easy placement of apps within the interior
# stockze directory.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "stockze"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# Import websocket application here, so apps from django_application are loaded first
from config.websocket import websocket_application  # noqa isort:skip
'''
import pypeln as pl
import asyncio
django_application = pl.task.map(django_application(scope, receive, send), workers=max)
django_application = list(django_application)
'''

async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")

import socketio
import engineio
sio = socketio.AsyncServer(async_mode='asgi', client_manager=socketio.AsyncRedisManager('redis://redis:6379/0'), logger=False, engineio_logger=True, ping_timeout=60000000, ping_interval= 6000000)
application = engineio.ASGIApp(sio, application)

'''
import pypeln as pl
application = pl.task.map(application, workers=max)
application = list(application)
'''
#import sys
#stage = pl.process.map(application, stage, workers=3, on_start=on_start, on_end=on_end)
#application = pl.sync.map(application, workers=1)
#application = list(application)
'''
async def application(scope, receive, send):
    if scope["type"] == "http":
        django_application(scope, receive, send)
        await pl.task.each.django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        websocket_application(scope, receive, send)
        await pl.task.each.websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
  
def application(scope, receive, send):
    if scope["type"] == "http":
        async def django_application(scope, receive, send)
            stage = pl.task.map(django_application, workers=max)
            await stage
    elif scope["type"] == "websocket":
        async def websocket_application(scope, receive, send)
            stage = pl.task.map(websocket_application, workers=max)
            await stage
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
'''
'''
import socketio
import engineio
#import gevent
#import eventlet

sio = socketio.AsyncServer(async_mode='asgi', client_manager=socketio.AsyncRedisManager('redis://redis:6379/0'))
#sio = socketio.AsyncServer(async_mode='gevent/eventlet', client_manager=socketio.AsyncRedisManager('redis://redis:6379/0')) #fails
#sio = socketio.AsyncServer(async_mode='aiohttp', client_manager=socketio.AsyncRedisManager('redis://redis:6379/0')) #works
#sio = socketio.AsyncServer(async_mode='tornado', client_manager=socketio.AsyncRedisManager('redis://redis:6379/0')) #works aiohttp
application = engineio.ASGIApp(sio, application)
#application = socketio.ASGIApp(sio, application) #?complicated
'''
#application = pl.sync.map(application, workers=max)
#application = list(application)

#import pypeln as pl
#application = pl.task.map(application)
#application = pl.process.map(application, stage, workers=3, on_start=on_start, on_end=on_end)

#sio = socketio.AsyncServer(async_mode='wsgi', client_manager=socketio.AsyncRedisManager('redis://redis:6379/0')) #reduced
#application = socketio.ASGIApp(sio, application) #?complicated
#application = pl.task.each(application)

#import asyncio

#application = asyncio.run(application()) #works 404
#application = asyncio.run(application.serve_forever()) #438
#application = asyncio.run(application.start_server()) #438
#application = asyncio.start_server(application()) #works 454
#asyncio.run_until_complete(application.serve_forever()) #works 604 - 603 - 547
#asyncio.run(_main_coroutine(application, functools.partial(asyncio.start_server), _do_nothing, container)) #342

#asyncio.run(_main_coroutine(application.serve_forever(), functools.partial(asyncio.start_server), _do_nothing, container)) #684 fast reset by peer - 553 - 720 - 435 timeout - 727

#asyncio.start_server(_main_coroutine(application.serve_forever(), functools.partial(asyncio.start_server), _do_nothing, container)) # 543 - 715 fast 559
#asyncio.start_server(_main_coroutine(application.serve_forever(), functools.partial(asyncio.run), _do_nothing, container)) #533 fast 439

#asyncio.run(_main_coroutine(application.serve_forever(), functools.partial(asyncio.run), _do_nothing, container)) # 856 fast - timeout - 522 - 438

#asyncio.run_until_complete(_main_coroutine(application.serve_forever(), functools.partial(asyncio.start_server), _do_nothing, container)) #564
#asyncio.run_until_complete(_main_coroutine(application.serve_forever(), functools.partial(asyncio.run_until_complete), _do_nothing, container)) #709 -539 -
