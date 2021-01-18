#Best to execute in linux terminal or VSC (as it uses a linux terminal for execution)
#so that the output shows the colours -- Just nicer for visual output

from AmazonUK import checkAmazonUKStock
from Currys import checkCurrysStock
from multiprocessing import Process
import time

#using to test simultaneous execution
def test():
    for i in range(0,100):
        time.sleep(4)
        print("test")


#Running simultaneously
if __name__=='__main__':
    p1 = Process(target=checkAmazonUKStock)
    p1.start()
    p2 = Process(target=checkCurrysStock)
    p2.start()
    p1.join()
    p2.join() 