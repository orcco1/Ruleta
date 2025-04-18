import random

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


if __name__ == "__main__":
    log_result()

