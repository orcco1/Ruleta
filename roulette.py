import random
import os
import re
from collections import Counter
from datetime import datetime

# Roulette number colors
greens = [0]
reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Create a single list of all roulette numbers
roulette = greens + reds + blacks

def ensure_directories():
    """Ensure required directories exist"""
    os.makedirs("Logs", exist_ok=True)
    os.makedirs("analysis", exist_ok=True)

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
    ensure_directories()
    result = run_roulette()  # Call the function to get the result
    with open("Logs/log.txt", "a") as f:
        f.write(result + "\n")

def cleaner():
    if (os.path.exists("Logs/log.txt")):
        os.remove("Logs/log.txt")
    else:
        print("No logs to clean")

def save_analysis(filename, content):
    ensure_directories()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"analysis/{filename}", "a") as f:
        f.write(f"\n=== Analysis at {timestamp} ===\n")
        f.write(content + "\n")

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

    # Prepare analysis content
    analysis_content = f"Total spins: {total_spins}\n"
    analysis_content += f"\nMost common number: {most_common_num[0]} (appeared {most_common_num[1]} times)\n"

    analysis_content += "\nColor distribution:\n"
    for color, count in color_counts.items():
        percentage = (count / total_spins) * 100
        analysis_content += f"{color.capitalize()}: {count} spins ({percentage:.2f}%)\n"

    analysis_content += "\nNumber frequency (top 5):\n"
    for num, count in Counter(numbers).most_common(5):
        analysis_content += f"Number {num}: {count} times ({(count/total_spins)*100:.2f}%)\n"

    # Save to file
    save_analysis("general_analysis.txt", analysis_content)
    print("General analysis saved to analysis/general_analysis.txt")

def color_streak_analyzer():
    if not os.path.exists("Logs/log.txt"):
        print("No logs found.")
        return

    with open("Logs/log.txt", "r") as f:
        logs = f.readlines()

    if not logs:
        print("Empty log")
        return

    # Get colors
    colors = []
    pattern = r"Color: (\w+)"
    for entry in logs:
        match = re.search(pattern, entry.strip())
        if match:
            colors.append(match.group(1))

    # Analyze streaks
    current_streak = 1
    max_streaks = {"red": 0, "black": 0, "green": 0}
    current_color = colors[0]
    streaks = []

    for i in range(1, len(colors)):
        if colors[i] == current_color:
            current_streak += 1
        else:
            streaks.append((current_color, current_streak))
            if current_streak > max_streaks[current_color]:
                max_streaks[current_color] = current_streak
            current_color = colors[i]
            current_streak = 1

    # Add
    streaks.append((current_color, current_streak))
    if current_streak > max_streaks[current_color]:
        max_streaks[current_color] = current_streak

    # Top 3 longest streaks by color
    top_streaks = {"red": [], "black": [], "green": []}
    for color, length in streaks:
        if len(top_streaks[color]) < 3:
            top_streaks[color].append(length)
            top_streaks[color].sort(reverse=True)
        elif length > top_streaks[color][-1]:
            top_streaks[color].pop()
            top_streaks[color].append(length)
            top_streaks[color].sort(reverse=True)

    # Prepare analysis content
    analysis_content = f"Total runs analyzed: {len(colors)}\n"

    for color in ["red", "black", "green"]:
        analysis_content += f"\nColor {color.upper()}:\n"
        analysis_content += f"Max streak: {max_streaks[color]} consecutive runs\n"
        analysis_content += f"Top 3 streaks: {', '.join(map(str, top_streaks[color]))}\n"

        total_color = colors.count(color)
        streak_appearances = sum(1 for c, _ in streaks if c == color)
        if streak_appearances > 0:
            avg_streak = total_color / streak_appearances
            analysis_content += f"Avg streak: {avg_streak:.1f} runs\n"

    # Top 5 longest streaks of any color
    all_streaks = sorted(streaks, key=lambda x: x[1], reverse=True)[:5]
    analysis_content += "\nTop 5 longest streaks:\n"
    for i, (color, length) in enumerate(all_streaks, 1):
        analysis_content += f"{i}. {color.upper()}: {length} consecutive runs\n"

    # Save to file
    save_analysis("streak_analysis.txt", analysis_content)
    print("Streak analysis saved to analysis/streak_analysis.txt")

if __name__ == "__main__":
    ensure_directories()
    while True:
        print("\n1. Run roulette")
        print("2. Analyze results (general)")
        print("3. Analyze color streaks")
        print("4. Clean log")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
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
            color_streak_analyzer()

        elif choice == "4":
            print("Clean log...")
            cleaner()

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid option, please try again")
