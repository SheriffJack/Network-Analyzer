import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("network_log.csv", header=None)

data.columns = ["Time", "Size_MB", "Duration_sec", "Speed_MBps"]

print("\nAverage Speed:", data["Speed_MBps"].mean())

busiest = data.loc[data["Speed_MBps"].idxmin()]

print("Most congested hour:", busiest["Time"])


plt.plot(data["Time"], data["Speed_MBps"], marker='o')

plt.xlabel("Hour")

plt.ylabel("Speed (MB/s)")

plt.title("Network Throughput Over Time")

plt.xticks(rotation=45)

plt.grid()

plt.show()