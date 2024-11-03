from dataclasses import dataclass
from .config import connect
import json

@dataclass
class Crud:
    connection = connect()

    def get_connection(self):
        try:
            self.connection.ping()
        except Exception:
            self.connection = connect()
        return self.connection

    # Inserir dados no banco de dados
    def post(self, data: dict):
        cursor = None
        try:
            connection = self.get_connection()
            table = data.pop("table")
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f":{i+1}" for i in range(len(data))])
            values = tuple(data.values())
            command = f"INSERT INTO {table.upper()} ({columns}) VALUES ({placeholders})"
            cursor = connection.cursor()
            cursor.execute(command, values)
            connection.commit()
            return {"status": "success", "message": "Dados inseridos com sucesso!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Atualizar selecionando campo
    def patch(self, table: str, id: int, column: str, value: str):
        cursor = None
        try:
            connection = self.get_connection()
            command = f"UPDATE {table.upper()} SET {column} = :value WHERE ID = :id"
            cursor = connection.cursor()
            cursor.execute(command, {"value": value, "id": id})
            connection.commit()
            return {"status": "success", "message": "Campo atualizado com sucesso!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Deletar
    def delete(self, table: str, id: int):
        cursor = None
        try:
            connection = self.get_connection()
            command = f"DELETE FROM {table.upper()} WHERE ID = :id"
            cursor = connection.cursor()
            cursor.execute(command, {"id": id})
            connection.commit()
            return {"status": "success", "message": f"Id: {id} deletado!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Obter todos os dados
    def get(self, table: str):
        cursor = None
        try:
            connection = self.get_connection()
            command = f"SELECT * FROM {table.upper()}"
            cursor = connection.cursor()
            cursor.execute(command)
            rows = cursor.fetchall()
            return {
                "status": "success",
                "message": json.dumps(rows) if rows else [],
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Obter dados de um id especifico
    def get_with_id(self, table: str, id: int):
        cursor = None
        try:
            connection = self.get_connection()
            command = f"SELECT * FROM {table.upper()} WHERE ID = :id"
            cursor = connection.cursor()
            cursor.execute(command, {"id": id})
            row = cursor.fetchone()
            return {
                "status": "success",
                "message": json.dumps(row) if row else "{}",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    def __del__(self):
        if self.connection:
            self.connection.close()
