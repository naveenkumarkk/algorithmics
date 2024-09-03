import random
import time

def generateRandomList(sizeN,minValue,maxValue):

    beginingOfCounter = time.perf_counter()
    result = [random.randint(minValue, maxValue) for _ in range(sizeN)]
    endCounter= time.perf_counter()
    print(f"Time difference: {endCounter - beginingOfCounter:0.4f} seconds")



generateRandomList(1000,0,2**8-1)
generateRandomList(10000,0,2**8-1)
generateRandomList(100000,0,2**8-1)
generateRandomList(1000000,0,2**8-1)
generateRandomList(1000,0,2**16-1)
generateRandomList(10000,0,2**16-1)
generateRandomList(100000,0,2**16-1)
generateRandomList(1000000,0,2**16-1)
generateRandomList(1000,0,2**32-1)
generateRandomList(10000,0,2**32-1)
generateRandomList(100000,0,2**32-1)
generateRandomList(1000000,0,2**32-1)
generateRandomList(1000,0,2**64-1)
generateRandomList(10000,0,2**64-1)
generateRandomList(100000,0,2**64-1)
generateRandomList(1000000,0,2**64-1)
generateRandomList(1000,-100,100)
generateRandomList(10000,-100,100)
generateRandomList(100000,-100,100)
generateRandomList(1000000,-100,100)
generateRandomList(1000,-10000,10000)
generateRandomList(10000,-10000,10000)
generateRandomList(100000,-10000,10000)
generateRandomList(1000000,-10000,10000)
generateRandomList(1000,-1000000000,1000000000)
generateRandomList(10000,-1000000000,1000000000)
generateRandomList(100000,-1000000000,1000000000)
generateRandomList(1000000,-1000000000,1000000000)
