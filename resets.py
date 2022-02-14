from database import DataBase

database = DataBase()


def reset_segments():
    database.remove_allseg()


def reset_routes():
    database.remove_allroutes()


def reset_specialsites():
    database.remove_allsp()
