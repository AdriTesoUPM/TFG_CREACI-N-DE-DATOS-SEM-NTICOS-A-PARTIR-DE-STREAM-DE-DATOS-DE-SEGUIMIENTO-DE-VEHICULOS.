from database import DataBase
from matplotlib import pyplot as plt
import numpy as np
from datetime import date, timedelta, datetime


def scatter_last_month():
    database = DataBase()

    data = np.array(database.select_last_month())

    sp = np.array(database.select_sp())

    plt.gca().set_facecolor('white')
    plt.scatter(data[:, 1], data[:, 0], c='black')
    plt.scatter(sp[:, 1], sp[:, 0], c='aqua')
    plt.show()


def scatter_dayselect():
    database = DataBase()

    date_ = str(input("""Insert initial date [dd/mm/yyyy]:     Or     Insert amount of backdays (from now):

        """))
    if date_:
        if len(date_) == len('dd/mm/yyyy'):
            date_ = datetime.strptime(date_, '%d/%m/%Y')
        elif len(date_) <= 7:
            date_ = date.today() + timedelta(days=-int(date_))

    date_end = str(input("""Insert end date [dd/mm/yyyy]:     Or     Insert amount of (+/-) days (from initial date):

        """))
    if date_end:
        if len(date_end) == len('dd/mm/yyyy'):
            date_end = datetime.strptime(date_, '%d/%m/%Y')
        elif len(date_end) <= 7:
            date_end = date_ + timedelta(days=int(date_end))

    if date_end < date_:
        date_1 = date_end
        date_end = date_
        date_ = date_1

    data = np.array(database.select_dayselect(str(date_), str(date_end)))

    sp = np.array(database.select_sp())

    if len(data) > 0:
        plt.gca().set_facecolor('white')
        plt.scatter(data[:, 1], data[:, 0], c='black')
        plt.scatter(sp[:, 1], sp[:, 0], c='aqua')
        plt.show()

    else:
        print(f"No data for {date_}")
