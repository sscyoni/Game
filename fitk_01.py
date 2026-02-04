try :
    a = input("텍스트 파일을 입력하세요:")
    infile = open (a,"r",encoding="utf-8")
    s= infile.read()
    print(s)
    infile.close()
except FileNotFoundError :
    print("파일을 찾지 못했습니다")