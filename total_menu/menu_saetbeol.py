import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def get_meal_url_for_date(meal_type, target_date):
    return f"https://www.mealtify.com/univ/pusan/saetbeol/meal/{target_date}/{meal_type}"

def scrape_and_write_to_csv(url, meal_type, csv_file, target_date):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_elements = soup.find_all('td', class_='px-4 py-3 text-center')
    menu_values = [element.text for element in menu_elements]

    # Extract only the first value from each element
    menu_list = [menu_values[i] for i in range(0, len(menu_values), 3)]

    with open(csv_file, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        # Data
        writer.writerow([" ".join(menu_list), meal_type, target_date])

# Define meal types
meal_types = ["lunch","dinner"]

# Define CSV file path
csv_file_path = "menu_saetbeol.csv"

# Write header to CSV file
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["메뉴", "타입", "시간"])

# Loop through next 5 days or until Saturday
current_date = datetime.now()
for _ in range(5):
    target_date = current_date.strftime("%Y-%m-%d")
    
    # Loop through meal types and scrape, and write to CSV
    for meal_type in meal_types:
        meal_url = get_meal_url_for_date(meal_type, target_date)
        scrape_and_write_to_csv(meal_url, meal_type, csv_file_path, target_date)
    
    # Check if current day is Saturday, and exit the loop if true
    if current_date.weekday() == 4:  # 5 corresponds to Saturday
        break
    
    current_date += timedelta(days=1)

print("5일간의 파일이 생성되었습니다.")