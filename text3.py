import os
import tkinter as tk
from tkinter import filedialog

delete_num = 10  # 要刪除包含該數字的行

def delete_lines_with_specific_number(directory):
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    modified_files = []

    for txt_file in txt_files:
        file_path = os.path.join(directory, txt_file)
        try:
            with open(file_path, 'r+', encoding='utf-8') as file:
                lines = file.readlines()
                modified = False

                # 篩選並刪除包含特定數字的行
                new_lines = [line for line in lines if str(delete_num) not in line]

                # 如果有行被刪除，寫回檔案
                if len(new_lines) != len(lines):
                    modified = True
                    file.seek(0)
                    file.writelines(new_lines)
                    file.truncate()  # 去除多餘的內容
                    modified_files.append(txt_file)

        except Exception as e:
            print(f"讀取檔案 {txt_file} 時發生錯誤: {e}")

    if modified_files:
        print(f"以下檔案有行被刪除：")
        for modified_file in modified_files:
            print(modified_file)
    else:
        print(f"沒有檔案被修改或刪除。")

def select_folder():
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    folder_selected = filedialog.askdirectory()  # 開啟資料夾選擇對話框
    return folder_selected

if __name__ == "__main__":
    folder_path = select_folder()
    if folder_path:
        delete_lines_with_specific_number(folder_path)
    else:
        print("未選擇任何資料夾。")
