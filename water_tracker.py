import os
import json
from datetime import datetime, timedelta

LOG_FILE = "water_log.json"
DAILY_GOAL = 2000  #Default goal in ml

def initialize_db():
    """Ensure the water log file exists."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump({"history": []}, f)

def show_intro():
    """Explain why the user should use this app (Heuristic #1)."""
    print("\n💧 Welcome to the Water Tracker! 💧")
    print("=" * 50)
    print("Why use this?")
    print("- Stay hydrated and develop healthier habits.")
    print("- Easily track daily and weekly water intake.")
    print("- Visual progress keeps you motivated!")
    print("This tracker is simple, **private**, and quick to use.")
    print("=" * 50)

def show_potential_costs():
    """Reassure the user about potential costs (Heuristic #2)."""
    print("\n💡 What to Expect 💡")
    print("=" * 50)
    print("✅ **Quick & Simple:** Logging water takes just seconds.")
    print("✅ **Privacy-Friendly:** All data is stored **locally**.")
    print("✅ **No Overload:** Log water at your own pace—no pressure!")
    print("✅ **Minimal Effort:** Just a few clicks to track progress.")
    print("🚀 This tracker is here to help, not to add stress!")
    print("=" * 50)

def allow_data_control():
    print("Boosts Energy & Hydration – Prevents fatigue and keeps the body functioning efficiently.")
    print("Improves Skin & Joint Health – Promotes clearer skin and lubricates joints.")
    print("Aids Digestion & Metabolism – Prevents constipation and supports weight management.")
    print("Enhances Kidney & Heart Function – Flushes toxins and supports circulation.")
    print("Improves Focus & Mood – Reduces brain fog, stress, and headaches.")
    print("Regulates Body Temperature – Aids in sweating and overall body cooling.")
    print("Supports Long-Term Health – Lowers risks of UTIs, kidney stones, and chronic diseases.")


def log_water(amount):
    """Log water intake with reversible confirmation (Heuristic #5)."""
    confirm = input(f"Confirm logging {amount}ml? (y/n): ")
    if confirm.lower() == "y":
        with open(LOG_FILE, "r+") as f:
            data = json.load(f)
            today = datetime.now().strftime("%Y-%m-%d")
            data["history"].append({"date": today, "amount": amount})
            f.seek(0)
            json.dump(data, f)
        print(f"✅ {amount}ml logged!")
    else:
        print("❌ Action canceled.")

def display_progress():
    """Show a vertical progress bar (Heuristic #4)."""
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    total_intake = sum(entry["amount"] for entry in data["history"])
    percentage = min(100, (total_intake / DAILY_GOAL) * 100)
    filled = int(percentage / 5)  # Scale to terminal width

    print("\n💧 Daily Progress 💧")
    print("=" * 20)
    for i in range(20, -1, -1):
        print("|" + ("█" if i <= filled else " ")+"|")
    print("=" * 20)
    print(f"{total_intake}/{DAILY_GOAL}ml")

def display_progress_percent():
    """Show a percentage progress bar (Heuristic #4)."""
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    total_intake = sum(entry["amount"] for entry in data["history"])
    percentage = min(100, (total_intake / DAILY_GOAL) * 100)
    print(f"\n📈 Daily Progress: {percentage:.1f}%")


def start_new_day():
    """Start a new day (Heuristic #6)."""
    confirm = input("Start a new day? Previous data will be archived. (y/n): ")
    if confirm.lower() == "y":
        with open(LOG_FILE, "w") as f:
            json.dump({"history": []}, f)
        print("✅ New day started!")
    else:
        print("❌ Action canceled.")


def view_weekly_progress():
    """Show progress over multiple days (Heuristic #7)."""
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    today = datetime.now().date()  # Get today's date without time
    week_ago = today - timedelta(days=6)
    weekly_data = {today - timedelta(days=i): 0 for i in range(7)}

    for entry in data["history"]:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()  # Normalize entry date
        if week_ago <= entry_date <= today:
            weekly_data[entry_date] += entry["amount"]

    print("\n📊 Weekly Progress 📊")
    for date, amount in sorted(weekly_data.items()):
        print(f"{date.strftime('%Y-%m-%d')}: {amount}ml")


def main():
    """Main menu loop."""
    initialize_db()
    show_intro()
    show_potential_costs()

    while True:
        print("\nWater Tracker")
        print("1. Log More Water")
        print("2. View Water Progress")
        print("22. View Progress as Percentage")
        print("3. Start a New Day")
        print("4. View Weekly Progress")
        print("5. View Effects of Healthy Water Consumption")
        print("6. Exit")

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

        elif choice == "22":
            display_progress_percent()

        elif choice == "3":
            start_new_day()

        elif choice == "4":
            view_weekly_progress()

        elif choice == "5":
            allow_data_control()

        elif choice == "6":
            print("👋 Exiting. Stay hydrated!")
            break

        else:
            print("❌ Invalid choice. Please select again.")


if __name__ == "__main__":
    main()