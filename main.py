from app import *
import os
import topgg


if os.name != 'nt':
    import uvloop
    uvloop.install()


bot = Bot()



if __name__ == '__main__':
    bot.run()
