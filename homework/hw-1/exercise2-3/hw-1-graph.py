import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def generate_random_list(sizeN, minValue, maxValue):
    """Generates a list of random integers and returns the execution time."""
    begin_time = time.perf_counter()
    result = [random.randint(minValue, maxValue) for _ in range(sizeN)]
    end_time = time.perf_counter()
    return end_time - begin_time

# Define test cases
test_cases = [
    (1000, 0, 2**8 - 1),
    (10000, 0, 2**8 - 1),
    (100000, 0, 2**8 - 1),
    (1000000, 0, 2**8 - 1),
    (1000, 0, 2**16 - 1),
    (10000, 0, 2**16 - 1),
    (100000, 0, 2**16 - 1),
    (1000000, 0, 2**16 - 1),
    (1000, 0, 2**32 - 1),
    (10000, 0, 2**32 - 1),
    (100000, 0, 2**32 - 1),
    (1000000, 0, 2**32 - 1),
    (1000, 0, 2**64 - 1),
    (10000, 0, 2**64 - 1),
    (100000, 0, 2**64 - 1),
    (1000000, 0, 2**64 - 1),
    (1000, -100, 100),
    (10000, -100, 100),
    (100000, -100, 100),
    (1000000, -100, 100),
    (1000, -10000, 10000),
    (10000, -10000, 10000),
    (100000, -10000, 10000),
    (1000000, -10000, 10000),
    (1000, -1000000000, 1000000000),
    (10000, -1000000000, 1000000000),
    (100000, -1000000000, 1000000000),
    (1000000, -1000000000, 1000000000),
]

# Store execution times
results = []
for sizeN, minValue, maxValue in test_cases:
    time_taken = generate_random_list(sizeN, minValue, maxValue)
    results.append((sizeN, minValue, maxValue, time_taken))

# Convert results to a DataFrame for easier viewing
df = pd.DataFrame(results, columns=['Input Size', 'Min Value', 'Max Value', 'Execution Time (seconds)'])
print(df)

# Plotting
plt.figure(figsize=(12, 8))

for (minValue, maxValue), group_df in df.groupby(['Min Value', 'Max Value']):
    plt.plot(group_df['Input Size'], group_df['Execution Time (seconds)'], 
             marker='o', label=f"Range {minValue} to {maxValue}")

plt.xlabel('Input Size (N)')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time vs. Input Size for Different Ranges')
plt.legend(title="Value Ranges")
plt.grid(True)
plt.xscale('log')  # Use logarithmic scale for better visualization
plt.yscale('log')  # Use logarithmic scale for better visualization
plt.show()
