import requests
from datetime import datetime

"""DURAKOLsoftware"""


class TomatoTimerGraph:
    url_pixela = """https://docs.pixe.la/"""

    def __init__(self, username=None, password=None):
        if not username:
            self.username = "enter your name function"
        else:
            self.username = "name from database"

        if not password:
            self.headers = "enter password function"
        else:
            self.headers = "password from database"

        self.graph_list = []  # read all graph from database

        self.today = datetime.now()

        self.last_update = "log"

        self.pixela_endpoint = "https://pixe.la/v1/users"
        self.graph_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs"
        self.current_graph_id = "READ FROM DATABASE/LOG last used"

    def create_user_account(self):
        """

        :return:
        """
        in_user_params = {
            "token": self.headers,
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }
        response = requests.post(url=self.pixela_endpoint, json=in_user_params)
        return response.text

    @staticmethod
    def choose_color(color="default"):

        choice = "wrong"
        colors = {
            "green": "shibafu",
            "red": "momiji",
            "blue": "sora",
            "yellow": "ichou",
            "purple": "ajisai",
            "black": "kuro"
        }

        if color == "default":
            return colors["red"]
        else:
            for key, value in colors.keys():
                print(enumerate(key))

            while choice not in colors.keys():
                choice = input("type color name to choose a color: ")
                if color not in colors.keys():
                    print("unavailable color!")

            return colors[choice]

    def create_graph_frame(self, graph_name=None, color=None):

        # if not graph_name:
        #     # Todo import nameless counter numbers
        #     # create a automatic graph name with the username and counter number (username003)
        #     nameless_counter_number = 1
        #     graph_name = f"{self.name}{str(nameless_counter_number):.2d}"
        #     nameless_counter_number += 1  # create/save the counter to be read after

        graph_setup = {
            "id": graph_name,
            "name": self.username,
            "unit": "minutes",
            "type": "int",
            "color": self.choose_color(color)

        }

        # security reason to give the password or token in a json format
        password = {
            "X-USER-TOKEN": self.headers
        }

        response = requests.post(url=self.graph_endpoint, json=graph_setup, headers=password)
        # todo: log the graph in the graph database if succeful
        self.graph_list.append(graph_name)
        self.current_graph_id = graph_name
        return response.text

    def change_current_graph(self, graph_id=None):
        answer = None
        if not graph_id:
            for graph in self.graph_list:
                print(enumerate(graph))

        while answer not in self.graph_list:
            answer = input("enter the graph name: ")
            if answer not in self.graph_list:
                print("graph id not found")
        # Todo:  log the last used/current database
        self.current_graph_id = answer

    def add_pixel(self, graph, amount):

        create_pixel_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{graph}"

        pixel_data = {
            "date": self.set_date(),
            "quantity": amount,
        }

        self.last_update = "recreate log"

        response = requests.post(url=create_pixel_endpoint, json=pixel_data, headers=self.headers)
        return response.text

    def update_pixela(self, quantity=None, today=True):
        # Todo: ask credentials, confirmation
        if not today:
            date = self.set_date()
        else:
            date = self.today

        # if not quantity:
        #     quantity = quantity_UI()

        date = str(date.strftime("%Y%m%d"))

        pixel_data = {
            "quantity": str(quantity),
        }

        update_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{self.current_graph_id}/{date}"

        response = requests.put(url=update_endpoint, json=pixel_data, headers=self.headers)
        print(response.text)

    def delete_a_pixel(self, today=True):
        # Todo: ask credentials, confirmation
        if not today:
            date = self.set_date()
        else:
            date = datetime.now()

        date = str(date.strftime("%Y%m%d"))

        delete_pixel_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{self.current_graph_id}/{date}"
        response = requests.delete(url=delete_pixel_endpoint, headers=self.headers)
        print(response.text)

    def update_graph_details(self):
        # Todo: ask credentials, confirmation
        update_graph_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{self.current_graph_id}"
        graph_id = input("enter new graph name: ")
        choice = self.choose_color()

        graph_setup = {
            "id": graph_id,
            "name": self.username,
            "unit": "minutes",  # cause this is for the tomato_timer
            "type": "int",
            "color": f"{choice}"

        }

        response = requests.put(url=update_graph_endpoint, json=graph_setup, headers=self.headers)
        return response.text

    def change_password(self):  # not tested, not developed
        # Todo: ask credentials
        update_user_endpoint = f"{self.pixela_endpoint}/{self.username}"
        update_user_data = {
            "new_token": input("enter new password")
        }
        response = requests.put(url=update_user_endpoint, json=update_user_data, headers=self.headers)
        self.headers = update_user_data["new_token"]
        return response

    def delete_graph(self, graph):
        # Todo: ask credentials, confirmation
        delete_graph_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{graph}"
        response = requests.delete(url=delete_graph_endpoint, headers=self.headers)
        self.graph_list.remove(graph)
        # Todo: delete the graph from the database
        return response

    def delete_user(self):
        # Todo: ask credentials, confirmation
        delete_user_endpoint = f"{self.pixela_endpoint}/{self.username}"
        response = requests.delete(url=delete_user_endpoint, headers=self.headers)
        return response

    @staticmethod
    def set_date():
        data_date = ["year", "month", "day"]
        date_dict = {data: int(input(f"{data}: ")) for data in data_date}
        formatted_date = datetime(year=date_dict['year'], month=date_dict['month'], day=date_dict['day'])
        return formatted_date

    # LOGS & DATABASE
    def last_update_log(self):
        # Todo: check if there is a log file
        # Todo: if yes read from it last log and update
        # Todo: if not create one and write on it last log
        pass
