## 사용한 opensource, 모듈
# tkinter 모듈
# datetime 모듈 (별다른 모듈설치가 필요없다고 하는데 확인필요!)

## Ubuntu20.04 기준 모듈 설치방법
# sudo apt-get install python3-tk

## 독창적인 부분
# 1. 단순히 터미널에서 실행하는 것이 아니라 채팅창을 만들어 사용자 편의성 증대
# 2. OpenAI.py 파일을 import하여 두 파이썬 파일을 연결

## 참조문헌
# https://076923.github.io/posts/Python-tkinter-1/ : 해당 홈페이지의 tkinter 강의 참조

## 제작방식
# 혼합(정주영)

## Start here (개발담당 : 정주영)
import storage
import tkinter
import datetime
from tkinter import font
from OpenAI import answer

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

def chatPNU(event = None):
    user_input = user_input_field.get()
    
    if '종료' in user_input :
        PNU_window.destroy()  # close window
        return

    chat_field.insert(tkinter.END, "나: " + user_input + "\n", "User_color")
    chat_field.insert(tkinter.END, "PNU챗봇: " + answer(user_input) + "\n")
    user_input_field.delete(0, tkinter.END)

    chat_field.see(tkinter.END)

# Setting GUI windows
PNU_window = tkinter.Tk()
PNU_window.title("부산대학교전용 PNU챗봇")

customFont = font.Font(size=20)

scrollbar = tkinter.Scrollbar(PNU_window)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

chat_field = tkinter.Text(PNU_window, height=15, width=50, font=customFont, yscrollcommand=scrollbar.set)
chat_field.pack()

chat_field.insert(tkinter.END, "PNU챗봇: " + answer("자기소개 해 줘!") + "\n")

notice = "* (식단정보) 오늘(" + f"{today}" + ")과 내일(" + f"{tomorrow}" + "일)이 아닌 다른날의 정보는 다를 수 있습니다."
message=tkinter.Message(PNU_window, text=notice, width=700)
message.pack()

chat_field.tag_config("User_color", foreground="blue")

scrollbar.config(command=chat_field.yview)

user_input_field = tkinter.Entry(PNU_window, width=50, font=customFont)
user_input_field.pack()
user_input_field.bind("<Return>", chatPNU)  # 엔터 키 이벤트 바인딩

send_button = tkinter.Button(PNU_window, text="전송", command=chatPNU)
send_button.pack()

PNU_window.mainloop()

## End here (개발담당 : 정주영)
