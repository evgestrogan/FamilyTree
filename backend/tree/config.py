from starlette import status

from backend.core.additional import BaseUrlConfig
from backend.core.config import ResponseDescription
from backend.tree.schemas import NodeSchemaGet


class NodeUrlConfig(BaseUrlConfig):
    responses: dict | None


get_node_url_config = NodeUrlConfig(
    tags=['node'],
    name='Узел дерева',
    description='Получить узел дерева по его ID',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=NodeSchemaGet,
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
    response_model=str,
    status_code=status.HTTP_201_CREATED
)


update_node_url_config = NodeUrlConfig(
    tags=['node'],
    name='Обновить узел дерева',
    description='Обновить сведения о человеке в системе',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value,
        status.HTTP_401_UNAUTHORIZED: ResponseDescription.CONFLICT.value,
        status.HTTP_403_FORBIDDEN: ResponseDescription.CONFLICT.value,
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=str,
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