from bs4 import BeautifulSoup
import requests
import pandas as pd

class PNU_Crawling:
    def __init__(self, url):
        self.condition = False
        self.response = None
        self.url = url
        self.soup = None
    
    def connect(self):     
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.condition = True
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        else:
            self.condition = False

    
    def make_csv_file(self, category, df):
        df.to_csv(f'{category}.csv', index=False, encoding='utf-8')

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
                cleaned_notice = td_notice.get_text(strip=True).replace('\n', '').replace('\t', '').strip()
                self.notice_list.append(cleaned_notice)
        # 데이터가 있는지 여부에 상관없이 반환
        return self.date_list, self.notice_list
    
    def sort_data(self):
        self.collect_date, self.collect_notice = self.collect_data()
        if self.collect_date and self.collect_notice:  
            self.data = {'공지': self.collect_date, '작성일': self.collect_notice}
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

