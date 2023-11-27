from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://eec.pusan.ac.kr/eehome/14870/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZWVob21lJTJGMjY1MCUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEJTI2cGFnZSUzRDElMjZzcmNoV3JkJTNEJTI2cmdzQmduZGVTdHIlM0QlMjZiYnNDbFNlcSUzRCUyNnJnc0VuZGRlU3RyJTNEJTI2'
response = requests.get(url)

html = response.text 
soup = BeautifulSoup(html, 'html.parser')

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

class Notice(PNU_Crawling):

        def extract_data(self): 
            self.connect()  

            if self.condition:
                category = 'notice'
                data_list=[]
                new_posts = soup.find_all('tr', class_='headline')
                for post in new_posts:
                    post_content = post.find('strong').text.strip()
                    data_list.append(post_content)
                df = pd.DataFrame(data_list, columns=['새글'])
                self.make_csv_file(category, df)        
                
            else:
                print("연결할 수 없습니다.")


def main():
    notice_data = Notice()
    notice_data.extract_data()

if __name__ == '__main__':
    main()
                
