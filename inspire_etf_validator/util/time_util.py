import time


def to_datetime(datetime):
    return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(datetime))


def to_filename_datetime(datetime):
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(datetime))


def time_now():
    return time.time()


def to_duration(old_time, new_time):
    duration = new_time - old_time

    hours = duration // 3600
    minutes = duration // 60 % 60
    seconds = duration % 60

    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
