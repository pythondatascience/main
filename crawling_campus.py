import requests
from bs4 import BeautifulSoup
import csv
from itertools import cycle

url="https://www.pusan.ac.kr/kor/CMS/MenuMgr/menuListOnBuilding.do?mCode=MN202"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

if response.status_code == 200:
    # Parse the HTML content of the page   
    meal_table = soup.find('table', {'class': 'menu-tbl'})
    csv_file_path = 'meal_information_campus.csv'

    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Restaurant', 'Meal Type', 'Menu'])

        # Extract information for each day and meal type
        for row in meal_table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all(['th', 'td'])

            # Extract restaurant name
            restaurant_name = soup.find('span', {'class': 'term'}).get_text(strip=True)
            # Extract meal type and menu
            meal_type = columns[0].find('br').previous_sibling.strip() if columns[0].find('br') else columns[0].get_text(strip=True)
            menu_items = [item.get_text(strip=True) for item in columns[1:]]
            # Write the information to the CSV file
            for menu_item in menu_items:
                csv_writer.writerow([restaurant_name,meal_type, menu_item])

    print("CSV file created successfully.")

    #############################################################################################
    # day, date 데이터를 csv추가
    new_column_title = 'day'
    new_column_title2 = 'date'

    day=[]
    date=[]

    day_elements = soup.find_all('div', {'class': 'day'})
    date_elements = soup.find_all('div', {'class': 'date'})

    for day_element in day_elements:
        day.append(day_element.get_text(strip=True))


    for date_element in date_elements:
        date.append(date_element.get_text(strip=True))    


    # # CSV 파일 열기 및 데이터 읽기
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    data[0].append(new_column_title)  # 새로운 열의 제목 추가
    data[0].append(new_column_title2) 

    # # 나머지 행에 새로운 데이터 추가 (day를 순환하도록 수정)
    new_column_data_cycle = cycle(day)
    new_column_data_cycle2 = cycle(date)
    for i in range(1, len(data)):
        data[i].append(next(new_column_data_cycle))
        data[i].append(next(new_column_data_cycle2))

    # 업데이트된 데이터를 CSV 파일에 쓰기
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f'열이 성공적으로 추가되었습니다. 파일 경로: {csv_file_path}')
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
