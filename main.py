from batch_data import Rockwell
from continuous_data import ComtinuousData
def hello_world():
    rl = Rockwell()
    rl.start()
    cd=ComtinuousData()
    cd.start()
    return 'Hello World'

if __name__ == '__main__':
    hello_world()


