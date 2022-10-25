import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from httpx import AsyncClient
from sqlmodel import select

from core.database.crud import Crud
from core.database.migrations import clear_tables
from main import app
from user.models import UserDataBase


def send_massage(to: str, subject: str, text: str):
    global token
    token = text[text.find('eyJhbGc'):-10]
    return None


class AuthenticationApiTestCase(IsolatedAsyncioTestCase):

    user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}

    async def asyncTearDown(self):
        await clear_tables()

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_register_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=self.user)
        self.assertEqual(response.status_code, 201)
        user_id = response.content.decode("utf-8").replace('\"', '')
        database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        self.assertEqual(database_user.username, 'andrey')

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_activate_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_registrate = await ac.post(f"/authentication/registration", json=self.user)
            response_activate = await ac.put(f"/authentication/activate/{token}")
        self.assertEqual(response_registrate.status_code, 201)
        self.assertEqual(response_activate.status_code, 201)
        user_id = response_registrate.content.decode("utf-8").replace('\"', '')
        database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        self.assertEqual(database_user.username, 'andrey')
        self.assertEqual(database_user.active, True)

    async def test_register_user_with_same_email(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=self.user)
        self.assertEqual(response.status_code, 409)

    async def test_register_user_with_short_password(self):
        user = {'username': 'andrey', 'password': '1234567', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=user)
        self.assertEqual(response.status_code, 406)

    async def test_register_user_with_short_name(self):
        user = {'username': 'and', 'password': '12345678910', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=user)
        self.assertEqual(response.status_code, 406)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_login(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=self.user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 200)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_login_no_active_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            await ac.post(f"/authentication/registration", json=self.user)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 403)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_login_with_wrong_password(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=self.user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '235431brgb'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 403)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_login_with_wrong_username(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=self.user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 403)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_refresh(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=self.user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            await ac.post(f"/authentication/login", json=auth_data)
            response_refresh = await ac.get(f"/authentication/refresh")
        self.assertEqual(response_refresh.status_code, 200)

    async def test_refresh_without_cookies(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_refresh = await ac.get(f"/authentication/refresh")
        self.assertEqual(response_refresh.status_code, 403)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_logout(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=self.user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
            response_data = json.loads(response_login.content)
            response_logout = await ac.get(f"/authentication/logout", headers={'x-access-token': response_data['access_token']})
        self.assertEqual(response_logout.status_code, 200)

    @patch('core.email.driver.mail.send_message', send_massage)
    async def test_recovery_password(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=self.user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        start_recovery_password_data = {'email': 'pushkin@mail.com'}
        recovery_password_data = {'password': 'A1234545n'}
        wrong_auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        auth_data = {'username': 'andrey', 'password': 'A1234545n'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_start = await ac.post(f"/authentication/start_recovery_password", json=start_recovery_password_data)
            response_check = await ac.get(f"/authentication/check_recovery_password/{token}")
            response_recovery = await ac.put(f"/authentication/recovery_password/{token}", json=recovery_password_data)
            response_wrong_login = await ac.post(f"/authentication/login", json=wrong_auth_data)
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_start.status_code, 200)
        self.assertEqual(response_check.status_code, 200)
        self.assertEqual(response_recovery.status_code, 200)
        self.assertEqual(response_wrong_login.status_code, 403)
        self.assertEqual(response_login.status_code, 200)




