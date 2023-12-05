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
pip install requsts
pip install bs4
pip install pandas
pip install os
    
-제작 방식 
:혼합(gpt 사용했습니다.)

기타 수정 사항들과 프로그램 구현하는 데 있어서 많이 참고한 부분은 # 처리하겠습니다.

참고한 곳은 쳇지피티밖에 없기 때문에 밑에 # 표시한 부분의 출처는 쳇지피티입니다.

"""""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

class PNU_Crawling:
    def __init__(self, url):  ## 초기화 하는 부분 아이디어 얻었습니다.
        self.condition = False
        self.response = None
        self.url = url
        self.soup = None
################################# start here ################################# 
    def connect(self):     
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.condition = True
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            return self.soup
        else:
            self.condition = False

    ################### chat gpt code ###################
    def make_csv_file(self, category, df):
        current_directory = os.getcwd()
        data_storage_path = os.path.join(current_directory, 'data_storage')
        file_path = os.path.join(data_storage_path, f'{category}_.csv')
        df.to_csv(file_path, index=False, encoding='utf-8') 
    ################### chat gpt code ###################
class Notice(PNU_Crawling):
    def __init__(self, category, url):
        super().__init__(url)
        self.category = category
        self.date_list = []
        self.notice_list = []
        self.target = None

    def target_id(self):
        self.target = self.soup.find('div', {'id': 'menu14870_obj250'})
        return self.target
    
    def collect_data(self):
        if self.target_id():
            td_dates = self.target.find_all('td', class_="_artclTdRdate")
            td_notices = self.target.find_all('a', class_="artclLinkView")
            for td_date, td_notice in zip(td_dates, td_notices): 
                self.date_list.append(td_date.get_text(strip=True))
                cleaned_notice = td_notice.get_text(strip=True).replace('\n', '').replace('\t', '').strip() # 데이터를 읽기 편하게 정리하는 부분 참고했습니다.
                self.notice_list.append(cleaned_notice)
        return self.date_list, self.notice_list
    
    def sort_data(self):
        self.collect_date, self.collect_notice = self.collect_data()
        if self.collect_date and self.collect_notice:  
            self.data = {'작성일': self.collect_date, '공지': self.collect_notice} # 데이터 값을 정리하는 부분 참고했습니다.
            df = pd.DataFrame(self.data)

            self.make_csv_file('Notice', df)
        else:
            print("데이터를 수집할 수 없습니다.")

def main():
    url = 'https://eec.pusan.ac.kr/eehome/14870/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZWVob21lJTJGMjY1MCUyRmFydGNsTGlzdC5kbyUzRg%3D%3D'  # 실제 URL 입력
    notice_data = Notice('notice', url)
    notice_data.connect()
    notice_data.sort_data()

if __name__ == '__main__':
    main()

################################# end here ################################# 