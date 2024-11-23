from pyudev import Context, Monitor, MonitorObserver

from config import TARGET_VENDOR_ID, TARGET_PRODUCT_ID, MOUNT_POINT, FOLDER_ON_PC

from mount_manager import mount_iphone
from sync import sync_folders_with_merge


def device_event(device):
    """Обработчик событий подключения/отключения устройства."""
    action = device.action  # Действие (add/remove)
    
    if action == "add":
        vendor_id = device.get("ID_VENDOR_ID")
        product_id = device.get("ID_MODEL_ID")

        print(f"Подключено устройство: Vendor ID={vendor_id}, Product ID={product_id}")
        
        if vendor_id == TARGET_VENDOR_ID and product_id == TARGET_PRODUCT_ID:
            print("iPhone подключен!")
            mount_iphone()
            sync_folders_with_merge(f"{MOUNT_POINT}/test", FOLDER_ON_PC)
            # try:
                # sync_folders_with_merge(f"{MOUNT_POINT}/test", FOLDER_ON_PC)
            # except Exception as e:
            #     print(f"Ошибка при работе с iPhone: {e}")
            # finally:
            #     unmount_iphone()

if __name__ == "__main__":
    # Создаем контекст для отслеживания устройств
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by("usb")
    
    observer = MonitorObserver(monitor, callback=device_event, name="monitor-observer")
    observer.start()

    print("Ожидание подключения устройства...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        print("Завершение работы.")
