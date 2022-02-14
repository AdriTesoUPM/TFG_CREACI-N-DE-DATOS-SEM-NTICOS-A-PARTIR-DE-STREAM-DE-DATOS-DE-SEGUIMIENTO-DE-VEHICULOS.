from database import DataBase


def search():
    print("Type 'exit' to Exit")
    end = True
    while end:
        end = DataBase().show_()
