"""""
-담당자 : 홍석기

-참고 문헌 : chat_gpt 크롤링 하는 기본 예제 보여줘 
#####################################################################################################
import requests
from bs4 import BeautifulSoup

# 크롤링할 페이지 URL
url = 'https://example.com'

# 해당 URL로 요청을 보내고 HTML 내용 가져오기
response = requests.get(url)
html_content = response.content

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 제목과 링크 가져오기
titles = soup.find_all('h2')  # 예시로 h2 태그를 가진 제목들을 가져옵니다.
for title in titles:
    # 텍스트 내용과 링크 출력
    print("제목:", title.text.strip())
    print("링크:", title.a['href'])  # 예시로 제목이 링크를 포함하는 경우를 가정합니다.
    print()
#######################################################################################################

-Ubuntu 20.04 기준 모듈 설치 방법
sudo pip install requests 
sudo pip install bs4
sudo pip install pandas

-제작 방식 
:혼합(gpt 사용했습니다.)

기타 수정 사항들과 프로그램 구현하는 데 있어서 많이 참고한 부분은 # 처리하겠습니다.

참고한 곳은 쳇지피티밖에 없기 때문에 밑에 # 표시한 부분의 출처는 쳇지피티입니다.

"""""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

class PNU_Crawling:
    def __init__(self,url): ## 초기화 하는 부분 아이디어 얻었습니다.
        self.url = url
        self.condition = False
        self.response = None
        self.soup = None
################################# start here ################################# 
    def connect(self):     
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.condition = True
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
        else:
            self.condition = False
    
    ################### chat gpt code ###################
    def make_csv_file(self, category, df):
        current_directory = os.getcwd()
        data_storage_path = os.path.join(current_directory, 'data_storage')
        file_path = os.path.join(data_storage_path, f'{category}_.csv')
        df.to_csv(file_path, index=False, encoding='utf-8') 
    ################### chat gpt code ###################


class Schedule(PNU_Crawling):
    def __init__(self, url, category): 
        super().__init__(url)
        self.data_list = []
        self.category = category


        

    def find_section(self):
            self.connect()  
            if self.condition:

                self.schedule_section = self.soup.find('section', class_='sec-smart-schedule')
                return self.schedule_section

    def find_list(self):
        if self.find_section():
            self.schedule_list = self.schedule_section.find('ul', class_='schedule-list')
            return self.schedule_list
        else:
            print("찾을 수 없습니다.")   
            
    def find_data(self):        
        if self.find_list():
            self.schedule_data = self.schedule_list.find_all('li')
            return self.schedule_data

        else:
            print("찾을 수 없습니다.")
            
                
    def sort_data(self):               
        if self.find_data():
            for datum in self.schedule_data:
                schedule_date = datum.find(class_='list-date').text.strip()
                schedule_subject = datum.find(class_='subject').text.strip()
                self.data_list.append([schedule_date, schedule_subject])
                    
            df = pd.DataFrame(self.data_list, columns=['기간', '일정'])  # 데이터 값을 정리하는 부분 참고했습니다.
            self.make_csv_file(self.category, df)
        else:
            print("연결할 수 없습니다.")



def main():
    url = 'https://onestop.pusan.ac.kr/login'
    category = "schedule"
    schedule_data = Schedule(url,category)
    schedule_data.sort_data()

if __name__ == '__main__':
    main()
################################# end here #################################