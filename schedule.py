import requests
from bs4 import BeautifulSoup
import csv

url = 'https://onestop.pusan.ac.kr/login'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # 해당 섹션을 찾습니다.
    schedule_section = soup.find('section', class_='sec-1 sec-smart-schedule')
    if schedule_section:
        # 해당 섹션 내에서 데이터를 추출합니다.
        schedule_list = schedule_section.find('ul', class_='schedule-list')
        if schedule_list:
            # 각 일정별로 데이터를 추출합니다.
            schedule_items = schedule_list.find_all('li')

            # CSV 파일 작성
            with open('schedule_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['날짜', '일정'])  # 헤더 작성

                for item in schedule_items:
                    schedule_date = item.find(class_='list-date').text.strip()
                    schedule_subject = item.find(class_='subject').text.strip()
                    writer.writerow([schedule_date, schedule_subject])
                
                print("CSV 파일이 생성되었습니다.")
        else:
            print("일정 목록을 찾을 수 없습니다.")
    else:
        print("섹션을 찾을 수 없습니다.")
else:
    print("페이지를 가져올 수 없습니다.")
