import json
from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient
from sqlmodel import select

from core.database.crud import Crud
from core.database.migrations import clear_tables
from main import app
from user.models import UserDataBase


class UserApiTestCase(IsolatedAsyncioTestCase):

    async def asyncTearDown(self):
        await clear_tables()

    async def test_get_user(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/{user}")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertEqual(user_data['username'], 'pushkin')
        self.assertEqual(user_data['email'], 'pushkin@mail.com')

    async def test_get_not_exist_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/119104c1-ae00-43d4-9d43-f2a06d497e29")
        self.assertEqual(response.status_code, 204)

    async def test_get_user_by_wrong_id(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/10e234vredv32")
        self.assertEqual(response.status_code, 204)

    async def test_create_user(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'andrey@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", json=user)
        self.assertEqual(response.status_code, 201)
        user_id = response.content.decode("utf-8").replace('\"', '')
        database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        self.assertEqual(database_user.username, 'andrey')

    async def test_create_user_with_same_email(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", json=user)
        self.assertEqual(response.status_code, 409)

    async def test_create_user_with_short_password(self):
        user = {'username': 'andrey', 'password': '1234567', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", json=user)
        self.assertEqual(response.status_code, 406)

    async def test_create_user_with_short_name(self):
        user = {'username': 'and', 'password': '12345678910', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", json=user)
        self.assertEqual(response.status_code, 406)

    async def test_get_users(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(UserDataBase(username='andrey', password=b'veverrgbrbbi344', email='andrey@mail.com'))
        await Crud.save(UserDataBase(username='roman', password=b'wfvvw4r2fveffv', email='roman@mail.com'))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertIsInstance(user_data, list)
        self.assertEqual(3, len(user_data))

    async def test_get_empty_users(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertIsInstance(user_data, list)
        self.assertEqual(0, len(user_data))

    async def test_update_user(self):
        user_id = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        data = {'username': 'andrey'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/user/{user_id}", json=data)
        self.assertEqual(response.status_code, 201)
        update_user_id = response.content.decode("utf-8").replace('\"', '')
        self.assertEqual(update_user_id, str(user_id))
        database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        self.assertEqual(database_user.username, 'andrey')

    async def test_update_not_exist_user(self):
        data = {'username': 'andrey'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/user/12", json=data)
        self.assertEqual(response.status_code, 204)

    async def test_update_user_with_same_email(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user_id = await Crud.save(UserDataBase(username='andrey', password=b'rb4gt4gbtrb', email='andrey@mail.com'))
        data = {'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/user/{user_id}", json=data)
        self.assertEqual(response.status_code, 409)

    async def test_delete_user(self):
        user_id = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.delete(f"/user/{user_id}")
        self.assertEqual(response.status_code, 200)
        database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        self.assertIsNone(database_user)

    async def test_delete_not_exist_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.delete(f"/user/12")
        self.assertEqual(response.status_code, 204)

    async def test_delete_user_with_wrong_id(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.delete(f"/user/123fbdsb324")
        self.assertEqual(response.status_code, 204)





