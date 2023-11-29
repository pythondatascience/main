import requests
from bs4 import BeautifulSoup
import folium as g
import googlemaps as m

#googlemap setting
gmaps_key = 'AIzaSyA7PxgOBSjKmZ63DhoJOE-PJR4gbm4WYNw'
gmaps = m.Client(key=gmaps_key)
tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
attr = "Google"

# url, key=5291107000 : keumjunggu7, key=5200051000 : 51
url = 'http://apis.data.go.kr/6260000/BusanBIMS/busInfoByRouteId'
params ={'serviceKey' : 'Fc0bdu/n6BeHierLzLLkEkCEhc70zpeD92N0vcWYA3Pv/i22Bl8Z9yIGLv8AwjMj8SVDTsXZLohzxgATlYcvIQ==', 'lineid' : 5200051000}
response = requests.get(url, params=params, verify=False)

#lxml
soup = BeautifulSoup(response.text, features="xml")

#items
items = soup.find_all('item')

#bus_info
bus_info = []

#bus_stop, bus_gps
for bus in items:
    bus_stop = bus.find('bstopnm').get_text()    
    
    if bus.find('lat') == None and bus.find('lin') == None :
        print(end='')
    else:
        x_pos = bus.find('lat').get_text()
        y_pos = bus.find('lin').get_text()
        bus_direction = int(bus.find('direction').get_text())
        if bus_direction == 3 or bus_direction == 4 :
            is_stop = True
            is_up = False
        elif bus_direction == 1 :
            is_stop = False
            is_up = True
        else :
            is_stop = False
            is_up = False

        bus_info = bus_info + [[bus_stop, [x_pos, y_pos], is_stop, is_up]]

print(bus_info)

#google_map
map = g.Map(location=[35.1795543, 129.0756416], zoom_start=12, tiles=tiles, attr=attr)

#pin_map
for i in range(len(bus_info)) :
    marker = g.Marker(bus_info[i][1], popup='campus seven', icon = g.Icon(color='blue'))
    marker.add_to(map)

map