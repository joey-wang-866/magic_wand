import os
import tkinter as tk
from tkinter import filedialog

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
                    if line.startswith('1'):
                        # 修改每行的開頭為 '2'
                        lines[i] = '2' + line[1:]
                        modified = True

                if modified:
                    file.seek(0)
                    file.writelines(lines)
                    file.truncate()  # 去除多餘的內容
                    modified_files.append(txt_file)

        except Exception as e:
            print(f"讀取檔案 {txt_file} 時發生錯誤: {e}")

    if modified_files:
        print("以下檔案的行開頭已被修改：")
        for modified_file in modified_files:
            print(modified_file)
    else:
        print("沒有檔案需要修改，或所有符合條件的行已被修正。")

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
