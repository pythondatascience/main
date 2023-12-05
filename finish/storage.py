import os
import subprocess
from datetime import datetime, timedelta
# import Prompting
# 스크립트와 CSV 파일 이름의 쌍을 정의합니다.
script_csv_pairs = {
    "menu.py": "menu.csv",
    # "notice.py": "notice.csv",
    # "schedule.py": "schedule.csv"
    }

# 현재 작업 디렉토리를 변경합니다. (파이썬 파일이 존재하는 경로)
os.chdir("/home/pnuee/다운로드/finish")

# 각 스크립트를 실행합니다.
for script, csv_file in script_csv_pairs.items():
    # CSV 파일이 이미 존재하는지 확인합니다. == 처음 실행 되었을 때
    if os.path.isfile(csv_file):
        # CSV 파일의 수정 시간을 가져옵니다.
        # csv_creation_date = datetime.fromtimestamp(os.path.getctime(csv_file)).date()
        csv_modification_time = datetime.fromtimestamp(os.path.getmtime(csv_file)).date()
        # print(csv_creation_date)
        # print(csv_modification_time)
        
        # 현재 날짜를 가져옵니다.
        current_date = datetime.now().date()

        # CSV 파일이 수정된 날짜와 현재 날짜가 다르면 해당 스크립트를 다시 실행합니다.
        # if csv_creation_date != current_date:
        if csv_modification_time != current_date:
            command = f"python {script}"
            subprocess.run(command, shell=True)
            print(f"{csv_file}이(가) 업데이트되었습니다.")
        else:
            print(f"{csv_file} 파일이 이미 존재합니다.")  # 같은 날이면 기존 csv파일 사용
    else:
        # CSV 파일이 없으면 해당 스크립트를 실행합니다.
        command = f"python {script}"
        subprocess.run(command, shell=True)
        print(f"{csv_file}이(가) 생성되었습니다.")

print("모든 스크립트가 실행되었습니다.")

# menu_csv_filename = 'menu.csv'
# notice_csv_filename = 'notice.csv'
# schedule_csv_filename = 'schedule.csv'
# txt_filename = 'PDSPrompt.txt'
# new_column_order = ['날짜', '타입', '식사시간', '메뉴']

# Prompting.csv_to_txt(menu_csv_filename, notice_csv_filename, schedule_csv_filename, txt_filename, new_column_order)