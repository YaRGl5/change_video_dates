import os
import re
import time
from datetime import datetime

# Укажи путь к папке с видеофайлами
folder_path = r"C:\Users\yaros\Downloads\google photo"  # Замени на свой путь

# Регулярные выражения для всех форматов имен файлов
patterns = [
    re.compile(r"VID_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})"),  # VID_YYYYMMDD_HHMMSS
    re.compile(r"VID_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})_HSR_\d+"),  # VID_YYYYMMDD_HHMMSS_HSR_120
    re.compile(r"video_(\d+)@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})"),  # video_X@DD-MM-YYYY_HH-MM-SS
    re.compile(r"video_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})"),  # video_YYYY-MM-DD_HH-MM-SS
    re.compile(r"Screenrecorder-(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-\d+"),  # Screenrecorder-YYYY-MM-DD-HH-MM-SS-XXX
    re.compile(r"(\d{4})-(\d{2})-(\d{2})-(\d{6})\d*"),  # YYYY-MM-DD-HHMMSSXXX
    re.compile(r"(\d{4})-(\d{2})-(\d{2}) (\d{2})-(\d{2})-(\d{2})"),  # YYYY-MM-DD HH-MM-SS
    re.compile(r"video_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})"),  # video_YYYY-MM-DD_HH-MM-SS
    re.compile(r"video_(\d+)@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})"),  # video_X@DD-MM-YYYY_HH-MM-SS
]

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    match = None
    for pattern in patterns:
        match = pattern.search(filename)
        if match:
            break

    if match:
        groups = match.groups()

        if len(groups) == 6:  # Формат: YYYYMMDD_HHMMSS или video_X@DD-MM-YYYY_HH-MM-SS
            year, month, day, hour, minute, second = groups
        elif len(groups) == 4:  # Формат: YYYY-MM-DD HHMMSSXXX
            date_part, time_part = groups[:3], groups[3]
            year, month, day = date_part
            hour, minute, second = time_part[:2], time_part[2:4], time_part[4:6]
        else:
            # Если групп меньше или больше, необходимо скорректировать
            print(f"Неправильное количество групп для файла: {filename}")
            continue

        new_date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        timestamp = time.mktime(datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S").timetuple())

        os.utime(file_path, (timestamp, timestamp))

        try:
            import ctypes
            handle = ctypes.windll.kernel32.CreateFileW(file_path, 256, 0, None, 3, 128, None)
            if handle != -1:
                ctypes.windll.kernel32.SetFileTime(handle, int(timestamp), int(timestamp), int(timestamp))
                ctypes.windll.kernel32.CloseHandle(handle)
        except Exception as e:
            print(f"Не удалось изменить дату создания для {filename}: {e}")

        print(f"Дата для {filename} изменена на {new_date}")
    else:
        print(f"Дата не найдена в названии {filename}")