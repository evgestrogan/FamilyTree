import logging.handlers
import os
import uuid

from starlette.datastructures import URL

from core.config import project_config


def get_request_logger():
    request_handler = logging.handlers.TimedRotatingFileHandler(project_config['log']['path'] + 'request.log',
                                                                when='midnight', interval=1, backupCount=5)
    request_handler.setFormatter(
        logging.Formatter(fmt='%(asctime)s | %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))
    request_handler.setLevel(logging.INFO)
    request_logger = logging.getLogger('request')
    request_logger.setLevel(logging.INFO)
    request_logger.addHandler(request_handler)
    return request_logger


def get_error_logger():
    error_handler = logging.handlers.TimedRotatingFileHandler(project_config['log']['path'] + 'error.log',
                                                              when='midnight', interval=1, backupCount=5)
    error_handler.setFormatter(
        logging.Formatter(fmt='%(asctime)s | %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))
    error_handler.setLevel(logging.INFO)
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.INFO)
    error_logger.addHandler(error_handler)
    return error_logger


os.makedirs(project_config['log']['path'], exist_ok=True)
request_logger = get_request_logger()
error_logger = get_error_logger()


def log_request(request_id: uuid, method: str, url: URL, address: str, port: int, user: str | None, status: int) -> None:
    request_logger.info(' | '.join([str(request_id), method, str(url), address, str(port), str(user), str(status)]))


def log_error(request_id: uuid, traceback: str):
    error_logger.info(str(request_id) + ' | traceback: \n' + traceback + '\n' + '-'*200)
