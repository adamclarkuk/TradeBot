from daemon import Daemon
import os
import hitbtc

class Trabebot(Daemon):

    def run(self):
        bot = hitbtc.HitBTC("test")


if __name__ == "__main__":

    process = Trabebot('/tmp/tbotpid.pid')
    process.start()





