import asyncio
import logging
import time

from remote import Host


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger()

if __name__ == '__main__':
    host = Host('remote01')
    host.connect()
    s_time = time.time()
    host.get_file('/data/files', 'download/post2')
    e_time = time.time()
    log.info(f'下载 耗时: {e_time - s_time}秒')
    print('下载完毕')
    host.close()

