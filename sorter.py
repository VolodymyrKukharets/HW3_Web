import platform
import time
from pathlib import Path
import shutil
import os
from threading import Thread

# Словник розширень для кожного типу файлів
file_extensions = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown': '',
}


# Функція для переміщення файлу до відповідної категорії
def move_file(item, destination_path):
    file_extension = item.suffix
    for file_type, extensions in file_extensions.items():
        if file_extension[1:].upper() in extensions:
            destination_directory = Path(destination_path) / file_type
            destination_directory.mkdir(exist_ok=True)
            try:
                shutil.move(item, destination_directory / item.name)
            except PermissionError as e:
                print(f"Помилка при переміщенні файлу {item.name}: {e}")
            break
    else:
        destination_directory = Path(destination_path) / 'unknown'
        destination_directory.mkdir(exist_ok=True)
        try:
            shutil.move(item, destination_directory / item.name)
        except PermissionError as e:
            print(f"Помилка при переміщенні файлу {item.name}: {e}")



# Функція для обробки папки та її вмісту у окремому потоці
def process_directory(source_path, destination_path):
    source_directory = Path(source_path)
    for item in source_directory.iterdir():
        if item.is_file():
            move_file(item, destination_path)
        elif item.is_dir():
            if any(item.iterdir()):
                # Створюємо окремий потік для обробки цієї папки
                process_thread = Thread(target=process_directory, args=(item, destination_path))
                process_thread.start()
                process_thread.join()
            else:
                item.rmdir()


# Функція для рекурсивного видалення порожніх папок
def delete_empty_folders_recursive(directory):
    for item in directory.iterdir():
        if item.is_dir():
            delete_empty_folders_recursive(item)
            try:
                item.rmdir()
            except OSError:
                continue


def main():
    while True:
        print("1. Сортувати каталог")
        print("2. Вихід")
        choice = input("Введіть значення для вибору ")
        if choice == "1":
            source_path = input('Введіть повний шлях до вашого каталогу ')
            if platform.system() == "Windows" and len(source_path.split(":")[0]) > 1:
                current_directory = Path.cwd()
                source_path = current_directory / source_path

            source_directory = Path(source_path)
            if source_directory.exists() and source_directory.is_dir():
                print(f"Каталог '{source_path}' існує.")
                for file_type in file_extensions.keys():
                    destination_directory = source_directory / file_type
                    destination_directory.mkdir(exist_ok=True)

                # Створюємо окремий потік для обробки вихідного каталогу
                process_thread = Thread(target=process_directory, args=(source_path, source_path))
                process_thread.start()
                process_thread.join()

                delete_empty_folders_recursive(source_directory)
                print("Сортування завершено!")
            else:
                print(f"Каталог '{source_path}' не існує або це не каталог.")
        elif choice == "2":
            os.system('cls')
            break
        else:
            print('Некоректний вибір, спробуйте ще раз')
            time.sleep(2)
            os.system('cls')


if __name__ == '__main__':
    main()
