import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
# from Prompting =>파이썬 파일 import 파일안 어떤 클래스  
url = 'https://onestop.pusan.ac.kr/login'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


class PNU_Crawiling:
    
    def __init__(self,condition):
        self.condition =condition
    
    def connect(self):     
        if response.status_code == 200:
            self.condition = True
        else :
            self.condition = False
            print("연결할 수 없습니다.")
    
    def make_csv_file(self,category,df):
        df.to_csv(f'{category}_data.csv', index=False, encoding='utf-8')




class Schedule(PNU_Crawiling):
    def __init__(self,condition):
        super().__init__(condition)

    def extract_data(self): 
        category = "schdule"
        schedule_section = soup.find('section', class_='sec-smart-schedule')
        
        if schedule_section:
            schedule_list = schedule_section.find('ul', class_='schedule-list')
            
            if schedule_list:
                schedule_items = schedule_list.find_all('li')

            # 데이터를 저장할 리스트 생성
            data_list = []

            # 각 항목을 순회하며 데이터 리스트에 추가
            for item in schedule_items:
                schedule_date = item.find(class_='list-date').text.strip()
                schedule_subject = item.find(class_='subject').text.strip()
                data_list.append([schedule_date, schedule_subject])

            df = pd.DataFrame(data_list, columns=['기간', '일정'])

        super().make_csv_file(category,df)



        
        
        



schedule_instance = Schedule(response)  

schedule_instance.extract_data()

# class Bus(PNU_Crawiling) :
     
# class Menu(PNU_Crawiling) :     
     
# def main():
    



# if __name__ = '__main__':
#     main()          