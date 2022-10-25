from unittest import IsolatedAsyncioTestCase

from sqlmodel import select

from core.database.crud import Crud
from core.database.migrations import clear_tables
from core.exception.base_exeption import UniqueIndexException
from user.models import UserDataBase


class UserCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncTearDown(self):
        await clear_tables()

    async def test_get_user_by_id(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user_data: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user))
        self.assertEqual(user_data.username, 'pushkin')
        self.assertEqual(user_data.email, 'pushkin@mail.com')
        self.assertEqual(user_data.password, b'veverbi344')

    async def test_not_exist_user(self):
        user_data = await Crud.get(select(UserDataBase).where(UserDataBase.id == '119104c1-ae00-43d4-9d43-f2a06d497e29'))
        self.assertIsNone(user_data)

    async def test_user_by_wrong_id(self):
        user_data = await Crud.get(select(UserDataBase).where(UserDataBase.id == '10'))
        self.assertIsNone(user_data)

    async def test_create_with_same_email(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        with self.assertRaises(UniqueIndexException) as e:
            await Crud.save(UserDataBase(username='zero', password=b'343g3ewqe23', email='pushkin@mail.com'))
            self.assertIsInstance(e, UniqueIndexException)

    async def test_get_all_users(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(UserDataBase(username='evgestrogan', password=b'btrbt345', email='evgestrogan@mail.com'))
        await Crud.save(UserDataBase(username='nikolay', password=b'grbwvr4315btr', email='nikolay@mail.com'))
        users = await Crud.get_all(select(UserDataBase))
        self.assertIsInstance(users, list)
        self.assertEqual(3, len(users))

    async def test_remove_user(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user = await Crud.save(UserDataBase(username='evgestrogan', password=b'btrbt345', email='evgestrogan@mail.com'))
        await Crud.delete(await Crud.get(select(UserDataBase).where(UserDataBase.id == user)))
        users = await Crud.get_all(select(UserDataBase))
        self.assertEqual(1, len(users))

    async def test_find_user(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(UserDataBase(username='anton', password=b'rb43q4gbtrb3', email='anton@mail.com'))
        find_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.username == 'anton'))
        self.assertEqual('anton@mail.com', find_user.email)

    async def test_find_not_exist_user(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        find_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.username == 'anton'))
        self.assertIsNone(find_user)




