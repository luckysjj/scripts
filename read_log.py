#!/usr/bin/env python3
import sys
from pathlib import Path
import re
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def parse_log_file(file_path):
    # Dictionary to hold the total time and count for each function
    timings = defaultdict(lambda: {'total_time': 0.0, 'count': 0, 'max_time': float('-inf'), 'min_time': float('inf')})

    # Regex pattern to match the log lines
    pattern = re.compile(r'(?P<function>[\w\s]+) takes : (?P<time>\d+\.\d+)ms')
    
    # Read the log file
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                function_name = match.group('function').strip()
                time_taken = float(match.group('time'))
                # Update the total time and count for the function
                timings[function_name]['total_time'] += time_taken
                timings[function_name]['count'] += 1
                timings[function_name]['max_time'] = max(timings[function_name]['max_time'], time_taken)
                timings[function_name]['min_time'] = min(timings[function_name]['min_time'], time_taken)
    
    # Calculate the average time for each function
    for func in timings:
        timings[func]['average_time'] = timings[func]['total_time'] / timings[func]['count']

    return timings

def print_averages(file_name, timings_origin, timings_optimized):
    print(f"**************{file_name}:******************")

    all_functions = set(timings_origin.keys()).union(set(timings_optimized.keys()))
    for function in sorted(all_functions):
        orig_stats = timings_origin.get(function, {'average_time': 0, 'total_time': 0, 'count': 0, 'min_time': 0, 'max_time': 0})
        opt_stats = timings_optimized.get(function, {'average_time': 0, 'total_time': 0, 'count': 0, 'min_time': 0, 'max_time': 0})
        print(f"{function}:")
        print(f"  Original - Average time: {orig_stats['average_time']:.6f} ms, Total time: {orig_stats['total_time']:.6f} ms, Count: {orig_stats['count']}, Min time: {orig_stats['min_time']:.6f} ms, Max time: {orig_stats['max_time']:.6f} ms")
        print(f"  Optimized - Average time: {opt_stats['average_time']:.6f} ms, Total time: {opt_stats['total_time']:.6f} ms, Count: {opt_stats['count']}, Min time: {opt_stats['min_time']:.6f} ms, Max time: {opt_stats['max_time']:.6f} ms")

def visualize_averages(directory, file_name, timings_origin, timings_optimized):
    # Prepare the data for plotting
    data = []
    for function in timings_origin:
        if function != "slam process":
            data.append({'function': function, 'average_time': timings_origin[function]['average_time'], 'log': 'Original'})
    for function in timings_optimized:
        if function != "slam process":
            data.append({'function': function, 'average_time': timings_optimized[function]['average_time'], 'log': 'Optimized'})

    # Create DataFrame
    df = pd.DataFrame(data)

    if df.empty:
        print("No data available for plotting.")
        return

    # Plot
    sns.set_style('whitegrid')
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='function', y='average_time', hue='log', data=df)
    plt.title('Average Execution Time Comparison')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Annotate each bar with the average time value
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  # Only annotate bars with non-zero height
            ax.annotate(f'{height:.2f}ms',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom')

    # Save the plot
    save_path = Path(directory) / "Performance" / f"{file_name}_average_time_comparison.png"
    plt.savefig(save_path)
    plt.close()  # Close the plot to free up memory

def main(directory):
    # Ensure that the input is a Path object
    directory = Path(directory)

    # Subdirectories for original and optimized logs
    original_dir = directory / "Performance/original"
    optimized_dir = directory / "Performance/optimized"

    # Check if directories exist
    if not original_dir.exists() or not optimized_dir.exists():
        print(f"Missing 'original' or 'optimized' directories in {directory}")
        return

    # Iterate through original log files
    for original_log in original_dir.iterdir():
        if original_log.is_file() and original_log.suffix == '.txt':
            # Extract base file name by removing '_original_log' and '.txt'
            file_name = original_log.stem.replace('_log', '')
            # Corresponding optimized log path
            optimized_log = optimized_dir / f"{file_name}_log.txt"

            # Check if the corresponding optimized log exists
            if optimized_log.exists():
                # Process each pair of log files
                timings_origin = parse_log_file(original_log)
                timings_optimized = parse_log_file(optimized_log)
                print_averages(file_name, timings_origin, timings_optimized)
                visualize_averages(directory, file_name, timings_origin, timings_optimized)
            else:
                print(f"Optimized log for '{file_name}' does not exist.")
        else:
            print(f"Skipping non-text file or directory: {original_log}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: script.py <directory>")

