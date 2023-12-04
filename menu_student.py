import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def get_meal_url_for_date(meal_time, target_date):
    return f"https://www.mealtify.com/univ/pusan/gumjeong-student/meal/{target_date}/{meal_time}"

def get_menu_info(item_title):
    meal_type = item_title.text

    # 메뉴 정보가 있는 테이블을 찾기
    menu_table = item_title.find_next('table')

    # 테이블에서 각각의 행을 찾아 메뉴 정보를 문자열로 저장
    menu_items = []
    rows = menu_table.find_all('tr')
    for row in rows[1:-1]:  # 첫 번째 행은 헤더, 마지막 행은 총 칼로리이므로 제외
        columns = row.find_all('td')
        menu_name = columns[0].text
        menu_items.append(menu_name)

    # 메뉴 정보를 하나의 문자열로 출력
    menu_string = ". ".join(menu_items)

    return menu_string, meal_type

def crawling_and_write_to_csv(url, csv_writer, target_date, meal_time):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # "일품","일반","아침"에 해당하는 h4 태그를 찾기
        item_titles = soup.find_all('h4', class_='MenuTableMultiple_h4-title__DwlrY')

        for item_title in item_titles:
            menu_string, meal_type = get_menu_info(item_title)

            # csv파일 작성
            csv_writer.writerow([menu_string, meal_time, target_date, "금정회관-학생", meal_type])

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")#url이 없는 경우

def main():
    #meal times
    meal_times = ["breakfast", "lunch", "dinner"]

    #CSV file path
    csv_file_path = "menu_student.csv"

    # Open a CSV file in write mode
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # 헤더 작성
        csv_writer.writerow(['메뉴', '식사시간', '날짜', '식당', '타입'])

        # 오늘 날짜 확인
        current_date = datetime.now()
        target_date = current_date.strftime("%Y-%m-%d")

        # 오늘과 내일 메뉴, 금요일은 하루만 작성
        if current_date.weekday() == 4:  # 4 ->Friday
            for meal_time in meal_times:
                meal_url = get_meal_url_for_date(meal_time, target_date)
                crawling_and_write_to_csv(meal_url, csv_writer, target_date, meal_time)
        else:
            # Loop through meal times and scrape, and write to CSV for both today and tomorrow
            for _ in range(2):
                for meal_time in meal_times:
                    meal_url = get_meal_url_for_date(meal_time, target_date)
                    crawling_and_write_to_csv(meal_url, csv_writer, target_date, meal_time)

                #다음날 작성
                target_date = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")

    print("금정회관 학생 메뉴 정보입니다.")

if __name__ == "__main__":
    main()