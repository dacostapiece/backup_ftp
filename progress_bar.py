import subprocess
import time
import os
import timespeed

print("PROGRESS_BAR.PY")

#if script is run from command line, you'll see the outgoing process

def retrieve_parameters():
    # Read local_file_size from local_file_size.txt
    with open("local_file_size.txt", "r") as f:
        local_file_size = int(f.read().strip())

    # Read timespeed from timespeed.txt
    with open("timespeed.txt", "r") as f:
        timespeed = float(f.read().strip())

    # Calculate transfer_speed without capping
    transfer_speed = 10240 / timespeed

    # Print file upload information on separate lines
    print(f"\n")
    print(f"Local file size: {local_file_size} bytes")
    print(f"Transfer speed: {transfer_speed:.2f} bytes per second")

    # Calculate total_iterations
    total_iterations = int(local_file_size / transfer_speed)
    print("total_iterations: ",total_iterations)

    return total_iterations

def simple_progress_bar(iterations):
    for i in range(iterations + 1):
        progress = i / iterations
        bar_length = 40
        bar = "[" + "=" * int(progress * bar_length) + " " * (bar_length - int(progress * bar_length)) + "]"
        percentage = int(progress * 100)
        print(f"Progress: {percentage}% {bar}", end="\r")
        time.sleep(0.1)  # Simulate work during each iteration (replace with actual work)
