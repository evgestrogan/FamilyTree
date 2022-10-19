import json
import os
from enum import Enum

import yaml
from pydantic.tools import lru_cache


class ResponseDescription(Enum):
    CONFLICT: Enum = {
        "description": "Ошибка проверки уникальности значений",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                          "loc": [
                            "string"
                          ],
                          "msg": "string",
                          "type": "string"
                        }
                      ]
                }
            }
        }
    }
    NO_CONTENT: Enum = {
        "description": "Пустой ответ"
    }


@lru_cache
def load_config(path: str) -> dict:
    if path.split('.')[-1] == 'json':
        with open(path, 'r') as outfile:
            return json.loads(outfile.read())
    elif path.split('.')[-1] == 'yaml':
        with open(path, 'r') as outfile:
            return yaml.safe_load(outfile)


applications = [
    'authentication',
    'user'
]


project_config = load_config(os.environ.get('config_path', 'config.yaml'))

