import random
import time

def generateSortedRandomList(sizeN,minValue,maxValue):

    result = [random.randint(minValue, maxValue) for _ in range(sizeN)]
    beginingOfCounter = time.perf_counter()
    sorted(result)
    endCounter= time.perf_counter()
    print(f"Time difference: {endCounter - beginingOfCounter:0.4f} seconds")


generateSortedRandomList(80000000,0,2**64-1)