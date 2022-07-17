import json

class Buffer:
    def __init__(self, file):
        self.file = file

    async def get_buffer(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def set_buffer(self, user_id, buffer_data):
        data = await self.get_buffer()
        new_data = { str(user_id): str(buffer_data) }
        data.update(new_data)
        with open(self.file, "w") as json_data:
            json.dump(data, json_data, indent=2)

class Users:
    def __init__(self, file):
        self.file = file

    async def get_users(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def add_user(self, user_id):
        datas = await self.get_users()
        datas.append(user_id)
        with open(self.file, "w") as json_data:
            json.dump(datas, json_data, indent=2)

    async def del_user(self, user_id):
        data = await self.get_users()
        data.remove(user_id)
        with open(self.file, "w") as json_data:
            json.dump(data, json_data, indent=2)

class Words:
    def __init__(self, file):
        self.file = file

    async def get_buffer(self):
        with open(self.file, "r") as json_data:
            return json.load(json_data)

    async def set_buffer(self, user_id, buffer_data):
        data = await self.get_buffer()
        new_data = { str(user_id): str(buffer_data) }
        data.update(new_data)
        with open(self.file, "w") as json_data:
            json.dump(data, json_data, indent=2)