from os import system, name
from time import sleep
import json
import requests
from .modules.utils import confirm_exit, confirm_requisition
from .modules.validations import (
    validate_column,
    validate_value,
    validate_table,
    validate_id,
)
from .modules.exceptions import RequestError, InvalidResponseError, ValidateError


class App:
    """
    Classe App com toda CLI do sistema
    """

    def __init__(self) -> None:
        self.url = "http://127.0.0.1:5000"
        self.table = None

    def clear(self) -> None:
        """
        Limpa o terminal.
        """
        system("cls" if name == "nt" else "clear")

    def menu_option(self, option: str) -> None:
        """
        Exibe um menu de acordo com a opção passada
        """
        self.clear()
        print("-" * (len(option) + 18))
        print(f"-------- {option.title()} --------")
        print("-" * (len(option) + 18))

    def menu(self) -> None:
        """
        Exibe o menu principal.
        """
        self.clear()
        self.menu_option("Crud")
        print("[1] Post")
        print("[2] Get")
        print("[3] Patch")
        print("[4] Delete")
        print("[5] Table (switch)")
        print("[6] Exit")

    def input_column(self, option: str) -> str:
        """
        Solicita ao usuário o nome da coluna.
        """
        column_valid = False
        while not column_valid:
            self.menu_option(option)
            column = input("Informe o nome da coluna: ").strip()
            column_valid = validate_column(column)
            if not column_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return column

    def input_table(self, change: bool = False) -> str:
        """
        Solicita ao usuário o nome da tabela.
        """
        table_valid = False
        while not table_valid:
            self.menu_option("Tabela")
            if change:
                print(f"Tabela atual: {self.table}")
            table = input(
                f"Informe o nome da {'nova tabela' if change else 'tabela'} \nque deseja manipular: "
            ).strip()
            table_valid = validate_table(table)
            if not table_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return table

    def input_value(self, option: str, new: bool = False) -> str:
        """
        Solicita ao usuário o valor a ser inserido ou atualizado.
        """
        value_valid = False
        while not value_valid:
            self.menu_option(option)
            value = input(f"Informe o {'novo valor' if new else 'valor'}: ").strip()
            value_valid = validate_value(value)
            if not value_valid:
                input("APERTE ENTER PARA CONTINUAR")
        return value

    def input_id(self, option: str) -> int:
        """
        Solicita ao usuário o ID.
        """
        id_valid = False
        while not id_valid:
            try:
                self.menu_option(option)
                id = str(input("Informe o id: ")).strip()
                id_valid = validate_id(id)
                if not id_valid:
                    input("APERTE ENTER PARA CONTINUAR")
            except ValueError:
                print("ID inválido. Por favor, insira um número válido.")
                input("APERTE ENTER PARA CONTINUAR")
        return int(id)

    def post(self) -> None:
        """
        Método para enviar dados (POST).
        """
        try:
            data = {"table": self.table}
            while True:
                option = "post"
                self.menu_option(option)
                column = self.input_column(option)
                value = self.input_value(option)
                if column not in data:
                    data[column] = value
                    saida_valida = False
                    while not saida_valida:
                        self.menu_option(option)
                        confirm = (
                            input(
                                "Todos os dados foram adicionados com sucesso? [Sim/Não]\n"
                            )
                            .lower()
                            .strip()
                        )
                        saida_valida = confirm_exit(confirm)
                        if not saida_valida:
                            input("APERTE ENTER PARA CONTINUAR")
                    if confirm in ["sim", "s"]:
                        response = requests.post(f"{self.url}/post", json=data)
                        self.menu_option(option)
                        if response.status_code == 201:
                            print("dados enviados com sucesso!")
                            input("APERTE ENTER PARA CONTINUAR")
                            break
                        else:
                            print(
                                f"Erro ao enviar dados: {response.status_code} - {response.text["message"]}"
                            )
                            input("APERTE ENTER PARA CONTINUAR")
                        confirmValid = False
                        while not confirmValid:
                            confirm = str(input("Deseja voltar para o menu? [Sim/Não]")).lower().strip()
                            confirmValid = confirm_exit(confirm)
                            if not confirmValid:
                                input("APERTE ENTER PARA CONTINUAR")
                        if confirm in ["sim", "s"]:
                            self.menu_option(option)
                            print("Voltando para o menu")
                            sleep(1)
                            break
                else:
                    print("Dado já adicionado")
                    input("APERTE ENTER PARA CONTINUAR")
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")

    def get(self) -> None:
        """
        Método para obter dados (GET).
        """
        try:
            if self.table is None:
                print("Tabela não definida. Use a opção '5' para definir uma tabela.")
                input("APERTE ENTER PARA CONTINUAR")
                return
            tentativas = 0
            max_tentativas = 3
            while tentativas < max_tentativas:
                option = "get"
                self.menu_option(option)
                data = {"table": self.table}
                response = requests.get(f"{self.url}/get", json=data)
                if response.status_code == 200:
                    print("Requisição bem sucedida!")
                    input("APERTE ENTER PARA CONTINUAR")
                    self.menu_option("Get")
                    datas = json.load(response.content)
                    print(datas)
                    break
                else:
                    print("Falha ao obter dados após várias tentativas.")
                tentativas += 1
                confirmValid = False
                while not confirmValid:
                    confirm = str(input("Deseja voltar para o menu? [Sim/Não]")).lower().strip()
                    confirmValid = confirm_exit(confirm)
                    if not confirmValid:
                        input("APERTE ENTER PARA CONTINUAR")
                if confirm in ["sim", "s"]:
                    self.menu_option(option)
                    print("Voltando para o menu")
                    sleep(1)
                    break
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            input("APERTE ENTER PARA CONTINUAR")

    def patch(self) -> None:
        """
        Método para atualizar dados (PATCH).
        """
        try:
            while True:
                option = "patch"
                self.menu_option(option)
                column = self.input_column(option)
                new_value = self.input_value(option, new=True)
                id = self.input_id(option)
                data = {
                    "table": self.table,
                    "id": id,
                    "column": column,
                    "value": new_value,
                }
                response = requests.patch(f"{self.url}/patch", json=data)
                if response.status_code == 200:
                    print("Dados atualizados com sucesso!")
                    break
                else:
                    print(f"Erro ao atualizar dados: {response.status_code}")
                    input("APERTE ENTER PARA CONTINUAR")
                confirmValid = False
                while not confirmValid:
                    confirm = str(input("Deseja voltar para o menu? [Sim/Não]")).lower().strip()
                    confirmValid = confirm_exit(confirm)
                    if not confirmValid:
                        input("APERTE ENTER PARA CONTINUAR")
                if confirm in ["sim", "s"]:
                    self.menu_option(option)
                    print("Voltando para o menu")
                    sleep(1)
                    break

        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")

    def delete(self) -> None:
        """
        Método para deletar dados (DELETE).
        """
        try:
            while True:
                option = "delete"
                self.menu_option(option)
                id = self.input_id(option)
                data = {"table": self.table, "id": id}
                response = requests.delete(f"{self.url}/delete", json=data)
                if response.status_code == 200:
                    print("Dados deletados com sucesso!")
                    input("APERTE ENTER PARA CONTINUAR")
                    break
                else:
                    print(
                        f"Falha ao deletar os dados\nCode: {response.status_code}"
                    )
                confirmValid = False
                while not confirmValid:
                    confirm = str(input("Deseja voltar para o menu? [Sim/Não]")).lower().strip()
                    confirmValid = confirm_exit(confirm)
                    if not confirmValid:
                        input("APERTE ENTER PARA CONTINUAR")
                if confirm in ["sim", "s"]:
                    self.menu_option(option)
                    print("Voltando para o menu")
                    sleep(1)
                    break
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")

    def switch_table(self) -> None:
        """
        Método para alternar a tabela ativa.
        """
        self.table = self.input_table(change=True)

    def exit(self) -> None:
        """
        Método para sair do programa.
        """
        self.menu_option("Exit")
        response = input("Deseja mesmo sair? [Sim/Não]\n").strip().lower()
        if confirm_exit(response) and response in ["sim", "s"]:
            self.continuar = False
            print("Programa Finalizado!")

    def run(self) -> None:
        """
        Método principal para rodar o menu.
        """
        try:
            self.table = self.input_table()
            self.continuar = True
            while self.continuar:
                self.menu()
                choice = input("Informe a operação desejada: ").strip()
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
                        print("Opção inválida!")
                        input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")
