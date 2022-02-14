import SP20
from database import DataBase
import clust
import matplotlib.pyplot as plt
import numpy as np
import datetime

database = DataBase()


def twoyears_input():

    database.remove_allSP()
    sp = SP20.auto()
    i = 0

    for point in sp:
        lon = point[0]
        lon = str(lon)
        lat = point[1]
        lat = str(lat)

        i = i + 1
        cls = "C - " + str(i)

        special_site = database.select_users_compr(lon, lat)

        desc = (str(special_site[3]) + "  ID " + str(special_site[0]) + "  MAT " + str(special_site[1])).replace(".",
                                                                                                                 "")

        database.addSP(lat, lon, cls, desc)


def month_input(input_):

    global new_sp, cls
    if input_ == "1":
        date_ = str(input("""Insert date [dd/mm/yyyy]:     Or     Insert amount of backdays (from now):

            """))
        if date_:
            if len(date_) == len('dd/mm/yyyy'):
                date_ = datetime.datetime.strptime(date_, '%d/%m/%Y')
            elif len(date_) <= 7:
                date_ = datetime.date.today() + datetime.timedelta(days=-int(date_))

            users_past = database.select_users_past(date_)
            if users_past:
                cls = clust.clustering_20(users_past, 150, 500)
            if cls:
                new_sp = clust.sec_depur(cls, 150)

    sp = database.select_sp()

    if input_ == "0":
        new_sp = clust.clustering()

    plt.gca().set_facecolor('white')
    plt.scatter(np.array(sp)[:, 1], np.array(sp)[:, 0], c='black')
    plt.scatter(np.array(new_sp)[:, 1], np.array(new_sp)[:, 0], c='aqua')
    plt.show()

    for point in new_sp:

        sp_act = clust.sec_depur(sp + (point,), 300)

        if len(sp_act) > len(sp):
            lon = str(point[0])
            lat = str(point[1])

            special_site = database.select_users_compr(lon, lat)

            cls = "C - " + str(len(database.select_sp()) + 1)

            desc = (str(special_site[3]) + "  ID " + str(special_site[0]) + "  MAT " + str(special_site[1])).replace(
                ".",
                "")

            print(f"Se ha dado de alta {point} en la BBDD.")
            database.addSP(lat, lon, cls, desc)

        else:
            print(f"El punto {point} pertenece a un cúster ya dado de alta.")


