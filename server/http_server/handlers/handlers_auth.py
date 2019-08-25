from loguru import logger
from aiohttp import web

from ..DBdriver.db_worker import DBWorker
from ..utils import encode, decode
from ..middlewares import register_with_cors

class HandlersAuth:
    def __init__(self):
        self.db = DBWorker()


    async def get_user(self, request):
        data = await request.json()
        logger.info(data['login'])
        res = self.db.get_user(data['login'])
        logger.info(res)
        if res:
            return web.json_response(res)
        return web.json_response({'message': 'Can`t find this user'}, status=406)


    async def get_me(self, request):
        token = request.headers.get('token')
        decoded = decode(token)

        return web.json_response(decoded)


    @staticmethod
    def register(app):
        this_handler = HandlersAuth()
        register_with_cors(app, 'POST', '/get_me', this_handler.get_me)
        register_with_cors(app, 'POST', '/get_user',  this_handler.get_user)