import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def scrape_menu(url, meal_type):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        return None, None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_elements = soup.find_all('td', class_='px-4 py-3 text-center')
    menu_list = [menu.text for menu in menu_elements]
    
    calorie_element = soup.find('td', class_='px-4 py-3 text-center', text='총 칼로리:')
    calorie = calorie_element.text if calorie_element else None
    
    return menu_list, calorie

def write_to_csv(file, menu_list, calorie, meal_type):
    with open(file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        # Header
        writer.writerow(["메뉴", "타입", "칼로리", "시간"])
        
        # Data
        for i in range(0, len(menu_list), 3):
            writer.writerow([menu_list[i], menu_list[i + 1], menu_list[i + 2], meal_type])
        
        # Total Calorie
        writer.writerow(["총 칼로리", "", calorie])

# 아침 메뉴 크롤링 및 CSV 작성
url_breakfast = "https://www.mealtify.com/univ/pusan/gumjeong-staff/meal/today/breakfast"
menu_list_breakfast, calorie_breakfast = scrape_menu(url_breakfast, "아침")
write_to_csv("menu_information_breakfast.csv", menu_list_breakfast, calorie_breakfast, "아침")
print("아침 메뉴 파일이 생성되었습니다.")

# 점심 메뉴 크롤링 및 CSV 작성
url_lunch = "https://www.mealtify.com/univ/pusan/gumjeong-staff/meal/today/lunch"
menu_list_lunch, calorie_lunch = scrape_menu(url_lunch, "점심")
write_to_csv("menu_information_lunch.csv", menu_list_lunch, calorie_lunch, "점심")
print("점심 메뉴 파일이 생성되었습니다.")

# 저녁 메뉴 크롤링 및 CSV 작성
url_dinner = "https://www.mealtify.com/univ/pusan/gumjeong-staff/meal/today/dinner"
menu_list_dinner, calorie_dinner = scrape_menu(url_dinner, "저녁")
write_to_csv("menu_information_dinner.csv", menu_list_dinner, calorie_dinner, "저녁")
print("저녁 메뉴 파일이 생성되었습니다.")

# CSV 파일 합치기
df_breakfast = pd.read_csv("menu_information_breakfast.csv", encoding="utf-8")
df_lunch = pd.read_csv("menu_information_lunch.csv", encoding="utf-8")
df_dinner = pd.read_csv("menu_information_dinner.csv", encoding="utf-8")

df_combined = pd.concat([df_breakfast, df_lunch, df_dinner], ignore_index=True)
df_combined.to_csv("menu_information_combined.csv", index=False, encoding="utf-8")

print("세 파일이 합쳐진 새로운 파일이 생성되었습니다.")