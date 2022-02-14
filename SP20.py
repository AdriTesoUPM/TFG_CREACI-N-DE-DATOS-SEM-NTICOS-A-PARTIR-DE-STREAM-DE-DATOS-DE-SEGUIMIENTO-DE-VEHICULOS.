import clust
from datetime import timedelta, date, datetime
from database import DataBase
import numpy as np
import matplotlib.pyplot as plt

database = DataBase()


def manual():
    date_ = str(input("""Insert date [dd/mm/yyyy]:     Or     Insert amount of backdays (from now):

    """))
    if date_:
        if len(date_) == len('dd/mm/yyyy'):
            date_ = datetime.strptime(date_, '%d/%m/%Y')
        elif len(date_) <= 7:
            date_ = date.today() + timedelta(days=-int(date_))

        users_past = database.select_users_past(date_)
        cls = []

        all_sp = list(database.select_sp())

        if users_past:
            cls = clust.clustering_20(users_past, 150, 500)
        if cls:
            sp = clust.sec_depur(cls, 150)

            sp = np.array(sp)
            all_sp = np.array(all_sp)
            plt.gca().set_facecolor('white')
            plt.scatter(all_sp[:, 1], all_sp[:, 0], c='black')
            plt.scatter(sp[:, 1], sp[:, 0], c='aqua')
            plt.show()
            all_sp = np.array(all_sp).tolist()
            all_sp.extend(sp)
        else:
            print(f"No Data for {date_}")
        if all_sp:
            all_sp = clust.sec_depur(all_sp, 30)

        return all_sp


def auto():
    all_sp = []
    for days in range(600, 0, -20):

        pastdate = date.today() + timedelta(days=-days)
        print(pastdate, days)
        users_past = database.select_users_past(pastdate)
        cls = []

        if users_past:
            cls = clust.clustering_past(users_past, 100, 500)
        if cls:
            sp = clust.sec_depur(cls, 150)
            all_sp.extend(sp)
        if all_sp:
            all_sp = clust.sec_depur(all_sp, 150)

    all_sp_ = all_sp
    all_sp = clust.sec_depur(all_sp, 250)
    all_sp = np.array(all_sp)
    all_sp_ = np.array(all_sp_)
    plt.gca().set_facecolor('white')
    plt.scatter(all_sp_[:, 1], all_sp_[:, 0], c='black')
    plt.scatter(all_sp[:, 1], all_sp[:, 0], c='aqua')
    plt.show()

    return all_sp
