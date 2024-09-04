from dataclasses import dataclass
from config import connect
import json


@dataclass
class Crud:
    """
    Crud para manipulação de uma base de dados Oracle com métodos (Post, Put, Patch, Get, GetWithId, Delete)
    """

    connection = connect()

    def get_connection(self):
        try:
            self.connection.ping()
        except Exception:
            self.connection = connect()
        return self.connection

    # Inserir dados no banco de dados
    def post(self, data: dict):
        """
        Método para inserir novos dados
        """
        cursor = None
        try:
            connection = self.get_connection()
            table = data.pop("table")
            columns = ", ".join(data.keys())
            placeholders = ", ".join([":{}".format(i + 1) for i in range(len(data))])
            values = tuple(data.values())
            command = f"INSERT INTO {table.upper()} ({columns}) VALUES ({placeholders})"
            cursor = connection.cursor()
            cursor.execute(command, values)
            connection.commit()
            return {"status": "success", "message": "Dados inseridos com sucesso!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Atualizar selecionando campo
    def patch(self, table: str, id: int, column: str, value: str):
        """
        Método para atualizar um único dado de um id especificado
        """
        cursor = None
        try:
            connection = self.get_connection()
            command = f"UPDATE {table.upper()} SET {column} = :value WHERE ID = :id"
            cursor = connection.cursor()
            cursor.execute(command, value=value, id=id)
            connection.commit()
            return {"status": "success", "message": "Campo atualizado com sucesso!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Deletar
    def delete(self, table: str, id: int):
        """
        Método para deletar dados de um id especificado
        """
        cursor = None
        try:
            connection = self.get_connection()
            command = f"DELETE FROM {table.upper()} WHERE ID = :id"
            cursor = connection.cursor()
            cursor.execute(command, id=id)
            connection.commit()
            return {"status": "success", "message": f"id {id} deletado!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Obter todos os dados
    def get(self, table: str):
        """
        Método para pegar dados da tabela
        """
        cursor = None
        try:
            connection = self.get_connection()
            command = f"SELECT * FROM {table.upper()} ORDER BY ID"
            cursor = connection.cursor()
            cursor.execute(command)
            usuarios = cursor.fetchall()
            return {
                "status": "success",
                "message": json.dumps(usuarios) if usuarios else "{}",
            }
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    # Finalizando a conexão quando a instância é excluída
    def __del__(self):
        """
        Método que finaliza a conexão com o banco de dados quando a instancia do crud é deletada.
        """
        if self.connection:
            self.connection.close()
