# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

def time_format(seconds):
    seconds_r = seconds - int(seconds)
    seconds = int(seconds)

    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = (seconds % 3600) % 60

    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{int(seconds_r * 1000):d}"
