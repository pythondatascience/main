import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def scrape_and_write_to_csv(url, meal_type, csv_file):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_elements = soup.find_all('td', class_='px-4 py-3 text-center')
    menu_list = [menu.text for menu in menu_elements]
    
    calorie_element = soup.find('td', class_='px-4 py-3 text-center', text='총 칼로리:')
    calorie = calorie_element.text if calorie_element else None
    
    with open(csv_file, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        # Data
        for i in range(0, len(menu_list), 3):
            writer.writerow([menu_list[i], menu_list[i + 1], menu_list[i + 2], meal_type])
        
        # Total Calorie
        writer.writerow(["총 칼로리", "", calorie])

# Define URLs and CSV file path
urls = {
    "아침": "https://www.mealtify.com/univ/pusan/gumjeong-staff/meal/today/breakfast",
    "점심": "https://www.mealtify.com/univ/pusan/gumjeong-staff/meal/today/lunch",
    "저녁": "https://www.mealtify.com/univ/pusan/gumjeong-staff/meal/today/dinner"
}

csv_file_path = "menu_information_combined.csv"

# Write header to CSV file
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["메뉴", "타입", "칼로리", "시간"])

# Loop through URLs and scrape/write to CSV
for meal_type, url in urls.items():
    scrape_and_write_to_csv(url, meal_type, csv_file_path)

print("세 파일이 합쳐진 새로운 파일이 생성되었습니다.")
