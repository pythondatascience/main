# main
### 1. 프로그램 구동을 위한 필수 패키지

tkinter

datetime

openai

subprocess

requests

bs4

folium

googlemaps

csv

pandas

os

—————
### 2. Ubuntu 20.04 기준 설치 방법

sudo apt-get install python3-tk

sudo pip3 install openai==0.28

sudo pip3 install requests

sudo pip3 install bs4

sudo pip3 install beautifulsoup4 (* sudo pip3 install bs4와 동일, 실행안될 시 추가설치)

sudo pip3 install lxml

sudo pip3 install folium

sudo pip3 install googlemaps

sudo pip3 install datetime (* 우분투환경에 내장되어 있다고 하나 필요시 설치)

sudo pip3 install pandas

—————
### 3. 프로젝트 주요 특징

기존의 GPT가 답변해주지 못하는 부산대학교의 실시간 정보(학식메뉴, 순환버스, 공지사항, 학사일정)들을 제공해주는 프로그램이다.

크롤링, ChatGPT, 프롬프팅기술을 이용하여 부산대학교 전용 LLM서비스를 구축하였다.




구글링없이 Openai 홈페이지 레퍼런스만을 참고하여 전체적인 챗봇 알고리즘을 구상, 코드화하였으며, GPT가 크롤링된 부산대학교 홈페이지 정보들을 어떻게 전달하는것이 효과적인지에 대한 프롬프팅 알고리즘에 대해 공부하여 알고리즘을 선정하고 이를 코드화하였다.

또한 부산대학교 파이썬데이터사이언스 수업때 배운 ‘파일 I/O’와 ‘pandas모듈’을 적극활용하여 크롤링과 파이썬 파일들을 간접적으로 연결하였으며, 파이썬 파일들을 서로 import하여 ChatGUI.py 코드만 실행하여도 모든 파이썬 파일을 이용하도록 전체 프로그램 알고리즘을 고안하였다.



실제 자연어로 대화를 하여도 챗봇이 인식하여 원할하게 정보를 제공면서 자연스럽게 유저와 상호작용하는 것을 확인할 수 있다.

최종적으로 파이썬 GUI모듈 tkinter를 이용하여 터미널이 아니라 유저가 익숙한 챗봇화면을 구상하여 사용편의성을 증대시켰다.


—————
### 4. 프로그램 실행방법

1. 깃허브에서 코드 다운

2. main.zip 파일 압축해제 (현재 파일경로가 main으로 설정되어 있기 때문 / 경로를 직접 지정할시 (2)과정 생략가능)

3. OpenAI.py의 line24에 “YOUR_API_KEY” 부분에 PPT에 작성되어있는 API키를 입력

4. ChatGUI.py 파일 실행


—————
### 5. 프로그램 실행시 주의사항

1. API 키

코드를 작동시키기 위해서는 먼저 OpenAI.py의 lin24의 “YOUR_API_KEY” 부분에 API키를 입력하여야 합니다.



2. 파일경로 : 파일 경로를 잘 지정해주어야 파일이 정상적으로 동작합니다.

경로1 : storage.py의 line17

경로2 : OpenAI.py의 line 59, line 63

경로3 : bus_track.py의 line 115



(3) 인터넷 브라우저

bus_track.py의 line 116~118에서 자신에게 해당하는 인터넷 브라우저로 변경하여야 합니다.


—————
### 6. Class, Sequence 다이어그램

1. Class 다이어그램

Notice와 Schedule의 클래스를 PNU_Crawling이 상속한다. (이는 Notice와 Schedule을 한 사람이 담당하여 발생한 현상.)

이후 PNU_Crawling과 menu를 storage.py에서 받아서 Prompting.py를 실행한다. 그럼 PDSPrompt.txt이 생성된다.

생성된 PDSPrompt.txt와 BusanMap 클래스를 OpenAI와 연결하고, OpenAI를 ChatGUI에 상속시킨다.

최종적으로 ChatGUI와 storage.py를 연결하여 유저는 ChatGUI.py만 실행하여도 전체 Class를 이용하여 프로그램을 실행시킬 수 있게 된다.



2.  Sequence 다이어그램

실제 유저가 경험할 수 있는 시나리오는 채팅화면을 통해 챗봇과 소통하는 것이다.

User - ChatGUI 시퀀스를 중심으로, 크롤링과 버스정보, GPT통신과 같은 시퀀스가 존재한다.

해당 Sequence 다이어그램은 “seq_diagram_최종.pmul’로 확인할 수 있습니다.


—————
### 7. 파이썬 파일별 요약

1. ChatGUI.py

제작방식 : 혼합

제작자 : 정주영

사용모듈 : tkinter, datetime

독창적인 부분

  터미널에서 실행하는 것이 아니라 채팅창을 만들어 유저들의 이용편의성 증대

  import를 이용하여 파이썬 파일들을 연결하여 ChatGUI.py를 실행하여도 전체 코드가 작동되도록 동작

참조문헌

  [OpenAI 레퍼런스](https://076923.github.io/posts/Python-tkinter-1/) : 해당 홈페이지의 tkinter 강의글 참조



2. OpenAI.py

제작방식 : 자체개발

제작자 : 정주영, 최정민

사용모듈 : openai

독창적인 부분

  최근 관심이 높은 ChatGPT와 프롬프팅기술을 이용하여 부산대학교 전용 LLM서비스를 구축

  GPT를 이용했기 때문에 자연어를 구사하여 원하는 정보를 얻을 수 있음

  파일 I/O를 이용하여 코드를 간결하게 구현

  전체적인 대화 알고리즘은 자체적으로 생각하여 구현

참조문헌

  <https://platform.openai.com/docs/guides/text-generation/chat-completions-api> : 해당 홈페이지의 reference 참조



3. bus_track.py

제작방식 : 혼합

제작자 : 최정민

사용모듈 : requests, beautifulsoup4, lxml, folium, googlemaps

독창적인 부분

  공공기관 데이터의 API를 받아 실시간으로 버스의 위치 확인가능

  버스의 상행, 하행의 방향 뿐만 아니라 정차 상태도 확인가능

  부산대 순환버스에서만 국한되는 것이 아니라, 버스 노선 id와 기준 좌표 수정시 다른 노선의 위치도 확인이 가능

참조문헌

  ChatGPT : 코드의 대략적인 구조(클래스 형태 구현 측면에서)

  <https://www.data.go.kr/iim/api/selectAPIAcountView.do> : OpenAPI활용가이드_부산버스정보시스템_v2.0.docx 참고 (api키, 버스 실시간 좌표, 방향)

  <https://www.data.go.kr/data/15092750/openapi.do#tab_layer_detail_function> : 샘플 코드 > Python 쪽 참조 (데이터 가져오기)

  <https://minjoo-happy-blog.tistory.com/34> : 파싱 참조

  <https://continuous-development.tistory.com/entry/Python-%EC%8B%9C%EA%B0%81%ED%99%94-%EC%82%AC%EC%9A%A9%EB%B2%95-folium-%EC%9D%84-%ED%86%B5%ED%95%9C-%EC%A7%80%EB%8F%84-%EC%8B%9C%EA%B0%81%ED%99%94-%EB%B0%8F-%EB%A7%88%EC%BB%A4marker-%EC%B0%8D%EA%B8%B0> : folium 기초 명령어(핀 찍기, 지도 출력, 저장)

  <https://wooiljeong.github.io/python/folium-google-tiles/> : folium 지도를 googlemap으로 설정



4. menu.py

제작방식 : 혼합

제작자 : 안도욱

사용모듈 : requests, bs4, datatime

참조문헌

  ChatGPT



5. notice.py
제작방식 : 혼합

제작자 : 홍석기

사용모듈 : bs4, requests, pandas

참조문헌

  ChatGPT (실제 GPT에게 한 질문과 답변을 추가)



6. schedule.py

제작방식 : 혼합

제작자 : 홍석기

사용모듈 : requests, pandas, bs4

참조문헌

  ChatGPT (실제 GPT에게 한 질문과 답변을 추가)



7. Prompting.py

제작방식 : 자체개발

제작자 : 최정민, 정주영

사용모듈 : pandas

독창적인 부분

  GPT가 이해하기 쉽도록 정보를 나열하는 알고리즘을 공부하여 코드화하였음

  수업때 배운 pandas를 이용

참조문헌

  ChatGPT

  파이썬데이터사이언스 수업자료



8. storage.py

제작방식 : 혼합

제작자 : 안도욱

사용모듈 : os, subprocess, datetime

독창적인 부분

  파이썬 파일을 연결하였음

참조문헌

 ChatGPT


