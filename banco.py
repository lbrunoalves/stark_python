from tarefa import *
import pymysql.cursors


class database:
    def __init__(self, host: str, username: str, db: str, password: str):
        try:
            self.conexao = pymysql.connect(host=host, user=username,
                                            db=db, password=password,
                                            cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.conexao.cursor()

        except Exception as erro:
            print(f"Erro ao conectar ao banco! Erro: {erro}")


    def insert(self, tarefa: Tarefa):
        try:
            sql = ('INSERT INTO tarefas (descricao, dt_ini, dt_fim, status) '
                   'VALUES (%s, %s, %s, %s)')
            self.cursor.execute(sql, (tarefa.desc, tarefa.dt_ini, tarefa.dt_fim, tarefa.status))
            self.conexao.commit()
            print('Tarefa cadastrada com sucesso!')
        except Exception as error:
            print(f'Erro ao inserir! Erro: {error}')

    def select_all(self):
        try:
            self.cursor.execute("SELECT * FROM tarefas")
            tarefas = self.cursor.fetchall()
            return tarefas
        except pymysql.connector.Error as error:
            print(f"Erro ao selecionar tarefas! Erro: {error}")
            return None

    def select_concluidas(self):
        try:
            self.cursor.execute("SELECT * FROM tarefas WHERE status = 'Concluído'")
            tarefas_concluidas = self.cursor.fetchall()
            return tarefas_concluidas
        except Exception as error:
            print(f"Erro ao selecionar tarefas concluídas! Erro: {error}")
            return None


    def update_status(self, id_tarefa: int, novo_status: str):
        try:
            sql = "UPDATE tarefas SET status = %s WHERE id = %s"
            self.cursor.execute(sql, (novo_status, id_tarefa))
            self.conexao.commit()
            print("Status da tarefa atualizado com sucesso!")
        except Exception as error:
            print(f"Erro ao atualizar o status da tarefa! Erro: {error}")

    def delete(self, id: int):
        try:
            sql = "DELETE FROM tarefas WHERE id = %s"
            self.cursor.execute(sql, (id,))
            self.conexao.commit()
            print("Tarefa excluída com sucesso!")
        except Exception as error:
            print(f"Erro ao excluir a tarefa! Erro: {error}")


