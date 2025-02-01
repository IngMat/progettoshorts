import datetime as dt


def publish_time(week_day):
    # Calculates the scheduled publishing time for a video on a given weekday.
    now = dt.datetime.now()
    days_shift = (6 + week_day) - now.weekday()
    now = now + dt.timedelta(days=days_shift)
    now = now.replace(hour=17, minute=0, second=0)
    now = str(now)
    now = now.replace(" ", "T")
    now = now.split(".")
    publish_at = now[0] + "Z"
    print("The video will be published at " + publish_at)
    return publish_at
