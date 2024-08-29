from os import system, name
from .modules.utils import confirm_exit, confirm_requisition
from .modules.validations import (
    validate_column,
    validate_value,
    validate_table,
    validate_id,
)
import requests

class RequestError(Exception):
    pass


class App:
    def __init__(self) -> None:
        self.url = "http://127.0.0.1:5000"

    def clear(self) -> None:
        if name == "nt":
            system("cls")
        else:
            system("clear")

    def menu_option(self, option: str) -> None:
        self.clear()
        print("-" * (len(option) + 18))
        print(f"-------- {option.title()} --------")
        print("-" * (len(option) + 18))

    def menu(self) -> None:
        self.clear()
        self.menu_option("Crud")
        print("[1] Post")
        print("[2] Get")
        print("[3] Patch")
        print("[4] Delete")
        print("[5] Table (switch)")
        print("[6] Exit")

    def input_column(self) -> str:
        column_valid = False
        while not column_valid:
            column = str(
                input("Informe o nome da coluna que deseja inserir dado: ")
            ).strip()
            column_valid = validate_column(column)
            if not column_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return column

    def input_table(self, change: bool = False) -> str:
        table_valid = False
        while not table_valid:
            self.menu_option("Tabela")
            table = str(input(f"Informe o nome da {"nova tabela" if change else "tabela"} \nque deseja manipular: "))
            table_valid = validate_table(table)
            if not table_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return table

    def input_value(self, new:bool = False) -> str:
        value_valid = False
        while not value_valid:
            value = input(f"Informe o {"novo valor" if new else "valor"}: ")
            value_valid = validate_value(value)
            if not value_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return value

    def input_id(id: int) -> int:
        id_valid = False
        while not id_valid:
            id = int(input("Informe o id: "))
            id_valid = validate_id(id)
            if not id_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return id

    def post(self) -> None:
        try:
            data = {}
            while True:
                self.menu_option("post")
                column = self.input_column()
                value = self.input_value()
                data[column] = value
                if column in data.keys():
                    print("Dado ja adicionado")
                    continue
                else:
                    confirm = str(input("Todos as colunas foram adicionadas com sucesso? [Sim/Não]\n"))
                    if confirm_exit(confirm):
                        if confirm.lower() in ["sim", "s"]:
                            response = requests.post(f"{self.url}/post", data=data)
                            if confirm_requisition(response, "post"):
                                print("Dados enviados com sucesso!")
                                input("APERTE ENTER PARA CONTINUAR")
                                break
                            else:
                                raise RequestError("Erro ao enviar os dados.")
        except RequestError as e:
            print(e)

    def get(self) -> None:
        try:
            while True:
                self.menu_option("Get")
                data = {"table": self.table}
                response = requests.get(f"{self.url}/get", data=data)
                if confirm_requisition(response, "get"):
                    print(response.content)
                    break
                else:
                    raise RequestError("Erro ao pegar os dados.")
        except RequestError as e:
            print(e)

    def patch(self) -> None:
        try:
            while True:
                self.menu_option("patch")
                column = self.input_column()
                new_value = self.input_value(new=True)
                id = self.input_id()
                data = {"table": self.table, "id": id, "column": column, "value": new_value}
                response = requests.patch(f"{self.url}/patch", data=data)
                if confirm_requisition(response, "patch"):
                    print("Dado atualizado com sucesso")
                    break
                else:
                    raise RequestError("Erro ao atualizar o dado.")
        except RequestError as e:
            print(e)

    def delete(self) -> None:
        try:
            while True:
                self.menu_option("Delete")
                id = self.input_id()
                data = {"table": self.table, "id": id}
                response = requests.delete(f"{self.url}/delete", data=data)
                if confirm_requisition(response, "delete"):
                    print("Dados enviados com sucesso!")
                    break
                else:
                    raise RequestError("Erro ao enviar dados.")
        except RequestError as e:
            print(e)

    def switch_table(self) -> None:
        self.menu_option("Table")
        self.table = self.input_table(change=True)

    def exit(self) -> None:
        self.menu_option("Exit")
        response = str(input("Deseja mesmo sair? [Sim/Não]\n"))
        if confirm_exit(response) and response.lower() in ["sim", "s"]:
            self.continuar = False
            print("Programa Finalizado!")

    def run(self) -> None:
        try:
            self.table = self.input_table()
            self.continuar = True
            while self.continuar:
                self.menu()
                choice = str(input("Informe a operação desejada: "))
                match choice:
                    case "1":
                        self.post()
                    case "2":
                        self.get()
                    case "3":
                        self.patch()
                    case "4":
                        self.delete()
                    case "5":
                        self.switch_table()
                    case "6":
                        self.exit()
                    case _:
                        print("Opção invalida!")
                        input("APERTE ENTER PARA CONTINUAR")
        except ValueError as v:
            print(f"Error: {v}")
        except Exception as e:
            print(f"Error: {e}")
