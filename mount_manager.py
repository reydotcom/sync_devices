import os
import time

from config import MOUNT_POINT


def mount_iphone():
    """Монтирует iPhone в локальную папку."""
    try:
        # Проверяем, существует ли точка монтирования
        if not os.path.exists(MOUNT_POINT):
            os.makedirs(MOUNT_POINT)
        
        print("Монтирование iPhone...")

        time.sleep(1)
        os.system('ifuse ./iphone --documents md.obsidian')

        print(f"iPhone смонтирован в {MOUNT_POINT}")
    except Exception as e:
        print(f"Ошибка при монтировании iPhone: {e}")

def unmount_iphone():
    """Размонтирует iPhone."""
    try:
        print("Размонтирование iPhone...")
        time.sleep(1)
        os.system(f"fusermount -u {MOUNT_POINT}")
        print("iPhone размонтирован.")
    except Exception as e:
        print(f"Ошибка при размонтировании iPhone: {e}")