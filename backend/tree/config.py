import uuid
from typing import List

from starlette import status

from core.additional import BaseUrlConfig
from core.config import ResponseDescription
from tree.models import NodeSchemaGet


class NodeUrlConfig(BaseUrlConfig):
    responses: dict | None


get_node_url_config = NodeUrlConfig(
    tags=['node'],
    name='Узел дерева',
    description='Получить узел дерева по его ID',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value,
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value
    },
    response_model=NodeSchemaGet,
    status_code=status.HTTP_200_OK
)


get_nodes_url_config = NodeUrlConfig(
    tags=['node'],
    name='Узел дерева',
    description='Получить узел дерева по его ID',
    response_model=List[NodeSchemaGet],
    status_code=status.HTTP_200_OK
)


get_children_url_config = NodeUrlConfig(
    tags=['node'],
    name='Дети',
    description='Получить детей по ID',
    response_model=List[NodeSchemaGet],
    status_code=status.HTTP_200_OK
)


search_nodes_url_config = NodeUrlConfig(
    tags=['node'],
    name='Найти узел дерева',
    description='Найти узел дерева по строке',
    response_model=List[NodeSchemaGet],
    status_code=status.HTTP_200_OK
)


find_nodes_url_config = NodeUrlConfig(
    tags=['node'],
    name='Найти узел дерева',
    description='Найти узел дерева по его параметрам',
    response_model=List[NodeSchemaGet],
    status_code=status.HTTP_200_OK
)


create_node_url_config = NodeUrlConfig(
    tags=['node'],
    name='Создать узел дерева',
    description='Добавить человека в систему',
    responses={
        status.HTTP_401_UNAUTHORIZED: ResponseDescription.CONFLICT.value,
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=uuid.UUID,
    status_code=status.HTTP_201_CREATED
)


update_node_url_config = NodeUrlConfig(
    tags=['node'],
    name='Обновить узел дерева',
    description='Обновить информацию о человеке',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.CONFLICT.value,
        status.HTTP_401_UNAUTHORIZED: ResponseDescription.CONFLICT.value,
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=uuid.UUID,
    status_code=status.HTTP_201_CREATED
)


create_partner_url_config = NodeUrlConfig(
    tags=['node'],
    name='Создать брак',
    description='Добавить семейную связь (муж/жена)',
    responses={
        status.HTTP_401_UNAUTHORIZED: ResponseDescription.CONFLICT.value,
        status.HTTP_422_UNPROCESSABLE_ENTITY: ResponseDescription.CONFLICT.value
    },
    response_model=uuid.UUID,
    status_code=status.HTTP_201_CREATED
)


delete_node_url_config = NodeUrlConfig(
    tags=['node'],
    name='Удалить узел дерева',
    description='Удалить человека из системе',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value,
        status.HTTP_401_UNAUTHORIZED: ResponseDescription.CONFLICT.value,
        status.HTTP_403_FORBIDDEN: ResponseDescription.CONFLICT.value,
    },
    response_model=str,
    status_code=status.HTTP_200_OK
)