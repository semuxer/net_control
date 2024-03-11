import threading
import time
import ping3
from nested_dict import nested_dict
from loguru import logger
import datetime
import pygame

from config import conf
from defaults import *


class myping():
    def __init__(self, hosts):
        pygame.init()
        logger.add(LOGNAME, rotation=LOGGERSIZE, level=LOGGERLEVEL,
                   format=LOGGERFORMAT)
        logger.info(f"Контроль зв'язку відновлено.")
        self.hosts = conf(hosts).data
        self.loop = True
        self.thread = threading.Thread(target=self.ping)
        self.thread.start()

    def __del__(self):
        self.stop()

    def stop(self):
        logger.info(f"Контроль зв'язку зупинено.")
        self.loop = False
        self.thread.join()

    def get(self):
        result = True
        for host, data in self.hosts.items():
            result = result & (self.hosts[host]['status'] == 0)
        return result

    def ping(self):
        while self.loop:
            for host, data in self.hosts.items():
                # print(host, data)
                if self.hosts[host]['timecount'] <= 0:
                    self.hosts[host]['timecount'] = self.hosts[host]['timeout']

                    try:
                        r = ping3.ping(host)
                    except:
                        r = None
                    if r is not False and r is not None:  # PING OK

                        if self.hosts[host]['status'] != 0:
                            # відновлено
                            self.hosts[host]['status'] = 0
                            logger.success(f"Відновлено зв'язок з: {host}")

                        self.hosts[host]['skipecount'] = self.hosts[host]['skiperrors']

                    else:  # PING NOT OK
                        if self.hosts[host]['skipecount'] > 0:
                            self.hosts[host]['skipecount'] -= 1
                            if self.hosts[host]['status'] == 0:
                                logger.warning(f"Втрати пакетів з: {host}")
                            # ok!!!!
                        else:
                            self.playerror(host)
                            # errrrrroooorrrr!!!!
                            if self.hosts[host]['status'] != 1:
                                logger.error(f"Втрачено зв'язок з: {host}")
                            self.hosts[host]['skipecount'] = self.hosts[host]['skiperrors']
                            self.hosts[host]['status'] = 1
                else:
                    self.hosts[host]['timecount'] -= 1

            time.sleep(1)

    def playerror(self, host=""):
        try:
            pygame.mixer.music.load(
                self.hosts[host]['media'])
            pygame.mixer.music.play()
        except:
            try:
                pygame.mixer.music.load("error.mp3")
                pygame.mixer.music.play()
            except:
                pass


if __name__ == "__main__":
    hosts = CONFIG
    ping = myping(hosts)
    for i in range(100):
        p = ping.get()
        print(p, ping.hosts)
        time.sleep(1)
    ping.stop()
