import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://onestop.pusan.ac.kr/login'
class PNU_Crawling:
    def __init__(self):
        self.condition = False
        self.response = None
    
    def connect(self):     
        self.response = requests.get(url)
        if self.response.status_code == 200:
            self.condition = True
        else:
            self.condition = False
    
    def make_csv_file(self, category, df):
        df.to_csv(f'{category}_data.csv', index=False, encoding='utf-8')


class Schedule(PNU_Crawling):
    def extract_data(self): 
        self.connect()  

        if self.condition:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            category = "schedule"
            schedule_section = soup.find('section', class_='sec-smart-schedule')
            
            if schedule_section:
                schedule_list = schedule_section.find('ul', class_='schedule-list')
                
                if schedule_list:
                    schedule_items = schedule_list.find_all('li')
                
                    data_list = []
                    for item in schedule_items:
                        schedule_date = item.find(class_='list-date').text.strip()
                        schedule_subject = item.find(class_='subject').text.strip()
                        data_list.append([schedule_date, schedule_subject])
                
                    df = pd.DataFrame(data_list, columns=['기간', '일정'])
                    self.make_csv_file(category, df)
        else:
            print("연결할 수 없습니다.")




def main():
    schedule_data = Schedule()
    schedule_data.extract_data()

if __name__ == '__main__':
    main()

