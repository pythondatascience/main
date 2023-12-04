import os
import subprocess
from datetime import datetime, timedelta

# 스크립트와 CSV 파일 이름의 쌍을 정의합니다.
script_csv_pairs = {
    "menu_student.py": "menu_student.csv",
    "공지사항.py": "Notice.csv",
    "학사일정.py": "schedule_data.csv"
    }

# 현재 작업 디렉토리를 변경합니다. (파이썬 파일이 존재하는 경로)
os.chdir("/home/pnuee/menu")

# 각 스크립트를 실행합니다.
for script, csv_file in script_csv_pairs.items():
    # CSV 파일이 이미 존재하는지 확인합니다. == 처음 실행 되었을 때
    if os.path.isfile(csv_file):
        # CSV 파일의 생성 날짜를 가져옵니다.
        csv_creation_date = datetime.fromtimestamp(os.path.getctime(csv_file)).date()
        
        # 현재 날짜를 가져옵니다.
        current_date = datetime.now().date()

        # CSV 파일이 생성된 날짜와 현재 날짜가 다르면 해당 스크립트를 다시 실행합니다.
        if csv_creation_date != current_date:
            command = f"python {script}"
            subprocess.run(command, shell=True)
            print(f"{csv_file}이(가) 업데이트되었습니다.")
        else:
            print(f"{csv_file} 파일이 이미 존재합니다.") # 같은 날이면 기존 csv파일 사용
    else:
        # CSV 파일이 없으면 해당 스크립트를 실행합니다.
        command = f"python {script}"
        subprocess.run(command, shell=True)
        print(f"{csv_file}이(가) 생성되었습니다.")

print("모든 스크립트가 실행되었습니다.")
