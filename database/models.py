from dataclasses import dataclass
from config import connect
import json


@dataclass
class Crud:
    connection = connect()

    # Inserir dados no banco de dados
    def post(self, data: dict):
        try:
            table = data.pop("table")
            columns = ", ".join(data.keys())
            values = ", ".join([":" + value for value in data.values()])
            print(values)
            command = f"INSERT INTO :table (:columns) VALUES (:value)"
            cursor = self.connection.cursor()
            cursor.execute(
                command, {"table": table, "columns": columns, "value": values}
            )
            self.connection.commit()
            cursor.close()
            return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar dados
    def put(self, table: str, column: str, value: str):
        try:
            command = "UPDATE :table SET :column = :value WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"table": table, "column": column, "value": value})
            cursor.close()
            return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar selecionando campo
    def patch(self, table: str, id: int, column: str, value: str):
        try:
            command = "UPDATE :table SET :column = :value WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(
                command,
                {"table": table, "column": column, "value": value, "id": id},
            )
            cursor.close()
            return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Deletar
    def delete(self, table: str, id: int):
        try:
            command = f"DELETE FROM :table WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"id": id, "table": table})
            self.connection.commit()
            cursor.close()
            return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Obter todos os dados
    def get(self, table: str):
        try:
            command = "SELECT * FROM :table"
            cursor = self.connection.cursor()
            cursor.execute(command, {"table": table})
            usuarios = cursor.fetchall()
            cursor.close()
            return {
                "status": "success",
                "message": json.dumps([dict(usuario) for usuario in usuarios]),
            }
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Obter dados por ID
    def get_with_id(self, table: str, id: int):
        try:
            command = f"SELECT * FROM :table WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"table": table, "id": id})
            usuario = cursor.fetchone()
            cursor.close()
            return {"status": "success", "message": json.dumps([dict(usuario)])}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Finalizando a conexão quando instancia excluida
    def __del__(self):
        self.connection.close()
