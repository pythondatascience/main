# pip install openai 를 해야합니다.
# 사용하고 싶으면 카톡에 있는 api key를 5번째 줄 API_KEY부분에 그대로 복붙
# 파일 위치에 PDSPrompt.txt라는 이름의 파일이 있어야 동작 (아무내용 없이 그냥 만들기만 해도 됩니다.)

import openai
#import bus_track
import subprocess

openai.api_key = "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"
hidden_bus_key = "31qwef#fAWedf#fFsfdew" #버스 위치에 관한 답변을 받을때만을 판별

def user_input():
    text = input("질문하세요 : ")
    answer(text)

def answer(user_content):
    messages.append({"role" : "user", "content" : f"{user_content}"})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,  # 클수록 자유도가 높다.
        max_tokens=256  # 클수록 말이 많다.
    )

    assistant_content = completion.choices[0].message["content"].strip()
    
     # 사용자가 버스 위치에 관한 질문을 했을 때만 bus_track.py 실행
    if hidden_bus_key in assistant_content:          
        print('\n'.join(assistant_content.split('\n')[:-1]))
        execute_bus_track()
        messages.append({"role": "assistant", "content": assistant_content})
    
    else:
        print(assistant_content)
        messages.append({"role": "assistant", "content": assistant_content})    

    user_input()

def execute_bus_track():
    # subprocess를 사용하여 bus_track.py 프로그램 실행
    result = subprocess.run(["python", "bus_track.py"], capture_output=True, text=True)
    print(result.stdout)

prompt_list = ["PDSPrompt.txt"]
select_prompt_mode = prompt_list[0]

with open(select_prompt_mode, "r", encoding='utf-8') as file:
    data_prompt = file.read()

messages = [{"role": "system", "content": data_prompt}]

user_input()