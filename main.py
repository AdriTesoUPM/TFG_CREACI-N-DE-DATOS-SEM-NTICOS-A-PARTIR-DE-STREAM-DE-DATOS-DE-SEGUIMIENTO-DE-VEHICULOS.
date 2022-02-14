from addto_SQL import twoyears_input, month_input
import SP20
from os import system, name
import map
import segments
import search
import scattering
import visualizado
from time import sleep
import database
import resets

sc_1 = """
        MENU

[0] Initiate.
[1] Settings.
[2] Credits.
[3] Exit.

"""

sc_2 = """
        FUNCTIONS
        
[0] Routing.
[1] Clustering SP.
[2] Mapping.
[3] Scatter Search.
[4] Search in Database.
[5] Reset DDBB.
[6] Back.

"""

sc_3 = """
        CLUSTERING SP

[0] Month input.
[1] Day selection input.
[2] Reset all SP.
[3] Search for clusters.
[4] Back.

"""

sc_4 = """
        SCATTER SEARCH

[0] Scatter with day selection.
[1] Scatter last month.
[2] Back.

"""

sc_5 = """
        MAPPING

[0] Map route/seg selection.
[1] Map all sp.
[2] Back.

"""

sc_6 = """
        MAPPING ALL SP

[0] Spain.
[1] Hungary.
[2] Back.

"""

sc_7 = """
        Routing

[0] Daily routing.
[1] Selection routing.
[2] Back.

"""

sc_8 = """
        Reset DDBB

[0] Reset segments.
[1] Reset routes
[2] Reset specialsites.
[3] Back.

"""

exit = False
while not exit:
    system('cls' if name == 'nt' else 'clear')
    print(sc_1)

    op = input("Select an Option: ")

    if op == "0":
        back = False
        while not back:
            system('cls' if name == 'nt' else 'clear')
            print(sc_2)

            op_0 = input("Select an Option: ")

            if op_0 == "0":
                back_to_func_00 = False
                while not back_to_func_00:
                    system('cls' if name == 'nt' else 'clear')
                    print(sc_7)
                    op_00 = input("Select an Option: ")

                    if op_00 == "0" or op_00 == "1":
                        segments.segments(op_00)
                        sleep(3)

                    if op_00 == "2":
                        system('cls' if name == 'nt' else 'clear')
                        back_to_func_00 = True

            if op_0 == "1":
                system('cls' if name == 'nt' else 'clear')
                back_to_func = False
                while not back_to_func:
                    system('cls' if name == 'nt' else 'clear')
                    print(sc_3)

                    op_01 = input("Select an Option: ")

                    if op_01 == "0" or op_01 == "1":
                        system('cls' if name == 'nt' else 'clear')
                        month_input(op_01)
                        sleep(3.5)

                    if op_01 == "2":
                        system('cls' if name == 'nt' else 'clear')
                        twoyears_input()
                        sleep(3.5)

                    if op_01 == "3":
                        system('cls' if name == 'nt' else 'clear')
                        SP20.manual()
                        sleep(1.5)

                    if op_01 == "4":
                        system('cls' if name == 'nt' else 'clear')
                        back_to_func = True

            if op_0 == "2":
                back_to_func_2 = False
                while not back_to_func_2:
                    system('cls' if name == 'nt' else 'clear')
                    print(sc_5)
                    op_02 = input("Select an Option: ")

                    if op_02 == "0":
                        system('cls' if name == 'nt' else 'clear')
                        visualizado.visualization()
                        sleep(1.5)

                    if op_02 == "1":
                        back_to_mapping = False
                        while not back_to_mapping:
                            system('cls' if name == 'nt' else 'clear')
                            print(sc_6)
                            place = input("Select place to MapSP: ")
                            if place == '0' or place == '1':
                                map.mapping(place)
                            if place == '2':
                                back_to_mapping = True

                    if op_02 == "2":
                        system('cls' if name == 'nt' else 'clear')
                        back_to_func_2 = True

            if op_0 == "3":
                back_to_func_1 = False
                while not back_to_func_1:
                    system('cls' if name == 'nt' else 'clear')
                    print(sc_4)
                    op_03 = input("Select an Option: ")

                    if op_03 == "0":
                        system('cls' if name == 'nt' else 'clear')
                        scattering.scatter_dayselect()
                        sleep(1.5)

                    if op_03 == "1":
                        system('cls' if name == 'nt' else 'clear')
                        scattering.scatter_last_month()

                    if op_03 == "2":
                        system('cls' if name == 'nt' else 'clear')
                        back_to_func_1 = True

            if op_0 == "4":
                system('cls' if name == 'nt' else 'clear')
                search.search()

            if op_0 == "5":
                back_to_func_reset = False
                while not back_to_func_reset:
                    system('cls' if name == 'nt' else 'clear')
                    print(sc_8)
                    op_05 = input("Select an option:")
                    if op_05 == "0":
                        sure = input("Are you sure to reset segments?[Y/n]: ")
                        if sure == "Y":
                            resets.reset_segments()
                            sleep(1.5)
                    if op_05 == "1":
                        sure = input("Are you sure to reset routes?[Y/n]: ")
                        if sure == "Y":
                            resets.reset_routes()
                            sleep(1.5)
                    if op_05 == "2":
                        sure = input("Are you sure to reset specialsites?[Y/n]: ")
                        if sure == "Y":
                            resets.reset_specialsites()
                            sleep(1.5)
                    if op_05 == "3":
                        back_to_func_reset = True

            if op_0 == "6":
                back = True

    if op == "1":
        system('cls' if name == 'nt' else 'clear')
        pass
    if op == "2":
        system('cls' if name == 'nt' else 'clear')
        pass
    if op == "3":
        exit = True
        database.DataBase().conection_close()
