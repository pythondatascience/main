# 작성자: 안도욱
# 제작 방식 :혼합(chat-gpt)

# sudo pip install requests
# sudo pip install bs4
# sudo pip install datetime(내장모듈)

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

################################# start here (개발담당 : 안도욱) #################################
def get_meal_url_for_date(meal_time, target_date):
    return f"https://www.mealtify.com/univ/pusan/gumjeong-student/meal/{target_date}/{meal_time}"

def get_menu_info(item_title):
    meal_type = item_title.text
    menu_table = item_title.find_next('table')

    menu_items = []
    rows = menu_table.find_all('tr')
    for row in rows[1:-1]:  # 첫 번째 행은 헤더, 마지막 행은 총 칼로리이므로 제외
        columns = row.find_all('td')
        menu_name = columns[0].text
        menu_items.append(menu_name)

    menu_string = ". ".join(menu_items)

    return menu_string, meal_type

##################################chat gpt start########################################
#chat gpt를 사용해 크롤링을 위한 코드를 가져왔습니다.
def crawl_menu_info(url):
    response = requests.get(url, allow_redirects=False)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all('h4', class_='MenuTableMultiple_h4-title__DwlrY')

    elif response.status_code == 302 or response.status_code == 301:
        redirected_url = response.headers['Location']
        print(f"Redirected to: {redirected_url}")
        return None  # 리디렉션이면 None 반환

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
############################chat gpt end##############################################
def write_to_csv(csv_writer, menu_info, target_date, meal_time):
    if menu_info is not None:
        expected_types = ["1000원의 아침", "일반", "일품"]
        found_types = set()

        for expected_type in expected_types:
            type_found = False

            for item_title in menu_info:
                menu_string, meal_type = get_menu_info(item_title)

                if meal_type == expected_type:
                    type_found = True
                    found_types.add(meal_type)
                    csv_writer.writerow([menu_string, meal_time, target_date, "금정회관-학생", meal_type])

            if not type_found:
                csv_writer.writerow(["없음", meal_time, target_date, "금정회관-학생", expected_type])
    else:
        # If menu_info is None == url 존재x
        for expected_type in ["1000원의 아침", "일반", "일품"]:
            csv_writer.writerow(["없음", meal_time, target_date, "금정회관-학생", expected_type])

def main():
    meal_times = ["breakfast", "lunch", "dinner"]
    csv_file_path = "menu.csv"

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['메뉴', '식사시간', '날짜', '식당', '타입'])

        current_date = datetime.now()
        target_date = current_date.strftime("%Y-%m-%d")

        for _ in range(2):
            for meal_time in meal_times:
                meal_url = get_meal_url_for_date(meal_time, target_date)
                menu_info = crawl_menu_info(meal_url)
                write_to_csv(csv_writer, menu_info, target_date, meal_time)

            target_date = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")

    print("금정회관 학생 메뉴 정보입니다.")

if __name__ == "__main__":
    main()
################################# end here (개발담당 : 안도욱) #################################      