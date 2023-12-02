import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def get_meal_url_for_date(meal_time, target_date):
    return f"https://www.mealtify.com/univ/pusan/gumjeong-staff/{target_date}/{meal_time}"

def get_menu_values(soup):
    menu_elements = soup.find_all('td', class_='px-4 py-3 text-center')
    menu_values = [element.text for element in menu_elements]
    # 마지막 행인 총 칼로리를 빼고 반환
    menu_values = [menu_values[i] for i in range(0, len(menu_values) - 3, 3)]

    # 메뉴 정보를 하나의 문자열로 출력
    menu_string = ". ".join(menu_values)
    meal_type=""

    return menu_string,meal_type

def crawling_and_write_to_csv(url, csv_writer, target_date, meal_time):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    menu_string,meal_type = get_menu_values(soup)  
    csv_writer.writerow([menu_string, meal_time, target_date, "금정회관-교직원",meal_type])

def main():
    # Define meal times
    meal_times = ["lunch"]

    # Define CSV file path
    csv_file_path = "menu_staff.csv"

    # Open a CSV file in write mode
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        csv_writer.writerow(['메뉴', '식사시간', '날짜', '식당', '타입'])

        # Loop through weekdays (Monday to Friday) of the current week
        current_date = datetime.now()
        start_of_week = current_date - timedelta(days=current_date.weekday())

        for _ in range(5):
            target_date = start_of_week.strftime("%Y-%m-%d")

            # Loop through meal times and scrape, and write to CSV
            for meal_time in meal_times:
                meal_url = get_meal_url_for_date(meal_time, target_date)
                crawling_and_write_to_csv(meal_url, csv_writer, target_date, meal_time)
                
            start_of_week += timedelta(days=1)

    print("이번주 월요일부터 금요일까지의 파일이 생성되었습니다.")

if __name__ == "__main__":
    main()