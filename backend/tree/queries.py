from sqlmodel.sql.expression import Select, SelectOfScalar, col
from sqlmodel import select, or_

from tree.models import NodeDataBase, PartnersMapper, UserNodeMapper, NodeSchemaUpdate


def get_select_nodes_with_partners_query(user_id: str) -> Select | SelectOfScalar:
    return select(NodeDataBase, PartnersMapper). \
        join(UserNodeMapper, isouter=True). \
        join(PartnersMapper,
             or_(PartnersMapper.husband_id == NodeDataBase.id, PartnersMapper.wife_id == NodeDataBase.id),
             isouter=True). \
        where(
        or_(UserNodeMapper.user_id == user_id, NodeDataBase.user_id == user_id, NodeDataBase.author_id == user_id))


def get_select_children_with_partners_query(user_id: str, node_id: str) -> Select | SelectOfScalar:
    return get_select_nodes_with_partners_query(user_id). \
        where(or_(NodeDataBase.father_id == node_id, NodeDataBase.mother_id == node_id))


def get_search_nodes_with_partners_query(user_id: str, query: str) -> Select | SelectOfScalar:
    query_list = query.split(' ')
    return get_select_nodes_with_partners_query(user_id). \
        where(or_(col(NodeDataBase.name).in_(query_list),
                  col(NodeDataBase.family_name).in_(query_list),
                  col(NodeDataBase.father_name).in_(query_list)))


def get_find_nodes_with_partners_query(user_id: str, node: NodeSchemaUpdate) -> Select | SelectOfScalar:
    data_to_find: dict = node.dict(exclude_unset=True)
    return get_select_nodes_with_partners_query(user_id). \
        where(*[getattr(NodeDataBase, item[0]) == item[1] for item in data_to_find.items()])


def get_select_node_with_users_and_partners_query(node_id: str) -> Select | SelectOfScalar:
    return select(NodeDataBase, UserNodeMapper, PartnersMapper). \
        join(UserNodeMapper, isouter=True). \
        join(PartnersMapper,
             or_(PartnersMapper.husband_id == NodeDataBase.id,
                 PartnersMapper.wife_id == NodeDataBase.id),
             isouter=True). \
        where(NodeDataBase.id == node_id)


def get_select_node_with_users_query(node_id: str) -> Select | SelectOfScalar:
    return select(NodeDataBase, UserNodeMapper). \
        join(UserNodeMapper, isouter=True). \
        where(NodeDataBase.id == node_id)
