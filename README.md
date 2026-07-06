# GuessVerse

GuessVerse is a Random Number Guessing Game built using Python, NumPy, and Streamlit. The game offers multiple difficulty levels, a smart hint system, and an interactive user interface.

## Features

- Three difficulty levels: Easy, Medium, and Hard
- Smart hint system
- Input validation
- Personalized welcome screen
- Win/Lose messages
- Attempt counter
- Interactive user interface built with Streamlit

## Technologies Used

- Python
- NumPy
- Streamlit

## Difficulty Levels

### Easy
- Number Range: 1–30
- Attempts: 8
- Hint becomes available when 3 attempts remain.

### Medium
- Number Range: 1–70
- Attempts: 6
- Hint becomes available when 2 attempts remain.

### Hard
- Number Range: 1–100
- Attempts: 5
- Hint becomes available on the last attempt.

## Hint System
Hints become available based on the selected difficulty level:

- Easy: Hint is available when 3 attempts remain.
- Medium: Hint is available when 2 attempts remain.
- Hard: Hint is available on the last attempt.

The game provides helpful hints such as:
- The number lies between a specific range (e.g., 1–10, 11–20, etc.).
- The number is divisible by 2.
- The number is divisible by 3.
- The number is divisible by 5.

These hints help the player narrow down the possible number while keeping the game challenging.

## Author
Muskan Paul
