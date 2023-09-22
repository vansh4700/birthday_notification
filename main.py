import datetime
import json
import mysql.connector
from plyer import notification

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passkey=00',
    'database': 'devops',
}

# File to store birthdays data
BIRTHDAYS_FILE = 'birthdays.json'

# Function to load birthdays from a JSON file
def load_birthdays():
    try:
        with open(BIRTHDAYS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to schedule birthday notifications
def schedule_notifications():
    today = datetime.date.today()
    birthdays = load_birthdays()

    for birthday, name in birthdays.items():
        month, day = map(int, birthday.split())
        birthday_date = datetime.date(today.year, month, day)

        # Calculate the number of days until the birthday
        days_until_birthday = (birthday_date - today).days

        if days_until_birthday == 0:
            message = f"Today is {name}'s birthday! 🎉"
            notification.notify(
                title='Birthday Notification',
                message=message,
                app_name='Birthday Reminder',
                timeout=10,
            )

