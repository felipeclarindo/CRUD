from dataclasses import dataclass
from config import connect
import json


@dataclass
class Crud:
    """
    Crud para manipulação de uma base de dados com métodos (Post, Put, Patch, Get, GetWithId, Delete)
    """

    connection = connect()

    # Inserir dados no banco de dados
    def post(self, data: dict):
        """
        Método para inserir novos dados
        """
        try:
            table = data.pop("table")
            columns = ", ".join(data.keys())
            values = ", ".join(data.values())
            command = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            with self.connection.cursor() as cursor:
                cursor.execute(command)
            self.connection.commit()
            return {"status": "success", "message": "Dados inseridos com sucesso!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar dados
    def put(self, table: str, columns: list[str], values: list[str], id: int):
        """
        Método para atualizar todos os dados de um id especificado
        """
        try:
            set_command = ", ".join(f"{column} = ?" for column in columns)
            command = f"UPDATE {table} SET {set_command} WHERE ID = ?"
            with self.connection.cursor() as cursor:
                cursor.execute(command, (*values, id))
            self.connection.commit()
            return {"status": "success", "message": "Dados atualizados com sucesso!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar selecionando campo
    def patch(self, table: str, id: int, column: str, value: str):
        """
        Método para atualizar um único dado de um id especificado
        """
        try:
            command = f"UPDATE {table} SET {column} = :value WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"value": value, "id": id})
            self.connection.commit()
            return {"status": "success", "message": "Campo atualizado com sucesso!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Deletar
    def delete(self, table: str, id: int):
        """
        Método para deletar dados de um id especificado
        """
        try:
            command = f"DELETE FROM {table} WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
            self.connection.commit()
            return {"status": "success", "message": f"id {id} deletado!"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Obter todos os dados
    def get(self, table: str):
        """
        Método para pegar dados da tabela
        """
        try:
            command = f"SELECT * FROM {table}"
            with self.connection.cursor() as cursor:
                cursor.execute(command)
                usuarios = cursor.fetchall()
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
        """
        Método para pegar dados por id
        """
        try:
            command = f"SELECT * FROM {table} WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
                usuario = cursor.fetchone()
            return {
                "status": "success",
                "message": json.dumps(dict(usuario)),
            }
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Finalizando a conexão quando a instância é excluída
    def __del__(self):
        """
        Método que finaliza a conexão com o banco de dados quando a instancia do crud é deletada.
        """
        self.connection.close()
