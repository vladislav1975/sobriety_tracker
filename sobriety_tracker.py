# -------------------------------
# Sobriety Tracker Script
# -------------------------------
# This script helps users track how long they've been sober.
# It stores the start date in a file and calculates the time passed
# in years, months, and days using the dateutil library.
# -------------------------------

# Import standard libraries for date handling and file operations
from datetime import date, datetime  # 'date' for current date, 'datetime' for parsing strings
from calendar import monthrange      # Used to validate day input based on month/year
import os                            # Used to check if the save file exists
import json                          # Used to save and load the sobriety_tracker date
from json import JSONDecodeError     # Handles corrupted JSON files

# Import relativedelta for accurate date differences (years/months/days)
from dateutil.relativedelta import relativedelta

# File name where the sobriety_tracker start date will be saved
FNAME = "sobriety_start_date.json"

# Function to display error messages in a consistent format
def error(msg):
    print(f"❌ Error: {msg}")

# Function to get a valid integer input from the user
# Includes optional min/max validation and a quit option
def get_valid_int(prompt, min_val=None, max_val=None):
    while True:
        response = input(prompt)
        if response.lower() == 'q':  # Allow user to exit input
            print("👋 Exiting setup.")
            return None
        try:
            value = int(response)
            # Check if value is within the allowed range
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                error(f"Please enter a number between {min_val} and {max_val}.")
                continue
            return value
        except ValueError:
            error("Invalid input. Please enter a valid number.")

# Function to read the saved sobriety_tracker date from the JSON file
def read_saved_date():
    if os.path.exists(FNAME):
        try:
            with open(FNAME, 'r') as file:
                content = json.load(file)  # Load date string from file
                saved_date = datetime.strptime(content, '%Y-%m-%d').date()  # Convert to date object
                print(f"📅 Saved date: {saved_date.strftime('%A %d %B %Y')}")
                return saved_date
        except (ValueError, JSONDecodeError):
            # If the file is corrupted or unreadable, delete it and start fresh
            error("Corrupted file. Creating new...")
            os.remove(FNAME)
    else:
        print("📂 No saved date found.")
    return None

# Function to prompt the user to enter their sobriety_tracker start date
def prompt_for_date():
    while True:
        # Ask for year, month, and day with validation
        y = get_valid_int("Enter sobriety_tracker starting year (or 'q' to quit): ", 1900, date.today().year)
        if y is None:
            return None

        m = get_valid_int("Month (1–12): ", 1, 12)
        if m is None:
            return None

        # Get the maximum number of days in the selected month/year
        max_d = monthrange(y, m)[1]
        d = get_valid_int(f"Day (1–{max_d}): ", 1, max_d)
        if d is None:
            return None

        # Create a date object from the input
        start_date = date(y, m, d)

        # Prevent future dates
        if start_date > date.today():
            error("Date is in the future.")
            continue

        # Save the date to file in YYYY-MM-DD format
        with open(FNAME, 'w') as file:
            json.dump(start_date.strftime('%Y-%m-%d'), file)
        print(f"✅ Date saved: {start_date.strftime('%A %d %B %Y')}")
        return start_date

# Main function that runs the sobriety_tracker tracker
def main():
    # Try to load the saved date; if not found, prompt the user
    start_date = read_saved_date()
    if not start_date:
        start_date = prompt_for_date()

    if start_date:
        today = date.today()
        # Calculate total days sober
        days_sober = (today - start_date).days

        # Use relativedelta to get years, months, and days
        delta = relativedelta(today, start_date)

        # Display results
        print(f"\n🎉 You've been sober for {days_sober} day{'s' if days_sober != 1 else ''}, which is:")
        print(f"   🗓️ {delta.years} year{'s' if delta.years != 1 else ''}, "
              f"{delta.months} month{'s' if delta.months != 1 else ''}, "
              f"{delta.days} day{'s' if delta.days != 1 else ''}")

# Run the main function when the script is executed
if __name__ == '__main__':
    main()
