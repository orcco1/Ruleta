import random
import os
import re
from collections import Counter

# Roulette number colors
greens = [0]
reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Create a single list of all roulette numbers
roulette = greens + reds + blacks

def run_roulette():
    number = random.choice(roulette)

    # Determine the color
    if number in greens:
        color = "green"
    elif number in reds:
        color = "red"
    else:
        color = "black"

    result = (f"Number: {number}  Color: {color}")

    return result

def log_result():
    result = run_roulette()  # Call the function to get the result
    with open("Logs/log.txt", "a") as f:
        f.write(result + "\n")

def analyzer():
    # Check if log file exists
    if not os.path.exists("Logs/log.txt"):
        print("No log file found. Run the roulette first to generate data.")
        return

    # Read log file
    with open("Logs/log.txt", "r") as f:
        logs = f.readlines()

    if not logs:
        print("Log file is empty. No data to analyze.")
        return

    # Initialize counters
    numbers = []
    colors = []
    color_counts = {"red": 0, "black": 0, "green": 0}

    # Parse each log entry
    pattern = r"Number: (\d+)  Color: (\w+)"
    for entry in logs:
        match = re.match(pattern, entry.strip())
        if match:
            number, color = match.groups()
            numbers.append(int(number))
            colors.append(color)
            color_counts[color] += 1

    total_spins = len(numbers)

    if total_spins == 0:
        print("No valid data found in logs.")
        return

    # Calculate statistics
    most_common_num = Counter(numbers).most_common(1)[0]
    num_distribution = Counter(numbers)

    print("\n=== Roulette Statistics ===")
    print(f"Total spins: {total_spins}")
    print(f"\nMost common number: {most_common_num[0]} (appeared {most_common_num[1]} times)")

    print("\nColor distribution:")
    for color, count in color_counts.items():
        percentage = (count / total_spins) * 100
        print(f"{color.capitalize()}: {count} spins ({percentage:.2f}%)")

    print("\nNumber frequency (top 5):")
    for num, count in Counter(numbers).most_common(5):
        print(f"Number {num}: {count} times ({(count/total_spins)*100:.2f}%)")

if __name__ == "__main__":
    while True:
        print("\n1. Run roulette")
        print("2. Analyze results")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            # Your existing run code
            while True:
                try:
                    num_of_runs = int(input("Enter the number of runs (0 to cancel): "))
                    if num_of_runs == 0:
                        break
                    if num_of_runs < 0:
                        print("Please enter a positive number")
                        continue

                    for _ in range(num_of_runs):
                        log_result()
                    print(f"Completed {num_of_runs} runs.")
                    break
                except ValueError:
                    print("Please enter a valid number")

        elif choice == "2":
            analyzer()

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid option, please try again")
