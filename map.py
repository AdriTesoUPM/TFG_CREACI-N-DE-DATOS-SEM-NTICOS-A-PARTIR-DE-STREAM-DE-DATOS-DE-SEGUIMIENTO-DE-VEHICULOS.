from os import getcwd

import gmplot
from database import DataBase
import numpy as np
import webbrowser

database = DataBase()

sp = np.array(database.select_sp_name())

path = getcwd()


def mapping(place):

    global gmap

    if place == '0':
        gmap = gmplot.GoogleMapPlotter(39.9902498, -3.9255631, 7)

    if place == '1':
        gmap = gmplot.GoogleMapPlotter(47.1939666, 19.2374724, 7)

    for i in sp:
        gmap.scatter([i[0]], [i[1]], 'blue', label=i[2].replace(" ", ""), size=50)
    gmap.draw(f"{path}/map.html")

    webbrowser.open_new_tab(f'{path}/map.html')
