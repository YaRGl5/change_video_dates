import os
import re
import time
from datetime import datetime

# Папка с видеофайлами
folder_path = r"C:\Users\yaros\Downloads\google photo"  # Укажи свой путь

# Возможные форматы дат в названии файла
patterns = [
    re.compile(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})"),  # YYYY-MM-DD_HH-MM-SS
    re.compile(r"(\d{8})_(\d{6})"),  # YYYYMMDD_HHMMSS (без разделителей)
    re.compile(r"(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})"),  # DD-MM-YYYY_HH-MM-SS
    re.compile(r"(\d{4})-(\d{2})-(\d{2}) (\d{2})-(\d{2})-(\d{2})")  # YYYY-MM-DD HH-MM-SS
]

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Перебираем все возможные форматы
    match = None
    for pattern in patterns:
        match = pattern.search(filename)
        if match:
            break  # Если нашли дату, останавливаемся

    if match:
        groups = match.groups()
        if len(groups) == 6:  # Полный формат YYYY-MM-DD_HH-MM-SS или DD-MM-YYYY_HH-MM-SS
            year, month, day, hour, minute, second = groups
        elif len(groups) == 2:  # Формат YYYYMMDD_HHMMSS
            date_part, time_part = groups
            year, month, day = date_part[:4], date_part[4:6], date_part[6:8]
            hour, minute, second = time_part[:2], time_part[2:4], time_part[4:6]

        new_date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        timestamp = time.mktime(datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S").timetuple())

        # Изменяем дату создания и последнего изменения
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