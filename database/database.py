import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI, PROTECT_CONTENT, DOWNLOAD_TEXT_URL, IS_TUTORIAL, CUSTOM_FILE_CAPTION, SHORTLINK_URL, SHORTLINK_API, IS_SHORTLINK

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            _id=int(id),                                   
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})    

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        b_users = [user['id'] async for user in users]
        return b_users

    async def update_settings(self, id, settings):
        await self.col.update_one({'id': int(id)}, {'$set': {'settings': settings}})

    async def get_settings(self, id):
        default = {
            'file_secure': PROTECT_CONTENT,
            'tutorial' : DOWNLOAD_TEXT_URL,
            'is_tutorial' : IS_TUTORIAL,
            'caption': CUSTOM_FILE_CAPTION,
            'shortlink': SHORTLINK_URL,
            'shortlink_api': SHORTLINK_API,
            'is_shortlink': IS_SHORTLINK
        }
        user = await self.col.find_one({'id':int(id)})
        if user:
            return user.get('settings', default)
        return default

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

db = Database(DATABASE_URI, DATABASE_NAME)
