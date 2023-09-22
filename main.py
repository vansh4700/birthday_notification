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
# Main function to add a birthday
def add_birthday():
    month = int(input("Enter the month (1-12): "))
    day = int(input("Enter the day (1-31): "))
    name = input("Enter the name: ")

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(**DB_CONFIG)
    cursor = db_connection.cursor()

    # Insert the birthday data into the table
    insert_query = "INSERT INTO birthday_data (first_name, middle_name, last_name, year, month, day, sms) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name, '', '', datetime.date.today().year, month, day, ''))

    db_connection.commit()
    db_connection.close()

    birthdays = load_birthdays()
    birthday_key = f'{month:02d} {day:02d}'
    birthdays[birthday_key] = name

    with open(BIRTHDAYS_FILE, 'w') as file:
        json.dump(birthdays, file)

    print("Birthday added successfully!")

if _name_ == "_main_":
    while True:
        choice = input("Enter '1' to add a birthday or '2' to check for upcoming birthdays (q to quit): ")

        if choice == '1':
            add_birthday()
        elif choice == '2':
            schedule_notifications()
        elif choice.lower() == 'q':
            break
