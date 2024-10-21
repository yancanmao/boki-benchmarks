import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Define the base directories for Boki and Beldi experiments
boki_results_dir = '/home/ubuntu/boki-benchmarks/experiments/workflow/boki-hotel/results'   # Change this to the Boki path
# boki_results_dir = '/home/ubuntu/boki-benchmarks/experiments/workflow/boki-movie/results'   # Change this to the Boki path
beldi_results_dir = '/home/ubuntu/boki-benchmarks/experiments/workflow/beldi-hotel/results' # Change this to the Beldi path
# beldi_results_dir = '/home/ubuntu/boki-benchmarks/experiments/workflow/beldi-movie/results' # Change this to the Beldi path

QPS_VALUES = [5000, 6000, 7000, 8000]


qps_values = []
boki_p50_latencies = []
boki_p99_latencies = []
beldi_p50_latencies = []
beldi_p99_latencies = []

# Regex pattern to extract latency values
latency_regex = re.compile(r"p50 latency: ([\d.]+) ms\np99 latency: ([\d.]+) ms")

# Function to extract latency data from a given base directory
def extract_latencies_from_folder(folder_path):
    qps_latencies = {}
    for qps in QPS_VALUES:
        qps_folder = f"qps{qps}"
        latency_file = os.path.join(folder_path, qps_folder, "latency.txt")
        if os.path.exists(latency_file):
            with open(latency_file, "r") as f:
                content = f.read()
                match = re.search(latency_regex, content)
                if match:
                    p50_latency = float(match.group(1))
                    p99_latency = float(match.group(2))
                    qps_value = int(qps_folder.replace("qps", ""))
                    qps_latencies[qps_value] = (p50_latency, p99_latency)
    return qps_latencies

# Extract latencies for both Boki and Beldi
boki_latencies = extract_latencies_from_folder(boki_results_dir)
beldi_latencies = extract_latencies_from_folder(beldi_results_dir)

# Create a DataFrame to hold the data
data = {
    "QPS": sorted(boki_latencies.keys()),
    "Boki_p50 (ms)": [boki_latencies[qps][0] for qps in sorted(boki_latencies.keys())],
    "Boki_p99 (ms)": [boki_latencies[qps][1] for qps in sorted(boki_latencies.keys())],
    "Beldi_p50 (ms)": [beldi_latencies[qps][0] for qps in sorted(beldi_latencies.keys())],
    "Beldi_p99 (ms)": [beldi_latencies[qps][1] for qps in sorted(beldi_latencies.keys())],
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("latency_comparison_boki_beldi.csv", index=False)

# # Plotting the comparison of p50 and p99 latencies for both Boki and Beldi
# plt.figure(figsize=(10, 6))

# # p50 latencies
# plt.plot(df["QPS"], df["Boki_p50"], label="Boki p50", marker="o")
# plt.plot(df["QPS"], df["Beldi_p50"], label="Beldi p50", marker="o")

# # p99 latencies
# plt.plot(df["QPS"], df["Boki_p99"], label="Boki p99", marker="o")
# plt.plot(df["QPS"], df["Beldi_p99"], label="Beldi p99", marker="o")

# # Add labels and legend
# plt.xlabel("QPS")
# plt.ylabel("Latency (ms)")
# plt.title("Latency Comparison Between Boki and Beldi")
# plt.legend()

# # Show the plot
# plt.grid(True)
# plt.tight_layout()
# plt.show()
