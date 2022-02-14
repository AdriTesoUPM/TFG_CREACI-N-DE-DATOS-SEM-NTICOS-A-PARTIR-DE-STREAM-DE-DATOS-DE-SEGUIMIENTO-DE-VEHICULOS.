import itertools

from seg_toSQL import seg_toSQL
from route_toSQL import route_toSQL
from database import DataBase
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta, datetime
from os import system, name

database = DataBase()


def segments(input_):
    global unique_mats, date_, seg, parados, seg_id, i, dat

    system('cls' if name == 'nt' else 'clear')

    sp = np.array(database.select_sp())

    if input_ == "1":
        date_ = str(input("""Insert date [dd/mm/yyyy]:     Or     Insert amount of backdays (from now):
    
            """))
        if date_:
            if len(date_) == len('dd/mm/yyyy'):
                date_ = datetime.strptime(date_, '%d/%m/%Y')
            elif len(date_) <= 7:
                date_ = date.today() + timedelta(days=-int(date_))

            date_ = date_.strftime('%Y-%m-%d %H:%M:%S')
            mats = database.select_mat_0(date_)
            unique_mats_ = []

            for mat in mats:

                if mat not in unique_mats_:
                    if len(mat[0]) <= 7:
                        unique_mats_.append(mat)

            system('cls' if name == 'nt' else 'clear')
            print("Mat Selection:   [0 for all]")

            for i in range(0, len(unique_mats_)):
                print(f"{i+1}. {(unique_mats_[i])[0]}")

            mat = input("Select mat: ")
            system('cls' if name == 'nt' else 'clear')

            if int(mat) <= i + 1:
                if mat == "0":
                    unique_mats = unique_mats_
                if mat != "0":
                    unique_mats = [unique_mats_[int(mat)-1]]
            else:
                unique_mats = []

    if input_ == "0":
        date_ = date.today().strftime('%Y-%m-%d %H:%M:%S')

        mats = database.select_mat_0(date_)
        unique_mats = []

        for mat in mats:

            if mat not in unique_mats:
                if len(mat[0]) <= 7:
                    unique_mats.append(mat)

    if unique_mats:

        database.remove_seg(date_)
        database.remove_route(date_)

        print(date_)

        for mat in unique_mats:
            mat = str(mat)
            mat = mat.replace(",", "")

            time = datetime.combine(datetime.strptime(date_, '%Y-%m-%d %H:%M:%S'), datetime.min.time())
            time_1 = time + timedelta(minutes=5)

            time = time.strftime('%Y-%m-%d %H:%M:%S')
            time_1 = time_1.strftime('%Y-%m-%d %H:%M:%S')

            if input_ == "1":
                actual = (datetime.strptime(date_, '%Y-%m-%d %H:%M:%S') +
                          timedelta(hours=23, minutes=59)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            route = []
            route_id = []
            num_seg = len(route)
            Num = 1

            notnow = True
            while notnow:

                if len(route) > num_seg:
                    seg = np.array(seg)
                    parados = np.array(parados)

                    Num = seg_toSQL(seg_id, Num, date_)

                    """plt.scatter(seg[:, 1], seg[:, 0], c='orange')
                    plt.plot(seg[:, 1], seg[:, 0], c='orange')
                    plt.scatter(sp[:, 1], sp[:, 0], c='black')
                    plt.scatter(parados[:, 1], parados[:, 0], c='red')
                    plt.show()"""

                    num_seg = len(route)

                if datetime.strptime(time, '%Y-%m-%d %H:%M:%S') >= datetime.strptime(actual, '%Y-%m-%d %H:%M:%S'):
                    notnow = False

                    route = list(itertools.chain(*route))

                    if not route:
                        if dat:
                            pos = [dat[0], dat[1]]
                            id = dat[4]
                            route.append(pos)
                            route_id.append(id)

                    route_toSQL(route_id, date_)

                    """if route:
                        route = np.array(route)
                        plt.scatter(sp[:, 1], sp[:, 0], c='black')
                        plt.scatter(route[:, 1], route[:, 0], c='lightblue')
                        plt.plot(route[:, 1], route[:, 0], c='lightblue')
                        plt.show()"""
    
                    route = np.array(route).tolist()
                    seg = np.array(seg).tolist()
                    parados = np.array(parados).tolist()

                seg = []
                seg_id = []
                parados = []

                parado = False

                while not parado:

                    dat = database.select_seg(mat, time, time_1)

                    if dat:
                        print(mat, time, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dat[2], dat[5])

                        if dat[2] != 'Parado':
                            pos = [dat[0], dat[1]]
                            seg.append(pos)
                            seg_id.append(dat[4])

                        if dat[2] == 'Parado':
                            parado = True

                            if seg and datetime.strptime(time, '%Y-%m-%d %H:%M:%S') <= datetime.strptime(actual,
                                                                                                         '%Y-%m-%d %H:%M:%S'):
                                pos = [dat[0], dat[1]]
                                seg.append(pos)
                                seg_id.append(dat[4])
                                parados.append(pos)
                                route.append(seg)
                                route_id.append(seg_id)

                    if datetime.strptime(time, '%Y-%m-%d %H:%M:%S') >= datetime.strptime(actual, '%Y-%m-%d %H:%M:%S'):
                        parado = True
                        if dat:
                            if dat[2] != 'Parado' and dat[5] != '0.0':
                                pos = [dat[0], dat[1]]
                                seg.append(pos)
                                seg_id.append(dat[4])
                                parados.append(pos)
                                route.append(seg)
                                route_id.append(seg_id)

                    time = (datetime.strptime(time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=5)).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    time_1 = (datetime.strptime(time_1, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=5)).strftime(
                        '%Y-%m-%d %H:%M:%S')
