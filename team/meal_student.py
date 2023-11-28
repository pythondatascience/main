import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def get_meal_url_for_date(meal_type, target_date):
    return f"https://www.mealtify.com/univ/pusan/gumjeong-student/meal/{target_date}/{meal_type}"

def scrape_and_write_to_csv(url, meal_type, csv_file, target_date):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_elements = soup.find_all('td', class_='px-4 py-3 text-center')
    menu_list = [menu.text for menu in menu_elements]

    calorie_element = soup.find('td', class_='px-4 py-3 text-center', string='총 칼로리:')
    calorie = calorie_element.text if calorie_element else None
    
    with open(csv_file, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        # Data
        for i in range(0, len(menu_list), 3):
            writer.writerow([menu_list[i], menu_list[i + 1], menu_list[i + 2], meal_type, target_date])
        
        # Total Calorie
        writer.writerow(["총 칼로리", "", calorie, meal_type, target_date])

# Define meal types
meal_types = ["breakfast", "lunch", "dinner"]

# Define CSV file path
csv_file_path = "menu_fff.csv"

# Write header to CSV file
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["메뉴", "타입", "칼로리", "시간"])

# Loop through next 7 days
current_date = datetime.now()
for _ in range(7):
    target_date = current_date.strftime("%Y-%m-%d")
    
    # Loop through meal types and scrape, and write to CSV
    for meal_type in meal_types:
        meal_url = get_meal_url_for_date(meal_type, target_date)
        scrape_and_write_to_csv(meal_url, meal_type, csv_file_path, target_date)
    
    current_date += timedelta(days=1)

print("7일간의 파일이 생성되었습니다.")


    