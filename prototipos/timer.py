import time

# Set the countdown time (in seconds)
countdown_time = 10

# Run the countdown
while countdown_time > 0:
    # Display the remaining time
    print(f"Time remaining: {countdown_time} seconds")

    # Sleep for 1 second
    time.sleep(1)

    # Decrement the countdown time
    countdown_time -= 1

# Display a message when the countdown is finished
print("Time's up!")
