# sudo apt-get install python3-tk (Ubuntu20.04)
# sudo pip3 install openai==0.28
# sudo pip3 install folium
# sudo pip3 install googlemaps
# sudo pip3 install lxml
# sudo pip3 install beautifulsoup4 (확인필요)

import tkinter as tk
from OpenAI import answer
from tkinter import font

# 챗봇 응답 함수
def respond_to_user(event=None):
    user_input = user_input_field.get()
    
    if user_input.lower() == "종료" or user_input.lower() == "종료 ":  # 사용자가 '취소'를 입력한 경우
        root.destroy()  # 창을 닫음
        return

    chat_history.insert(tk.END, "나: " + user_input + "\n")
    chat_history.insert(tk.END, "ChatPNU: " + answer(user_input) + "\n")
    user_input_field.delete(0, tk.END)

    chat_history.see(tk.END)

# GUI 생성
root = tk.Tk()
root.title("챗봇 인터페이스")

# 폰트설정
customFont = font.Font(family="Helvetica", size=20)

# 대화 영역 스크롤바 설정
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 대화 영역
chat_history = tk.Text(root, height=15, width=50, font=customFont, yscrollcommand=scrollbar.set)
chat_history.pack()

# 스크롤바와 텍스트 위젯 연결
scrollbar.config(command=chat_history.yview)

# 입력 필드
user_input_field = tk.Entry(root, width=50, font=customFont)
user_input_field.pack()
user_input_field.bind("<Return>", respond_to_user)  # 엔터 키 이벤트 바인딩

# 전송 버튼
send_button = tk.Button(root, text="전송", command=respond_to_user)
send_button.pack()



# 메인 루프 시작
root.mainloop()
