import gmplot
from database import DataBase
import numpy as np
import webbrowser
from datetime import datetime, date, timedelta
from os import system, name, getcwd

database = DataBase()
sp = np.array(database.select_sp_name())
path = getcwd()


def visualization():
    global i, ids
    color = ['white', 'yellow', 'orange', 'red', 'purple', 'lightblue', 'lightgreen', 'green',
             'darkgreen', 'gold']
    date_ = str(input("""Insert date [dd/mm/yyyy]:     Or     Insert amount of backdays (from now):

    """))
    if date_:
        if len(date_) == len('dd/mm/yyyy'):
            date_ = datetime.strptime(date_, '%d/%m/%Y')
        elif len(date_) <= 7:
            date_ = date.today() + timedelta(days=-int(date_))

        date_ = str(date_)

        data = database.select_mat_fromroutes(date_)

        system('cls' if name == 'nt' else 'clear')

        print(f"""Day {date_}.""")
        if data:
            print("")
            for i in range(0, len(data)):
                print(i + 1, (data[i])[0])
            print("")
            mat = input("""
Select mat: """)

            system('cls' if name == 'nt' else 'clear')
            if int(mat) <= i + 1:
                mat = (data[int(mat) - 1])[0]

                route_data = database.select_data_fromroutes(date_, mat)
                route_data = np.array((route_data[0])[1:])

                end = False
                while not end:
                    print(
                        f"""Date: {route_data[0]} 
Desde: {route_data[1]} 
Hasta: {route_data[2]} 
Matricula: {route_data[3]} 
Número de Segmentos: {route_data[4]}
ID origen: {route_data[5]}
ID final: {route_data[6]}
Número de Paradas: {route_data[7]}  
Duración Viajes: {route_data[8]} 
Duración Paradas: {route_data[9]}
Secuencia Paradas: {route_data[10]}  
Kilómetros: {route_data[11]} 
Vmax: {route_data[12]} 
Vavg: {route_data[13]} 
            """)
                    print("")
                    print("Segments to draw: [x] [x-y] [0 = complete route] [exit to Exit]")
                    print("\n")

                    seg = input("Select segments to draw: ")
                    print('______________________________')
                    system('cls' if name == 'nt' else 'clear')

                    # SELECCION DE SEGMENTOS A DIBUJAR

                    if len(seg) == 1 or len(seg) == 2:
                        if int(seg) <= route_data[4]:
                            if seg == "0":

                                segs = []
                                for i in range(1, route_data[4] + 1):
                                    seg_data = database.select_data_fromsegments(date_, mat, i)
                                    seg_data = np.array((seg_data[0])[1:])
                                    print(
                                        f"""Dateseg: {seg_data[0]} 
Desde: {seg_data[1]} 
Hasta: {seg_data[2]} 
Número de Segmento en Ruta: {seg_data[3]} 
ID origen: {seg_data[4]}
ID final: {seg_data[5]}
Matrícula: {seg_data[6]}
Special Point Origen: {seg_data[7]}   
Special Point Final: {seg_data[8]}  
Kilómetros: {seg_data[9]} 
Vmax: {seg_data[10]} 
Vavg: {seg_data[11]} 
Observaciones: {seg_data[12]} 
    
                """)
                                    idorg = seg_data[4]
                                    idend = seg_data[5]

                                    ids = database.select_data_frommovements(idorg, idend, mat)
                                    segs.append(ids)

                                input("\nEnter to continue")

                                i = int(len(ids) / 2)
                                gmap = gmplot.GoogleMapPlotter((ids[i])[0], (ids[i][1]), 11)

                                i = 0
                                for ids in segs:
                                    ids = np.array(ids)
                                    j = 0
                                    for point in ids:
                                        gmap.scatter([point[0]], [point[1]], color[i], label=f'{i + 1}.{j}', size=50)
                                        j += 1
                                    gmap.plot(ids[:, 0], ids[:, 1], color[i], size=50)
                                    i += 1
                                    if i == len(color):
                                        i = 0

                                for i in sp:
                                    gmap.scatter([i[0]], [i[1]], 'blue', label=i[2].replace(" ", ""), size=50)
                                    gmap.scatter([i[0]], [i[1]], 'blue', size=150, marker=False)

                                gmap.draw(f"{path}/map_.html")

                                webbrowser.open_new_tab(f'{path}/map_.html')

                            else:
                                seg = int(seg)
                                seg_data = database.select_data_fromsegments(date_, mat, seg)
                                seg_data = np.array((seg_data[0])[1:])
                                print(
                                    f"""Dateseg: {seg_data[0]} 
Desde: {seg_data[1]} 
Hasta: {seg_data[2]} 
Número de Segmento en Ruta: {seg_data[3]} 
ID origen: {seg_data[4]}
ID final: {seg_data[5]}
Matrícula: {seg_data[6]}
Special Point Origen: {seg_data[7]}   
Special Point Final: {seg_data[8]}  
Kilómetros: {seg_data[9]} 
Vmax: {seg_data[10]} 
Vavg: {seg_data[11]} 
Observaciones: {seg_data[12]} 

                """)
                                idorg = seg_data[4]
                                idend = seg_data[5]

                                ids = database.select_data_frommovements(idorg, idend, mat)
                                ids = np.array(ids)

                                i = int(len(ids) / 2)

                                gmap = gmplot.GoogleMapPlotter((ids[i])[0], (ids[i][1]), 11)
                                for i in sp:
                                    gmap.scatter([i[0]], [i[1]], 'blue', label=i[2].replace(" ", ""), size=150)
                                    gmap.scatter([i[0]], [i[1]], 'blue', size=250, marker=False)
                                j = 0
                                for point in ids:
                                    gmap.scatter([point[0]], [point[1]], color[seg - 1], label=f'{j}', size=50)
                                    j += 1
                                gmap.plot(ids[:, 0], ids[:, 1], f'{color[seg - 1]}', label=f'{seg}', size=50)
                                gmap.draw(f"{path}/map_.html")

                                webbrowser.open_new_tab(f'{path}/map_.html')

                    elif seg != 'exit':
                        ch = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]
                        range_ = ""
                        for i in seg:
                            if i in ch:
                                range_ += i

                        range_ = range_.split("-")
                        if len(range_) > 1:
                            if int(range_[1]) <= route_data[4]:
                                segs = []
                                for i in range(int(range_[0]), int(range_[1]) + 1):
                                    seg_data = database.select_data_fromsegments(date_, mat, i)
                                    seg_data = np.array((seg_data[0])[1:])
                                    print(
                                        f"""Dateseg: {seg_data[0]} 
Desde: {seg_data[1]} 
Hasta: {seg_data[2]} 
Número de Segmento en Ruta: {seg_data[3]} 
ID origen: {seg_data[4]}
ID final: {seg_data[5]}
Matrícula: {seg_data[6]}
Special Point Origen: {seg_data[7]}   
Special Point Final: {seg_data[8]}  
Kilómetros: {seg_data[9]} 
Vmax: {seg_data[10]} 
Vavg: {seg_data[11]} 
Observaciones: {seg_data[12]} 
                
                """)
                                    idorg = seg_data[4]
                                    idend = seg_data[5]

                                    ids = database.select_data_frommovements(idorg, idend, mat)
                                    segs.append(ids)

                                input("\nEnter to continue")

                                i = int(len(ids) / 2)
                                gmap = gmplot.GoogleMapPlotter((ids[i])[0], (ids[i][1]), 11)

                                i = int(range_[0]) - 1
                                for ids in segs:
                                    ids = np.array(ids)
                                    j = 0
                                    for point in ids:
                                        gmap.scatter([point[0]], [point[1]], color[i], label=f'{i + 1}.{j}', size=50)
                                        j += 1
                                    gmap.plot(ids[:, 0], ids[:, 1], color[i], size=50)
                                    i += 1
                                    if i == len(color):
                                        i = int(range_[0]) - 1

                                for i in sp:
                                    gmap.scatter([i[0]], [i[1]], 'blue', label=i[2].replace(" ", ""), size=150)
                                    gmap.scatter([i[0]], [i[1]], 'blue', size=250, marker=False)

                                gmap.draw(f"{path}/map_.html")

                                webbrowser.open_new_tab(f'{path}/map_.html')

                    elif seg == 'exit':
                        end = True

        else:
            print(f"No data for {date_}")
