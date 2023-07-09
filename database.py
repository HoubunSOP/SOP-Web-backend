import aiomysql
import yaml


class Database:
    def __init__(self):
        with open('config.yml', 'r') as f:
            self.config = yaml.safe_load(f)['database']
        self.pool = None

    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                db=self.config['database'],
                autocommit=True,
                cursorclass=aiomysql.cursors.DictCursor
            )
        except Exception as e:
            print('数据库无法连接，请检查后重试：', e)
            exit()

    async def disconnect(self):
        self.pool.close()
        await self.pool.wait_closed()

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchall()

    async def execute_many(self, query, args_list):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.executemany(query, args_list)
                return await cursor.fetchall()