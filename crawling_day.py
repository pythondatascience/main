import requests
from bs4 import BeautifulSoup
import csv
from itertools import cycle

url = "https://www.pusan.ac.kr/kor/CMS/MenuMgr/menuListOnWeekly.do?mCode=MN203"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the meal information table
    meal_table = soup.find('table', {'class': 'menu-tbl'})

    csv_file_path='meal_information.csv'
    # Create a CSV file and write header
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Restaurant', 'day', 'Menu'])

        # Extract information for each day and meal type
        for row in meal_table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all(['th', 'td'])

            # Extract restaurant name
            day = soup.find('span', {'class': 'term'}).get_text(strip=True)
            
            # Extract meal type and menu
            restaurant_name= columns[0].find('br').previous_sibling.strip() if columns[0].find('br') else columns[0].get_text(strip=True)
            menu_items = [item.get_text(strip=True) for item in columns[1:]]

            # Write the information to the CSV file
            for menu_item in menu_items:
                # Modify the day value to include <div class="day">
                csv_writer.writerow([restaurant_name, day, menu_item])

    print("CSV file created successfully.")

    new_column_title = 'time'
    time=cycle(["조식","중식","석식"])

    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    # 새로운 열 추가
    data[0].append(new_column_title)  # 첫 번째 행에 새로운 열의 제목 추가
    for i in range(1, len(data)):     # 나머지 행에 새로운 데이터 추가
        data[i].append(next(time))  # 순환된 값을 추가

    # 업데이트된 데이터를 CSV 파일에 쓰기
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f'열이 성공적으로 추가되었습니다. 파일 경로: {csv_file_path}')

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")   