from unittest import IsolatedAsyncioTestCase

from sqlmodel import select

from authentication.functions import create_refresh_token
from authentication.models import BaseRefreshToken
from core.database.crud import Crud
from core.database.driver import init_db
from core.database.migrations import clear_tables
from user.models import UserDataBase


class AuthenticationCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        init_db()

    async def asyncTearDown(self):
        await clear_tables()

    async def test_get_refresh_token_by_id(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        token = await Crud.save(create_refresh_token(user))
        token_data: BaseRefreshToken = await Crud.get(select(BaseRefreshToken).where(BaseRefreshToken.id == token))
        self.assertEqual(token_data.user_id, user)

    async def test_get_not_exist_token(self):
        token_data: BaseRefreshToken = await Crud.get(select(BaseRefreshToken).where(BaseRefreshToken.id == 12))
        self.assertIsNone(token_data)

    async def test_get_token_with_wrong_id(self):
        token_data: BaseRefreshToken = await Crud.get(select(BaseRefreshToken).where(BaseRefreshToken.id == 'sg32rged'))
        self.assertIsNone(token_data)

    async def test_get_all_tokens(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(create_refresh_token(user))
        await Crud.save(create_refresh_token(user))
        await Crud.save(create_refresh_token(user))
        tokens = await Crud.get_all(select(BaseRefreshToken))
        self.assertIsInstance(tokens, list)
        self.assertEqual(3, len(tokens))

    async def test_remove_token(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(create_refresh_token(user))
        token_id = await Crud.save(create_refresh_token(user))
        token = await Crud.get(select(BaseRefreshToken).where(BaseRefreshToken.id == token_id))
        await Crud.delete(token)
        token = await Crud.get(select(BaseRefreshToken).where(BaseRefreshToken.id == token_id))
        tokens = await Crud.get_all(select(BaseRefreshToken))
        self.assertEqual(1, len(tokens))
        self.assertIsNone(token)

    async def test_find_token(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(create_refresh_token(user))
        await Crud.save(create_refresh_token(user))
        tokens = await Crud.get_all(select(BaseRefreshToken).where(BaseRefreshToken.user_id == user))
        self.assertIsInstance(tokens, list)
        self.assertEqual(2, len(tokens))

    async def test_find_not_exist_token(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(create_refresh_token(user))
        tokens = await Crud.get_all(select(BaseRefreshToken).where(BaseRefreshToken.user_id == ('user'+'1')))
        self.assertIsInstance(tokens, list)
        self.assertEqual(0, len(tokens))

