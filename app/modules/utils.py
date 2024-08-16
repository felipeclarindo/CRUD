from ...database.config import connect

def validate_table(table: str) -> bool:
    try:
        if table:
            if table.isalnum():
                connection = connect()
            else:
                raise Exception("O nome da tabela não pode conter caracteres.")
        else:
            raise Exception("O nome da tabela não pode ser vazio.")
    except ValueError as v:
        print(f"Error: {v}")
    except Exception as e:
        print(f"Error: {e}")

def validate_column(column:str) -> bool:
    try:
        pass
    except ValueError as v:
        print(f"Error: {v}")
    except Exception as e:
        print(f"Error: {e}")

def validate_type(type:int) -> int | str:
    try:
        match type:
            case 1:
                return int
            case 2:
                return str
            case _:
                raise Exception("Opção invalida")
    except ValueError as v:
        print(f"Error: {v}")
    except Exception as e:
        print(f"Error: {e}")

def validate_value(value:str) -> bool:
    try:
        pass
    except ValueError as v:
        print(f"Error: {v}")
    except Exception as e:
        print(f"Error: {e}")