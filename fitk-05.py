from tkinter import *
from tkinter import filedialog, messagebox

def count_stats(filename):
    space_cnt = 0
    upper_cnt = 0
    lower_cnt = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            for ch in line:
                if ch == ' ':
                    space_cnt += 1
                elif ch.isupper():
                    upper_cnt += 1
                elif ch.islower():
                    lower_cnt += 1
    return space_cnt, upper_cnt, lower_cnt

def select_file():
    filepath = filedialog.askopenfilename(
        title="파일을 선택하세요",
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
    )
    if not filepath:   
        return
    try:
        space_cnt, upper_cnt, lower_cnt = count_stats(filepath)

        file_label.config(text=f"선택된 파일: {filepath}")
        result_label.config(text=f"스페이스: {space_cnt}, 대문자: {upper_cnt}, 소문자: {lower_cnt}")
    except Exception as e:
        messagebox.showerror("에러", f"파일을 처리하는 중 오류가 발생했습니다.\n{e}")


root = Tk()
root.title("문제5")
root.geometry("520x220")

Label(root, text="텍스트 파일을 선택하여 스페이스, 대문자, 소문자 개수를 세어보세요.").pack(pady=10)

Button(root, text="파일 선택", command=select_file).pack(pady=5)

file_label = Label(root, text="선택된 파일: (없음)")
file_label.pack(pady=5)

result_label = Label(root, text="스페이스: 0, 대문자: 0, 소문자: 0")
result_label.pack(pady=10)

root.mainloop()