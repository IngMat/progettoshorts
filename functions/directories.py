import os
import datetime as dt


def weekly_directory(path):
    today = dt.datetime.now()  # get the current date
    days_shift = 7 - today.weekday() # calculate days until next monday
    next_monday = today + dt.timedelta(days=days_shift)
    next_sunday = next_monday + dt.timedelta(days=6)

    # Format the dates into a valid format for folder names
    monday_str = next_monday.strftime('%Y-%m-%d')
    sunday_str = next_sunday.strftime('%Y-%m-%d')

    folder_name = f'PostsDal{monday_str}al{sunday_str}'  # create the folder name
    folder_path = os.path.join(path, folder_name)  # create the full folder path
    os.makedirs(folder_path, exist_ok=True)  # create the folder
    return folder_path


def daily_directory(day_number, base_path):
    days_of_week = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}

    today = dt.datetime.now()
    days_shift = (6 + day_number) - today.weekday()  # calculate the target day offset
    target_day = today + dt.timedelta(days=days_shift)

    day_str = target_day.strftime('%Y-%m-%d')  # Format the date into a valid format for folder names

    folder_name = f'PostDi{days_of_week[day_number]}{day_str}'  # create the folder name
    folder_path = os.path.join(base_path, folder_name)  # create the full folder path
    os.makedirs(folder_path, exist_ok=True)  # create the folder
    return folder_path


def check_upper_directory(name):
    # Ensures the existance of a specific parent directory
    parent_dir = os.path.dirname(os.getcwd())
    directory_path = os.path.join(parent_dir, name)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    return directory_path
