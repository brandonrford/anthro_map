# -*- coding: utf-8 -*-
"""map.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K2vyhIYiiX2RTCg3ZSk6_xe8_InPsOUt
"""

#installing the latest version of folium
!pip install git+https://github.com/python-visualization/folium@master

#mounting google drive
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

#imports
import folium 
import pandas as pd
import json
from folium import plugins
import math

#defining data variable
data = pd.read_csv('map_data.csv') #set your own data here

#see if there's any missing data in the DataField
print("Count of missing data : \n\n", data.isnull().sum())

#importing json and initializing mapa variable
import json

mapa = folium.Map(location=[10,0], tiles='OpenStreetMap', zoom_start=2)

with open("map_data.geojson") as f:
          map_data = json.load(f)

#creating legend
import branca
legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 320px;
    left: 75px;
    width: 200px;
    height: 250px;
    z-index:9999;
    font-size:14px;
    ">
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/chicken.png" alt="Small Species Icon" width="25" height="25"></a>&emsp;Small Species</p>
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/pig.png" alt="Pigs Icon" width="25" height="25"></a>&emsp;Pigs</p>
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/sheep.png" alt="Ovis Icon" width="25" height="25"></a>&emsp;Ovis</p>
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/horse.png" alt="Equines Icon" width="25" height="25"></a>&emsp;Equines</p>
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/reindeer.png" alt="Reindeer Icon" width="25" height="25"></a>&emsp;Reindeer</p>
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/camel.png" alt="Camels Icon" width="25" height="25"></a>&emsp;Camels</p>
    <p><a><img src="https://raw.githubusercontent.com/brandonrford/brandonrford.github.io/main/icons/cow.png" alt="Bovines Icon" width="25" height="25"></a>&emsp;Bovines</p>
</div>
<div style="
    position: fixed;
    bottom: 300px;
    left: 50px;
    width: 180px;
    height: 300px;
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    filter: blur(8px);
    -webkit-filter: blur(8px);
    opacity: 0.7;
    ">
</div>
{% endmacro %}
"""

legend = branca.element.MacroElement()
legend._template = branca.element.Template(legend_html)

#setting default icon size (also change this in the for loop)
icon_size = (30, 30)

#map icon for loop
for feature in map_data['features']:
    lon, lat = feature['geometry']['coordinates']
    icon_url = feature['properties']['icon_url'] #this is all taken from the geojson file, to make mine, i used https://www.convertcsv.com/csv-to-geojson.htm
    popup = "Focal Year: " + str(feature['properties']['focal_year']) + "<br>Role of Gods: " + feature['properties']['roleofgods_label'] + "<br>Animals Hunted: " + feature['properties']['animalshunted_label'] + "<br>Religion: " + feature['properties']['religion_label'] #appear on click
    tooltip = feature['properties']['society_name'] #appear on hover
    
    icon = folium.features.CustomIcon(icon_url,
                                      icon_size=(30, 30))
    
    marker = folium.map.Marker([lat, lon], icon=icon,
                               popup=folium.Popup(popup,
                                                  min_width=150,
                                                  max_width=150),
                               tooltip=folium.map.Tooltip(tooltip))
    mapa.add_child(marker)

mapa.get_root().add_child(legend) #adds legend to the html map

mapa.save('mapa.html') #saves map to html
mapa