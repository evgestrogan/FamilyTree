from unittest import IsolatedAsyncioTestCase

from sqlmodel import select, or_

from core.database.crud import Crud
from core.database.migrations import clear_tables
from tree.models import NodeDataBase, UserNodeMapper
from user.models import UserDataBase


class UserCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncTearDown(self):
        await clear_tables()

    async def test_get_node_with_link(self):
        user_1 = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user_2 = await Crud.save(UserDataBase(username='zero', password=b'veverbi3444', email='zero@mail.com'))
        user_3 = await Crud.save(UserDataBase(username='mash', password=b'veverbi3441', email='mash@mail.com'))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user_1))
        await Crud.save(UserNodeMapper(user_id=user_2, node_id=node))
        await Crud.save(UserNodeMapper(user_id=user_3, node_id=node))

        node_with_link = await Crud.get_all(select(NodeDataBase, UserNodeMapper).
                                            where(NodeDataBase.id == node, NodeDataBase.id == UserNodeMapper.node_id))
        node_data_base = node_with_link[0][0]
        user_id_list = [item[1].user_id for item in node_with_link]
        user_in = user_2 in user_id_list and user_3 in user_id_list

        self.assertEqual(len(node_with_link), 2)
        self.assertEqual(user_in, True)
        self.assertEqual(node_data_base.id, node)

    async def test_get_nodes(self):
        user_1 = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user_2 = await Crud.save(UserDataBase(username='zero', password=b'veverbi3444', email='zero@mail.com'))
        user_3 = await Crud.save(UserDataBase(username='mash', password=b'veverbi3441', email='mash@mail.com'))
        user_4 = await Crud.save(UserDataBase(username='evgen', password=b'veverbi3441', email='evgen@mail.com'))
        user_5 = await Crud.save(UserDataBase(username='kirill', password=b'veverbi3441', email='kirill@mail.com'))
        node_1 = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user_1, user_id=user_4))
        node_2 = await Crud.save(NodeDataBase(name='Sergei', family_name='Bichkoy', author_id=user_2, user_id=user_3))
        await Crud.save(UserNodeMapper(user_id=user_4, node_id=node_1))
        await Crud.save(UserNodeMapper(user_id=user_4, node_id=node_2))

        nodes = await Crud.get_all(select(NodeDataBase).where(NodeDataBase.id == UserNodeMapper.node_id,
                                                              or_(UserNodeMapper.user_id == user_4,
                                                                  NodeDataBase.author_id == user_4,
                                                                  NodeDataBase.user_id == user_4)))

        self.assertEqual(len(nodes), 2)

        nodes_2 = await Crud.get_all(select(NodeDataBase).where(NodeDataBase.id == UserNodeMapper.node_id,
                                                                or_(UserNodeMapper.user_id == user_5,
                                                                    NodeDataBase.author_id == user_5,
                                                                    NodeDataBase.user_id == user_5)))

        self.assertEqual(len(nodes_2), 0)

        nodes_3 = await Crud.get_all(select(NodeDataBase).where(NodeDataBase.id == UserNodeMapper.node_id,
                                                                or_(UserNodeMapper.user_id == user_1,
                                                                    NodeDataBase.author_id == user_1,
                                                                    NodeDataBase.user_id == user_1)))

        self.assertEqual(len(nodes_3), 1)
