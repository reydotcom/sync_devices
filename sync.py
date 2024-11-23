import os

import shutil
from difflib import unified_diff


def merge_files(file1, file2, output_file):
    """
    Склеивает два текстовых файла, добавляя различия в файл-результат.
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()

    # Используем unified_diff для определения различий
    merged_content = list(unified_diff(content1, content2, lineterm=''))

    # Записываем результат в выходной файл
    with open(output_file, 'w', encoding='utf-8') as output:
        output.writelines(merged_content)
    print(f"Merged conflict into: {output_file}")

def sync_folders_with_merge(from_folder, to_folder):
    def copy_file(src, dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(src, dest)
        print(f"Copied: {src} -> {dest}")

    def handle_conflict(file1, file2, dest):
        """
        Объединяет содержимое файлов в случае конфликта.
        """
        base_name = os.path.basename(file1)
        merged_file = os.path.join(dest, f"{base_name}")

        # Склеиваем файлы
        merge_files(file1, file2, merged_file)

    def sync_folder(from_folder, to_folder):
        for root, _, files in os.walk(from_folder):
            for file in files:
                src_file = os.path.join(root, file)
                relative_path = os.path.relpath(src_file, from_folder)
                dest_file = os.path.join(to_folder, relative_path)

                if not os.path.exists(dest_file):
                    # Если файл отсутствует, копируем
                    copy_file(src_file, dest_file)
                else:
                    # Если файл существует, проверяем на конфликт
                    src_time = os.path.getmtime(src_file)
                    dest_time = os.path.getmtime(dest_file)

                    if src_time > dest_time:
                        if os.path.getsize(src_file) != os.path.getsize(dest_file):
                            # Обнаружен конфликт
                            handle_conflict(src_file, dest_file, os.path.dirname(dest_file))
                        copy_file(src_file, dest_file)

    # Синхронизируем обе стороны
    sync_folder(from_folder, to_folder)
    print('Sync end')