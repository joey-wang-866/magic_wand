"""修改每一行為同一數字"""

import os
import tkinter as tk
from tkinter import filedialog

change_num = 6


def check_and_fix_first_digit_in_all_lines(directory):
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    modified_files = []

    for txt_file in txt_files:
        file_path = os.path.join(directory, txt_file)
        try:
            with open(file_path, 'r+', encoding='utf-8') as file:
                lines = file.readlines()
                modified = False

                for i, line in enumerate(lines):
                    if line and line[0].isdigit() and line[0] != str(change_num):
                        # 修改每行的開頭為 '0'
                        lines[i] = str(change_num) + line[1:]
                        modified = True
                    elif line and not line[0].isdigit():
                        print(f"檔案 {txt_file} 的第 {i + 1} 行開頭不是數字，無法修正。")

                if modified:
                    file.seek(0)
                    file.writelines(lines)
                    file.truncate()  # 去除多餘的內容
                    modified_files.append(txt_file)

        except Exception as e:
            print(f"讀取檔案 {txt_file} 時發生錯誤: {e}")

    if modified_files:
        print(f"以下檔案的行開頭已被修改為 {str(change_num)}：")
        for modified_file in modified_files:
            print(modified_file)
    else:
        print(f"所有檔案的行開頭都已經是數字 {str(change_num)}，或沒有可修正的檔案。")


def select_folder():
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    folder_selected = filedialog.askdirectory()  # 開啟資料夾選擇對話框
    return folder_selected


if __name__ == "__main__":
    folder_path = select_folder()
    if folder_path:
        check_and_fix_first_digit_in_all_lines(folder_path)
    else:
        print("未選擇任何資料夾。")
