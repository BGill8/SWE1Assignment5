import sqlite3
from datetime import date

# Constants
DAILY_GOAL = 2000  # Daily goal in ml
BAR_HEIGHT = 10  # Height of the vertical progress bar
DB_FILE = "water_tracker.db"


def initialize_db():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            amount_ml INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def log_water(amount):
    """Log water intake."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO water_log (log_date, amount_ml) VALUES (?, ?)", (date.today(), amount))
    conn.commit()
    conn.close()
    print(f"\n✅ Logged {amount}ml of water.")


def get_today_water():
    """Retrieve total water intake for today."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount_ml) FROM water_log WHERE log_date = ?", (date.today(),))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0


def display_progress():
    """Display a vertical progress bar in the terminal."""
    total_water = get_today_water()
    progress = int((total_water / DAILY_GOAL) * BAR_HEIGHT)

    print("\nWater Intake Progress")
    print("-" * 22)

    for i in range(BAR_HEIGHT, 0, -1):
        if progress >= i:
            print("|██|")  # Full block
        else:
            print("|  |")  # Empty block

    print(f" {total_water}ml / {DAILY_GOAL}ml\n")


def main():
    """Main menu loop."""
    initialize_db()

    while True:
        print("\nWater Tracker")
        print("1. Log More Water")
        print("2. View Water Progress")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            try:
                amount = int(input("Enter water amount (ml): "))
                if amount > 0:
                    log_water(amount)
                else:
                    print("❌ Please enter a positive number.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

        elif choice == "2":
            display_progress()

        elif choice == "3":
            print("👋 Exiting. Stay hydrated!")
            break

        else:
            print("❌ Invalid choice. Please select again.")


if __name__ == "__main__":
    main()
