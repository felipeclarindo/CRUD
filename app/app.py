from os import system, name
from time import sleep
import json
import requests
from .utils.utils import confirm_exit, confirm_requisition
from .validations.validations import (
    validate_column,
    validate_value,
    validate_table,
    validate_id,
)
from .modules.generate_json import generate_json_file

class App:
    """
    Classe App com toda CLI do sistema
    """

    def __init__(self) -> None:
        self.url = "http://127.0.0.1:3000"
        self.table = None
        self.valid = True
        self.ids = []

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
        print(f"Manipulando tabela: {self.table}")
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
                print("Buscando usúarios...")
                sleep(1)
                self.get(option, search=True, method=option)
                if self.valid:
                    while not id_valid:
                        id = str(input("Informe o id: ")).strip()
                        id_valid = validate_id(id, self.ids)
                        if not id_valid:
                            input("APERTE ENTER PARA CONTINUAR")
                            self.menu_option(option)
                            self.get(option, search=True, method=option)
                else:
                    return None
                    
            except ValueError:
                print("ID inválido. Por favor, insira um número válido.")
                input("APERTE ENTER PARA CONTINUAR")
        return int(id)

    def save_dados(self, dados: list[list], option: str) -> None:
        """
        Salva os dados em um arquivo JSON.
        """
        try:
            option = option.lower()
            self.menu_option(option)
            confirm_valid = False
            while not confirm_valid:
                self.menu_option(option)
                confirm = input("Deseja salvar os dados em um arquivo JSON? [Sim/Não]\n")
                confirm_valid = confirm_exit(confirm)
                if not confirm_valid:
                    input("APERTE ENTER PARA CONTINUAR")
            if confirm.lower() in ["sim", "s", "ss"]:
                self.menu_option(option)
                filename= input("Informe o nome do arquivo: ").strip()
                print(generate_json_file(dados, filename=f"{filename}.json"))
                input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            input("APERTE ENTER PARA CONTINUAR")

    def view_dado(self, dados: dict, option: str) -> None:
        """
        Exibe um dado específico.
        """
        self.menu_option(option)
        for key, value in dados.items():
            print(f"{key}: {value}")
        input("APERTE ENTER PARA CONTINUAR")

    def view_dados(self, dados: list[list], option: str, id: bool = False):
        dados_list = ["id", "nome", "marca", "ano"]
        if id:
            self.menu_option("ids")
        if dados:
            for dado in dados:
                if id:
                    nome = dado[1]
                    valor_id = dado[0]
                    self.ids.append(valor_id)
                    print(f"{valor_id:<3} ->   {nome}")
                else:
                    self.menu_option(option)
                    for indice, campo in enumerate(dados_list):
                        valor = dado[indice] if indice < len(dado) else "Dados ausentes"
                        print(f"{campo:<8} ->   {valor}")
                    (
                        input("APERTE ENTER PARA VER O PRÓXIMO DADO!")
                        if len(dados) > 1
                        else input("APERTE ENTER PARA CONTINUAR")
                    )
            if not id:
                self.menu_option(option)
                print("Dados exibidos com sucesso!")
                input("APERTE ENTER PARA CONTINUAR")
        else:
            self.valid = False
            self.menu_option(option)
            print("Nenhum dado encontrado!")
            input("APERTE ENTER PARA CONTINUAR")

    def voltar_menu(self, option: str) -> bool:
        confirmValid = False
        while not confirmValid:
            self.menu_option(option)
            confirm = (
                str(input("Deseja voltar para o menu? [Sim/Não]\n")).lower().strip()
            )
            confirmValid = confirm_exit(confirm)
            if not confirmValid:
                input("APERTE ENTER PARA CONTINUAR")
        if confirm in ["sim", "s"]:
            self.menu_option(option)
            print("Voltando ao menu...")
            sleep(1)
            return True
        return False

    def post(self) -> None:
        """
        Método para enviar dados (POST).
        """
        try:
            dados = {}
            while True:
                option = "post"
                self.menu_option(option)
                column = self.input_column(option)
                value = self.input_value(option)
                if column not in dados:
                    dados[column] = value
                    saida_valida = False
                    while not saida_valida:
                        self.menu_option(option)
                        dados_view = dados
                        print(
                            "\n".join(
                                f"{dado:<6} -> {valor:>6}"
                                for dado, valor in dados_view.items()
                                if dado != "message"
                            )
                        )
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
                        dados["table"] = self.table
                        dados = {
                            dado: valor
                            for dado, valor in dados.items()
                            if dado != "message"
                        }
                        response = requests.post(f"{self.url}/api/table", params=dados)
                        self.menu_option(option)
                        if response.status_code == 201:
                            try:
                                dados = response.json()
                            except ValueError:
                                print("Erro ao decodificar a resposta JSON.")
                                input("APERTE ENTER PARA CONTINUAR")
                            print(dados.get("message"))
                            input("APERTE ENTER PARA CONTINUAR")
                            if self.voltar_menu(option):
                                break
                            self.menu_option(option)
                            print(f"Reiniciando método: {option}...")
                            sleep(1)
                            continue
                        else:
                            try:
                                error_message = response.json().get(
                                    "message", "Nenhuma mensagem de erro fornecida."
                                )
                            except ValueError:
                                error_message = response.text
                            print(
                                f"Erro ao enviar dados: {response.status_code} - {error_message}"
                            )
                            input("APERTE ENTER PARA CONTINUAR")

                        if self.voltar_menu(option):
                            break
                        dados = {}
                        self.menu_option(option)
                        print(f"Reiniciando método: {option}...")
                        sleep(1)
                        continue
                else:
                    print("Dado já adicionado")
                    input("APERTE ENTER PARA CONTINUAR")
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")

    def get(self, option: str = "get", search: bool = False, method: str = "") -> None:
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
                params = {"table": self.table}
                response = requests.get(f"{self.url}/api/table", params=params)

                if response.status_code == 200:
                    try:
                        dados = response.json()  # Decodifica o JSON da resposta
                    except ValueError:
                        print("Erro ao decodificar a resposta JSON.")
                        input("APERTE ENTER PARA CONTINUAR")
                        tentativas += 1
                        continue
                    print(dados)
                    dados = json.loads(dados.get("content"))
                    if search:
                        self.view_dados(dados, option=method, id=True)
                    else:
                        self.view_dados(dados, option)
                        self.save_dados(dados, option)
                        if self.voltar_menu(option):
                            break
                        self.menu_option(option)
                        print(f"Reiniciando método: {option}...")
                        sleep(1)
                        continue
                else:
                    print("Falha ao obter dados após várias tentativas.")
                    input("APERTE ENTER PARA CONTINUAR")
                    if self.voltar_menu(option):
                        break
                    self.menu_option(option)
                    print(f"Reiniciando método: {option}...")
                    sleep(1)
                    continue

                tentativas += 1

        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")

    def get_with_id(self, id: int, option: str = "get") -> None:
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
                params = {"table": self.table}
                response = requests.get(f"{self.url}/api/table/{id}", params=params)

                if response.status_code == 200:
                    try:
                        dados = response.json()  # Decodifica a resposta JSON
                    except ValueError:
                        print("Erro ao decodificar a resposta JSON.")
                        input("APERTE ENTER PARA CONTINUAR")
                        tentativas += 1
                        continue

                    dados = json.loads(dados.get("content"))
                    self.view_dado(dados, option)
                    self.save_dados(dados, option)
                    if self.voltar_menu(option):
                        break
                    self.menu_option(option)
                    print(f"Reiniciando método: {option}...")
                    sleep(1)
                    continue
                else:
                    print("Falha ao obter dados após várias tentativas.")
                    input("APERTE ENTER PARA CONTINUAR")
                    if self.voltar_menu(option):
                        break
                    self.menu_option(option)
                    print(f"Reiniciando método: {option}...")
                    sleep(1)
                    continue

                tentativas += 1

        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            input("APERTE ENTER PARA CONTINUAR")
        except Exception as e:
            print(f"Erro: {e}")
            input("APERTE ENTER PARA CONTINUAR")


    def patch(self) -> None:
        """
        Método para atualizar dados (PATCH).
        """
        try:
            while True:
                option = "patch"
                id = self.input_id(option)
                if id is not None: 
                    option_id = f"{option} id: {id}"
                    column = self.input_column(option_id)
                    new_value = self.input_value(option_id, new=True)
                    dados = {
                        "table": self.table,
                        "column": column,
                        "value": new_value,
                    }
                    response = requests.patch(f"{self.url}/api/table/{id}", params=dados)
                    if response.status_code == 200:
                        self.menu_option(option)
                        print("Dados atualizados com sucesso!")
                        input("APERTE ENTER PARA CONTINUAR")
                        if self.voltar_menu(option):
                            break
                        self.menu_option(option)
                        print(f"Reiniciando método: {option}...")
                        sleep(1)
                        continue
                    else:
                        print(f"Erro ao atualizar dados: {response.status_code}")
                        input("APERTE ENTER PARA CONTINUAR")
                else:
                    if self.voltar_menu(option):
                        break
                    
                    self.menu_option(option)
                    print(f"Reiniciando método: {option}")
                    sleep(1)
                    continue

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
                id = self.input_id(option)
                dados = {"table": self.table}
                if self.valid and id:
                    response = requests.delete(f"{self.url}/delete/{id}", params=dados)
                    if response.status_code == 200:
                        self.menu_option(option)
                        response = response.json()
                        print(response["message"])
                        input("APERTE ENTER PARA CONTINUAR")
                        if self.voltar_menu(option):
                            break
                        self.menu_option(option)
                        print(f"Reiniciando método: {option}...")
                        sleep(1)
                        continue
                else:
                    if self.voltar_menu(option):
                        break
                    self.menu_option(option)
                    print(f"Reiniciando método: {option}")
                    sleep(1)
                    continue
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
        responseValid = False
        while not responseValid:
            self.menu_option("Exit")
            response = input("Deseja mesmo sair? [Sim/Não]\n").strip().lower()
            responseValid = confirm_exit(response)
            if not responseValid:
                input("APERTE ENTER PARA CONTINUAR")

        if response in ["sim", "s"]:
            self.continuar = False
            self.menu_option("good bye!")
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
