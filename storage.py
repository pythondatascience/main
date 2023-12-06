#작성자: 안도욱
# 제작 방식 :혼합(chat-gpt)
# 중요- s.chdir에 파이썬 파일이 존재하는 경로로 바꿔야 합니다!

import os
import subprocess
from datetime import datetime, timedelta
import Prompting
# 스크립트와 CSV 파일 이름의 쌍을 정의합니다.
script_csv_pairs = {
    "menu.py": "menu.csv",
    "notice.py": "notice.csv",
    "schedule.py": "schedule.csv"
    }

# 현재 작업 디렉토리를 변경합니다. (파이썬 파일이 존재하는 경로) 
os.chdir("./") #중요!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


for script, csv_file in script_csv_pairs.items():
    # CSV 파일이 이미 존재하는지 확인합니다. == 처음 실행 되었을 때
    if os.path.isfile(csv_file):
################################# start here (개발담당 : 안도욱) #################################        
       
        csv_modification_time = datetime.fromtimestamp(os.path.getmtime(csv_file)).date() # CSV 파일 수정 시간
        current_date = datetime.now().date() # 오늘 날짜

        if csv_modification_time != current_date:
            command = f"python3 {script}"
            subprocess.run(command, shell=True)
            print(f"{csv_file}이(가) 업데이트되었습니다.")#수정된 날짜와 오늘 날짜 비교
        else:
            print(f"{csv_file} 파일이 이미 존재합니다.")  #같은 날이면 기존 csv파일 사용
################################# end here (개발담당 : 안도욱) #################################  

    else:
        command = f"python3 {script}"
        subprocess.run(command, shell=True)
        print(f"{csv_file}이(가) 생성되었습니다.")

print("모든 스크립트가 실행되었습니다.")

################################# start here (개발담당 : 안도욱) #################################   
menu_csv_filename = 'menu.csv'
notice_csv_filename = 'notice.csv'
schedule_csv_filename = 'schedule.csv'
txt_filename = 'PDSPrompt.txt'
new_column_order = ['날짜', '타입', '식사시간', '메뉴']

Prompting.csv_to_txt(menu_csv_filename, notice_csv_filename, schedule_csv_filename, txt_filename, new_column_order)
################################# end here (개발담당 : 안도욱) #################################  