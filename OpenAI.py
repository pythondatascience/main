## 사용한 opensource, 모듈
# openai 모듈(서비스)

## Ubuntu20.04 기준 모듈 설치방법
# sudo pip3 install openai 
# (실패시) sudo pip3 install openai==0.28 

## 독창적인 부분
# 1. 최근 관심이 높은 ChatGPT와 프롬프팅기술을 이용하여 부산대학교 전용 LLM서비스를 구축
# 2. GPT를 이용했기 때문에 자연어를 구사하여 원하는 정보를 얻어낼 수 있음
# 3. 파일 I/O를 이용하여 코드를 간결하게 구현
# 4. 외부 라이브러리를 사용하였지만, 챗봇구현을 위한 알고리즘은 자체개발함 (answer와 user input이 상호작용 하는 알고리즘)

## 참조문헌
# https://platform.openai.com/docs/guides/text-generation/chat-completions-api : 해당 홈페이지의 reference 참조

## 제작방식
# 혼합(정주영, 최정민)

### Start here (개발담당 : 정주영)
import openai
import subprocess

openai.api_key = "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"
hidden_bus_key = "31qwef#fAWedf#fFsfdew"

def answer(user_content):
    messages.append({"role" : "user", "content" : f"{user_content}"})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0,
        max_tokens=256
    )

    assistant_content = completion.choices[0].message["content"].strip()

    if hidden_bus_key in assistant_content:       
        execute_bus_track()
        messages.append({"role": "assistant", "content": assistant_content})
        print("ChatPNU : " + assistant_content)
        text = "현재 순환버스의 위치를 표시합니다."
        return text
### End here (개발담당 : 정주영)


### Start here (개발담당 : 최정민)
    else:
        print("ChatPNU : " + assistant_content)
        messages.append({"role": "assistant", "content": assistant_content})  
        return assistant_content  

def execute_bus_track():
    result = subprocess.run(["python3", "./PDSProject/bus_track.py"], capture_output=True, text=True) #위치를 변경하였습니다.
    print(result.stdout)
### End here (개발담당 : 최정민)


### Start here (개발담당 : 정주영)
prompt_list = ["PDSPrompt.txt"]
select_prompt_mode = prompt_list[0]

with open(select_prompt_mode, "r", encoding='utf-8') as file:
    data_prompt = file.read()

messages = [{"role": "system", "content": data_prompt}]

### End here (개발담당 : 정주영)
