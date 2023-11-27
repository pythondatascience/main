import requests
from bs4 import BeautifulSoup
import csv
from itertools import cycle

def extract_day(soup):
    return soup.find('span', {'class': 'term'}).get_text(strip=True)

def extract_restaurant_info(row):
    restaurant_name = row.find(['th', 'td']).find('br').previous_sibling.strip() if row.find(['th', 'td']).find('br') else row.find(['th', 'td']).get_text(strip=True)
    menu_items = [item.get_text(strip=True) for item in row.find_all(['th', 'td'])[1:]]
    return restaurant_name, menu_items

def write_to_csv(csv_file_path, header, data):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerows(data)

def main():
    url = "https://www.pusan.ac.kr/kor/CMS/MenuMgr/menuListOnWeekly.do?mCode=MN203"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meal_table = soup.find('table', {'class': 'menu-tbl'})
        csv_file_path = 'meal_information.csv'

        header = ['Restaurant', 'day', 'Menu']

        data = []
        for row in meal_table.find_all('tr')[1:]:
            day = extract_day(soup)
            restaurant_name, menu_items = extract_restaurant_info(row)

            for menu_item in menu_items:
                data.append([restaurant_name, day, menu_item])

        print("CSV file created successfully.")


        new_column_title = 'time'
        time = cycle(["조식", "중식", "석식"])

        with open(csv_file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        # 새로운 열 추가
        data[0].append(new_column_title)
        for i in range(1, len(data)):
            data[i].append(next(time))

        write_to_csv(csv_file_path, header, data)

        print(f'Columns added successfully. File path: {csv_file_path}')

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    main()