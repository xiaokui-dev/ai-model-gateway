import uuid
import sys
import traceback
from loguru import logger
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.responses import Response
from starlette.datastructures import MutableHeaders


class LoggerConfig:
    @staticmethod
    def setup_logger():
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | " \
                     "<level>{level: <8}</level> | " \
                     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - " \
                     "<magenta>{process}</magenta>  " \
                     "<yellow>{thread}</yellow> " \
                     "<blue>{extra[request_id]}</blue> | " \
                     "<level>{message}</level>"
        logger.remove()
        logger.add(sys.stdout, level="INFO", format=log_format)


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp, header_name: str = 'X-Request-ID'):
        self.app = app
        self.header_name = header_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] not in ('http', 'websocket'):
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4()).replace("-", "")
        with logger.contextualize(request_id=request_id):
            logger.info(f"Request start {scope['method']} {scope['path']}")

            async def send_wrapper(message):
                if message['type'] == 'http.response.start':
                    headers = MutableHeaders(raw=message['headers'])
                    headers.append(self.header_name, request_id)
                    message['headers'] = headers.items()
                await send(message)

            try:
                await self.app(scope, receive, send_wrapper)
            except Exception as ex:
                traceback_str = traceback.format_exc()
                logger.error(f"Request Error: {ex}\n{traceback_str}")
                error_response = Response(content=str(ex), status_code=500)
                await error_response(scope, receive, send_wrapper)
            finally:
                logger.info(f"Request end {scope['method']} {scope['path']}")
