import time
import random



N = 10_000_000
TIME_LIMIT = 60

sorted_data = list(range(N))
unsorted_data = list(range(N))
random.shuffle(unsorted_data)


def generate_queries(num_queries):
    return [random.randint(0, N-1) for _ in range(num_queries)]


def linear_search(data, key):
    try:
        return data.index(key)
    except ValueError:
        return -1

def binary_search(data, key):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == key:
            return mid
        elif data[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def rank_query_sorted(data, rank):
    if 0 <= rank < len(data):
        return data[rank]
    return None


def execute_queries(data, queries, search_func, rank_func=None):
    count = 0
    start_time = time.time()
    for query in queries:
        if rank_func:
            rank = rank_func(data, query)
            if rank is not None:
                search_func(data, rank) 
        else:
            search_func(data, query)
        count += 1
        if time.time() - start_time > TIME_LIMIT:
            break
    return count


num_queries = 10000 
query_keys = generate_queries(num_queries)
query_ranks = generate_queries(num_queries)


print("Testing on Unsorted Data:")
unsorted_lookup_count = execute_queries(unsorted_data, query_keys, linear_search)
print(f"Number of queries executed on unsorted data: {unsorted_lookup_count}")

print("Testing on Sorted Data:")
sorted_lookup_count = execute_queries(sorted_data, query_keys, binary_search)
sorted_rank_count = execute_queries(sorted_data, query_ranks, linear_search, rank_query_sorted)
print(f"Number of queries executed for lookup on sorted data: {sorted_lookup_count}")
print(f"Number of queries executed for rank on sorted data: {sorted_rank_count}")
