# sudo pip3 install requests
# sudo pip3 install beautifulsoup4
# sudo pip3 install lxml
# sudo pip3 install folium
# sudo pip3 install googlemaps

## 독창적인 부분
# 1. 공공기관 데이터의 api를 받아 실시간으로 버스의 위치 확인 가능
# 2. 버스의 상행, 하행의 방향 뿐만 아니라 정차 상태도 확인 가능
# 3. 부산대 순환버스에만 국한되는것이 아니라 버스 노선 id와 기준 좌표 수정시 다른 노선의 위치도 확인 가능(아래의 주석 참조)

## 참조문헌
# ChatGPT : 코드의 대략적인 구조(클래스 형태 구현 측면에서)
# https://www.data.go.kr/iim/api/selectAPIAcountView.do : OpenAPI활용가이드_부산버스정보시스템_v2.0.docx 참고 (api키, 버스 실시간 좌표, 방향)
# https://www.data.go.kr/data/15092750/openapi.do#tab_layer_detail_function : 샘플 코드 > Python 쪽 참조 (데이터 가져오기)
# https://minjoo-happy-blog.tistory.com/34 : 파싱 참조
# https://continuous-development.tistory.com/entry/Python-%EC%8B%9C%EA%B0%81%ED%99%94-%EC%82%AC%EC%9A%A9%EB%B2%95-folium-%EC%9D%84-%ED%86%B5%ED%95%9C-%EC%A7%80%EB%8F%84-%EC%8B%9C%EA%B0%81%ED%99%94-%EB%B0%8F-%EB%A7%88%EC%BB%A4marker-%EC%B0%8D%EA%B8%B0 : folium 기초 명령어(핀 찍기, 지도 출력, 저장)
# https://wooiljeong.github.io/python/folium-google-tiles/ : folium 지도를 googlemap으로 설정

import requests
from bs4 import BeautifulSoup
import folium as g
import googlemaps as m
import subprocess

# 클래스 구조 : Chatgpt
class BusanMap:
    def __init__(self, gmaps_key, bus_api_key):
        self.gmaps_key = gmaps_key
        self.bus_api_key = bus_api_key
        self.gmaps = m.Client(key=gmaps_key)
        self.tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
        self.attr = "Google"
        self.bus_info = []

    def get_bus_info(self, line_id):
        url = 'http://apis.data.go.kr/6260000/BusanBIMS/busInfoByRouteId'
        params = {'serviceKey': self.bus_api_key, 'lineid': line_id}
        response = requests.get(url, params=params, verify=False)
        soup = BeautifulSoup(response.text, features="xml")
        items = soup.find_all('item')
        turn_check = 1     

         ## Start here (개발담당  : 최정민) - 회차 여부 체크(회차지점 이전 : 상행, 이후: 하행), 버스 이동 방향 체크(상행, 하행, 정차)   
        
        for bus in items:
          bus_stop = bus.find('bstopnm').get_text()
          bus_turn = int(bus.find('rpoint').get_text())

          if bus_turn == turn_check : # 회차 여부 체크
            turn_check -= 1 

          if bus_stop == '부산대제2도서관' : bus_stop = '새벽벌도서관'
          elif bus_stop == '부산대음악관' : bus_stop = '학생회관' # 이름 정정

          if bus.find('lat') is None or bus.find('lin') is None:
              continue

          x_pos = bus.find('lat').get_text()
          y_pos = bus.find('lin').get_text()
          bus_direction = int(bus.find('direction').get_text())

          if bus_direction == 0: # 버스 정차
              is_stop = True
              is_up = False
          elif bus_direction in [1, 3]: # 버스 상행
              is_stop = False 
              if turn_check <= 0:   
                is_up = False
              else:
                is_up = True              
          else: # 버스 하행
              is_stop = False
              is_up = False
            
          if bus_stop != '신한은행' : # 종점 : 신한은행
            self.bus_info = self.bus_info + [[bus_stop, [x_pos, y_pos], is_stop, is_up, turn_check]]       
       
        return self.bus_info   

        ## end here (개발담당  : 최정민)

    
    def generate_map(self, center, zoom_start):
        self.bus_map = g.Map(location=center, zoom_start=zoom_start, tiles=self.tiles, attr=self.attr)

    ## Start here (개발담당  : 최정민) - 상행, 하행, 정차 여부 핀으로 표시 

        for i in range(len(self.bus_info)):
            if self.bus_info[i][2] == True:
                marker = g.Marker(self.bus_info[i][1], popup=g.Popup((self.bus_info[i][0]+'(정차)'), min_width=200, max_width=200), icon=g.Icon(color='black'))
                marker.add_to(self.bus_map)
            else :
                if self.bus_info[i][3] == True:
                    marker = g.Marker(self.bus_info[i][1], popup=g.Popup((self.bus_info[i][0]+'(상행)'), min_width=200, max_width=200), icon=g.Icon(color='red'))
                    marker.add_to(self.bus_map)
                else :
                    marker = g.Marker(self.bus_info[i][1], popup=g.Popup((self.bus_info[i][0]+'(하행)'), min_width=200, max_width=200), icon=g.Icon(color='blue'))
                    marker.add_to(self.bus_map)

        return self.bus_map

    ## end here (개발담당  : 최정민)

gmaps_key =  'AIzaSyA7PxgOBSjKmZ63DhoJOE-PJR4gbm4WYNw'
bus_api_key = 'Fc0bdu/n6BeHierLzLLkEkCEhc70zpeD92N0vcWYA3Pv/i22Bl8Z9yIGLv8AwjMj8SVDTsXZLohzxgATlYcvIQ=='
line_id = 5291107000 # 5291107000 : keumjunggu7, key=5200051000 : 51


bs = BusanMap(gmaps_key, bus_api_key)
bs.get_bus_info(line_id)
bs.generate_map([35.231944, 129.083333], 15) # busan_entire : [35.1795543, 129.0756416, zoom : 12] #busan_university : [35.231944, 129.083333, zoom : 15]
bs.bus_map.save('bus_map.html')

html_path = './bus_map.html'
subprocess.run(['firefox',html_path]) #Firefox
# subprocess.run(['chrome',html_path]) #Chrome
# subprocess.run(['open',html_path]) #MacOs