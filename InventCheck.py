#Best to execute in linux terminal or VSC (as it uses a linux terminal for execution)
#so that the output shows the colours -- Just nicer for visual output

from multiprocessing import Process
import time
from Supplier import Currys, Amazon, Labels

#using to test simultaneous execution
# def test():
#     for i in range(0,100):
#         time.sleep(4)
#         print("test")


#Running simultaneously
if __name__=='__main__':
    #Initialising and loading data for shops
    currys = Currys('£', Labels(750, "FREE delivery available", ["Not available for delivery", "Sorry this item is out of stock"]))
    currys.loadData()
    amazon = Amazon('£', Labels(750, "In stock.", ["out of stock", "unavailable"]))
    amazon.loadData()


    p1 = Process(target=amazon.checkStock)
    p1.start()
    p2 = Process(target=currys.checkStock)
    p2.start()
    p1.join()
    p2.join() 