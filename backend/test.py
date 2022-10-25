import asyncio
import os
import sys

config_path = sys.argv[1] if len(sys.argv) > 1 else "test_config.yaml"
os.environ["config_path"] = config_path

from core.database.migrations import create_db_and_tables, drop_tables


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coroutine = create_db_and_tables()
    loop.run_until_complete(coroutine)
    os.system('python3 -m unittest')
    coroutine = drop_tables()
    loop.run_until_complete(coroutine)

