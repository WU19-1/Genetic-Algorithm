from handlers.input_handler import input_message
from controller.docker_controller import show_docker_information, show_docker_usage
from genetic_algorithm import genetic_algorithm
from manual_stress_test import manual_stress_test
from dotenv import load_dotenv


if __name__ == "__main__":

    load_dotenv()

    MENU = -1
    MENU_LIST = {
        "1": ("Show docker information", show_docker_information),
        "2": ("Show running docker container status", show_docker_usage),
        "3": ("Run genetic algorithm", genetic_algorithm),
        "4": ("Run manual stress test", manual_stress_test),
        "5": ("Exit", exit),
    }

    while MENU != len(MENU_LIST):
        MENU = -1

        input_message(withInput=False)
        print("Main Menu")
        for index in MENU_LIST.keys():
            print(index + ". " + MENU_LIST[index][0])

        while MENU < 1 or MENU > len(MENU_LIST):
            try:
                MENU = int(input(">> "))
            except ValueError:
                MENU = -1
        input_message(withInput=False)

        MENU_LIST.get(str(MENU))[1]()
        input_message(withEnter=False)
