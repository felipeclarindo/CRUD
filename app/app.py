from .modules.utils import validate_table

class App:
    def __init__(self) -> None:
        self.api = "https://localhost"

    def clear(self):   
        pass 

    def menu_post(self):
        self.clear()
        print("""
------------------------
-------- Post --------
------------------------
""")

    def menu_delete(self):
        self.clear()
        print(""" 
------------------------
--------- Delete ---------
------------------------
""")


    def menu_get(self):
        self.clear()
        print(""" 
-----------------------
--------- Get ---------
-----------------------
""")
    
    def menu_update(self):
        self.clear()
        print("""
------------------------
-------- Update --------
------------------------
""")
        
    def menu(self):
        self.clear()
        print("""
------------------------
--------- Crud ---------
------------------------
[1] Post
[2] Get
[3] Update
[4] Delete
[5] Exit
""")
        
    def run(self):
        try:
            table_valid = False
            while not table_valid:
                self.clear()
                self.table = str(input("Informe o nome da tabela para manipulação: "))
                table_valid = validate_table(self.table)
                if not table_valid:
                    input("PRESS ENTER TO CONTINUE")
            if table_valid:
                while True:
                    self.menu()
                    choice = int(input("Informe a operação desejada: "))
                    match choice:
                        # Post
                        case 1:
                            column = str(input("Qual coluna você deseja inserir dados? "))
                            

                            value = str(input(""))
                        # Get
                        case 2:
                            pass
                        # Update
                        case 3:
                            pass
                        # Delete
                        case 4:
                            pass
                        # Sair
                        case 5:
                            pass
                        case _:
                            print("Opção invalida!")
                            input("APERTE ENTER PARA CONTINUAR")
        except ValueError as v:
            print(f"Error: {v}")
        except Exception as e:
            print(f"Error: {e}")
        