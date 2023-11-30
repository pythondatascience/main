from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

class PNU_Crawling():
    def __init__(self,url,driver_path):
        self.url = url
        self.driver_path = driver_path
        self.page_source = None
        self.soup = None
        self.driver =None

    def setting_driver(self) :           
        chrome_options = Options()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--disable-gpu')  
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url)
        self.page_source=driver.page_source
        self.soup = BeautifulSoup(self.page_source, 'html.parser')
        
    def close_driver(self):
        if self.driver:
            self.driver.quit()

       
        
class Notice(PNU_Crawling):
    def __init__(self,category,url,driver_path):
        self.category=category
        self.date_list=[]
        self.notice_list=[]
        super().__init__(url,driver_path)
        self.target = None


    def target_id(self):
        super().setting_driver()
        self.target = self.soup.find('div', {'id': 'menu14870_obj250'})
        
        return self.target

    
    def collect_data(self):
        if self.target_id() :
            td_dates = self.soup.find_all('td', class_="_artclTdRdate")
            td_notices = self.soup.find_all('a', class_="artclLinkView")
            for td_date, td_notice in zip(td_dates, td_notices):
                self.date_list.append(td_date.get_text(strip=True))
                cleaned_notice = td_notice.get_text(strip=True).replace('\n', '').replace('\t', '').strip()
                self.notice_list.append(cleaned_notice)
            return self.date_list , self.notice_list    
                
        
    def sort_data(self) :
        self.collect_date,self.collect_notice = self.collect_data()
        self.data = {'공지': self.collect_date, '작성일': self.collect_notice}
        df = pd.DataFrame(self.data)        
        return df.to_csv('Notice_data.csv',index=False)

class Schedule(PNU_Crawling):
    def __init__(self,category,url,driver_path):
        self.category=category
        self.date_list=[]
        self.schdule_list=[]
        super().__init__(url,driver_path)
        self.target = None

    def target_class(self):
        super().setting_driver()
        if self.soup.find('section', class_='sec-smart-schedule'):
            self.target = self.soup.find('ul', class_='schedule-list')
        return self.target
    



    def collect_data(self):
       if self.target_class() :
            schedule_dates = self.target.find_all('span',class_='list-date')
            schedule_subjects = self.target.find_all('span',class_='subject')
            for schedule_date, schedule_subject in zip(schedule_dates,schedule_subjects):
                self.date_list.append(schedule_date)
                self.schdule_list.append(schedule_subject)
        
            return self.date_list, self.schdule_list
    
    def sort_data(self):
        self.collect_date,self.collect_schedule = self.collect_data()
        self.data = {'날짜': self.collect_date, '일정': self.collect_schedule}
        df = pd.DataFrame(self.data)        
        return df.to_csv('Schedule_data.csv',index=False)
        



def main():
    url = 'https://eec.pusan.ac.kr/eehome/14870/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZWVob21lJTJGMjY1MCUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEJTI2cGFnZSUzRDElMjZzcmNoV3JkJTNEJTI2cmdzQmduZGVTdHIlM0QlMjZiYnNDbFNlcSUzRCUyNnJnc0VuZGRlU3RyJTNEJTI2'
    category ="Notice"
    # category = "Schedule" #category는 어디에 사용할지 고민
    # url = 'https://onestop.pusan.ac.kr/login#target_href1'
    driver_path = '/Users/hongseoggi/hong/chromedriver'
    connect = PNU_Crawling(url,driver_path)  
    n = Notice(category,url,driver_path)
    # l = Schedule(category,url,driver_path)

    try:
        connect.setting_driver()
        print(n.sort_data())
        connect.close_driver()
        

    except:
        print("서버를 연결할 수 없습니다.")


        
    


if __name__ == '__main__':
    main()


       