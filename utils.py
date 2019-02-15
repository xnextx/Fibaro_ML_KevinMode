from datetime import datetime, timedelta


def timestamp_to_minutes_after_midnight(time):
    hours = time.hour
    minutes = time.minute
    return (hours * 60) + minutes


def mins_to_dhms(seconds):
    d = datetime(1, 1, 1) + timedelta(minutes=int(seconds))
    output = "{:02}:{:02}".format(d.hour, d.minute)
    return output
