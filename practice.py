
import requests
from bs4 import BeautifulSoup

url = 'https://onestop.pusan.ac.kr/page?menuCD=000000000000386'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table_body = soup.find('tbody', {'id': 'board-default'})
rows = table_body.find_all('tr')

for row in rows:
    columns = row.find_all('td')
    if columns:  # 데이터가 있는 행만 처리
        print(columns)    
    
