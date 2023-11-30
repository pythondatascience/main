import requests
from bs4 import BeautifulSoup
import folium as g
import googlemaps as m

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
        
        for bus in items:
          bus_stop = bus.find('bstopnm').get_text()
          bus_turn = int(bus.find('rpoint').get_text())

          if bus_turn == turn_check : #check turn
            turn_check -= 1 

          if bus_stop == '부산대제2도서관' : bus_stop = '새벽벌도서관'
          elif bus_stop == '부산대음악관' : bus_stop = '학생회관' #name correction

          if bus.find('lat') is None or bus.find('lin') is None:
              continue

          x_pos = bus.find('lat').get_text()
          y_pos = bus.find('lin').get_text()
          bus_direction = int(bus.find('direction').get_text())

          if bus_direction == 0: #bus not move
              is_stop = True
              is_up = False
          elif bus_direction in [1, 3]: #bus direction : up
              is_stop = False 
              if turn_check <= 0:   
                is_up = False
              else:
                is_up = True              
          else: #bus direction : down
              is_stop = False
              is_up = False
            
          if bus_stop != '신한은행' : #신한은행 is last stop : don't care
            self.bus_info = self.bus_info + [[bus_stop, [x_pos, y_pos], is_stop, is_up, turn_check]]       
       
        return self.bus_info   

    def generate_map(self, center, zoom_start):
        self.bus_map = g.Map(location=center, zoom_start=zoom_start, tiles=self.tiles, attr=self.attr)
        
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


gmaps_key =  'AIzaSyA7PxgOBSjKmZ63DhoJOE-PJR4gbm4WYNw'
bus_api_key = 'Fc0bdu/n6BeHierLzLLkEkCEhc70zpeD92N0vcWYA3Pv/i22Bl8Z9yIGLv8AwjMj8SVDTsXZLohzxgATlYcvIQ=='
line_id = 5200051000 #5291107000 : keumjunggu7, key=5200051000 : 51

bs = BusanMap(gmaps_key, bus_api_key)

#print(bs.get_bus_info(line_id))
bs.get_bus_info(line_id)
bs.generate_map([35.231944, 129.083333], 16) #busan_entire : [35.1795543, 129.0756416, zoom : 12] #busan_university : [35.231944, 129.083333, zoom : 16]
bs.bus_map.save('bus_map.html')
