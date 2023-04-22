import logging
import time

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger()

__version__ = '1.0.0'
__all__ = [
    'log_time', 'log'
]


def log_time(func):
    def wrapper(*args, **kwargs):
        # 在调用原始函数前添加新的功能，或在后面添加
        s_time = time.time()
        # 调用原始函数
        result = func(*args, **kwargs)
        # 在结果之前或结果之后添加其他内容
        e_time = time.time()
        log.info(f'{repr(func)} 耗时: {e_time - s_time}秒')
        return result

    return wrapper
