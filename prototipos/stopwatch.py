"""
This code will print out the elapsed time in seconds, with two decimal places of precision, every second. To stop the stopwatch, you can press CTRL+C to interrupt the program.
"""


import time

# Set the start time
start_time = time.time()

# Run the stopwatch
while True:
    # Get the elapsed time
    elapsed_time = time.time() - start_time

    # Print the elapsed time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    # Sleep for 1 second
    time.sleep(1)
