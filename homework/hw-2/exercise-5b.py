import numpy as np
import matplotlib.pyplot as plt

data = np.random.randint(0, 10000, size=1000)

def quickselect(arr, left, right, k):
    if left == right:
        return arr[left]
    
    pivot_index = np.random.randint(left, right + 1)
    pivot_index = partition(arr, left, right, pivot_index)
    
    if k == pivot_index:
        return arr[k]
    elif k < pivot_index:
        return quickselect(arr, left, pivot_index - 1, k)
    else:
        return quickselect(arr, pivot_index + 1, right, k)
    
def partition(arr, left, right, pivot_index):
    pivot_value = arr[pivot_index]
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
    store_index = left
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[store_index], arr[i] = arr[i], arr[store_index]
            store_index += 1
    arr[right], arr[store_index] = arr[store_index], arr[right]
    return store_index


data_snapshots = [data.copy()]

num_queries = 50

for _ in range(num_queries):
    k = np.random.randint(0, len(data)) 
    quickselect(data, 0, len(data) - 1, k)
    data_snapshots.append(data.copy())

plt.figure(figsize=(14, 7))
plt.plot(data_snapshots[0], label='Initial Random Data', color='blue', alpha=0.5)
plt.plot(data_snapshots[-1], label='Final Data After Queries', color='red', alpha=0.5)

plt.title('Visualization of Data Evolution with Quickselect')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.show()
plt.figure(figsize=(14, 7))

