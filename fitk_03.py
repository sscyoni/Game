file1 = input("첫 번째 파일명을 입력하세요: ").strip()
file2 = input("두 번째 파일명을 입력하세요: ").strip()
outfile = input("저장할 새 파일명을 입력하세요: ").strip()

try:
    # 첫 번째 파일 읽기
    with open(file1, "r", encoding="utf-8") as f1:
        data1 = f1.read()

    # 두 번째 파일 읽기
    with open(file2, "r", encoding="utf-8") as f2:
        data2 = f2.read()

    # 새로운 파일로 합쳐서 저장
    with open(outfile, "w", encoding="utf-8") as out:
        out.write(data1 + "\n" + data2)

    print(f"파일 병합이 완료되었습니다! → {outfile}")

except FileNotFoundError:
    print("입력한 파일 중 하나를 찾을 수 없습니다.")
