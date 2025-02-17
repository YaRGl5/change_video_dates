import os
import re
import time
from datetime import datetime

# Папка с видеофайлами
folder_path = r"C:\Users\yaros\Downloads\google photo"  # Укажи свой путь

# Регулярное выражение для поиска даты и времени в названии файла
date_pattern = re.compile(r"video_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})")

for filename in os.listdir(folder_path):
    match = date_pattern.search(filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        new_date = f"{year}-{month}-{day} {hour}:{minute}:{second}"

        # Конвертация в timestamp
        timestamp = time.mktime(datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S").timetuple())

        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        # Изменяем дату изменения и последнего доступа
        os.utime(file_path, (timestamp, timestamp))  

        try:
            import ctypes
            ctime = datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S").timestamp()
            handle = ctypes.windll.kernel32.CreateFileW(file_path, 256, 0, None, 3, 128, None)
            if handle != -1:
                ctypes.windll.kernel32.SetFileTime(handle, int(ctime), int(ctime), int(ctime))
                ctypes.windll.kernel32.CloseHandle(handle)
        except Exception as e:
            print(f"Не удалось изменить дату создания для {filename}: {e}")

        print(f"Дата для {filename} изменена на {new_date}")
    else:
        print(f"Дата не найдена в названии {filename}")