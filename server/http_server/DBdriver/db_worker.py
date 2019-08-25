import sqlite3
from loguru import logger
from ..utils import settings

class SingletonMeta(type):
    """
    В Python класс Одиночка можно реализовать по-разному. Возможные способы
    включают себя базовый класс, декоратор, метакласс. Мы воспользуемся
    метаклассом, поскольку он лучше всего подходит для этой цели.
    """

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

class DBWorker(metaclass=SingletonMeta):
    def __init__(self):
        self.connect_db()
        logger.info(self.cursor)


    def connect_db(self):
        self.conn = sqlite3.connect("DB.db")
        self.cursor = self.conn.cursor()


    def add_new_user(self, login, password):
        img_url = settings.image_url.format(login)
        logger.info(img_url)
        self.cursor.execute('''INSERT OR IGNORE INTO "users_info" (login, password, role, image)
                        VALUES ('{}', '{}', {}, '{}')'''.format(login, password, 1, img_url))
        self.conn.commit()
        logger.info(self.cursor.lastrowid)
        if self.cursor.lastrowid:
            return {"id": self.cursor.lastrowid, "login": login, "role": 1, "img_url": img_url}
        return False


    def get_user(self, login):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' '''.format(login))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4]}
        return False


    def authentication(self, login, password):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' and password = '{}' '''.format(login, password))
        k = self.cursor.fetchone()
        logger.info(k)
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4]}
        return False


    def get_fullchannels(self):
        self.cursor.execute('''SELECT * FROM "channels" ''')
        k = self.cursor.fetchall()
        l = list()
        logger.info(k)
        for i in k:
            l.append({"id": i[0], "name": i[1], "description": i[2], "img_url": i[3]})
        logger.info(l)
        if k:
            return l
        return False


    def get_channel(self, id):
        self.cursor.execute('''SELECT * FROM "channels" WHERE id = {} '''.format(id))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "name": k[1], "description": k[2], "img_url": k[3]}
        return False