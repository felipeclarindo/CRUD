from dataclasses import dataclass
from config import connect
import json


@dataclass
class Crud:
    """
    Crud para manipulação de uma base de dados Oracle com métodos (Post, Put, Patch, Get, GetWithId, Delete)
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
            placeholders = ", ".join([":{}".format(i + 1) for i in range(len(data))])
            values = tuple(data.values())
            command = f"INSERT INTO {table.upper()} ({columns}) VALUES ({placeholders})"
            cursor = self.connection.cursor()
            cursor.execute(command, values)
            self.connection.commit()
            cursor.close()
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
            set_command = ", ".join(
                f"{column} = :{i+1}" for i, column in enumerate(columns)
            )
            command = f"UPDATE {table.upper()} SET {set_command} WHERE ID = :{len(columns) + 1}"
            cursor = self.connection.cursor()
            cursor.execute(command, (*values, id))
            self.connection.commit()
            cursor.close()
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
            command = f"UPDATE {table.upper()} SET {column} = :value WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, value=value, id=id)
            self.connection.commit()
            cursor.close()
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
            command = f"DELETE FROM {table.upper()} WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, id=id)
            self.connection.commit()
            cursor.close()
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
            command = f"SELECT * FROM {table.upper()}"
            cursor = self.connection.cursor()
            cursor.execute(command)
            usuarios = cursor.fetchall()
            cursor.close()
            return {
                "status": "success",
                "message": json.dumps(usuarios) if usuarios else "{}",
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
            command = f"SELECT * FROM {table.upper()} WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"id": id})
            usuarios = cursor.fetchone()
            if usuarios:
                columns = [desc[0] for desc in cursor.description]
                usuarios = dict(zip(columns, usuarios))
            return {
                "status": "success",
                "message": json.dumps(usuarios) if usuarios else "{}",
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
