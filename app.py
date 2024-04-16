import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tarefa import Tarefa
from banco import database
import datetime


class TarefasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Projeto de Tarefas")
        self.root.configure(bg="red")
        self.db = database("localhost", "root", "stark", "3264")
        self.corpo()
        self.carregar_tarefas()

    def corpo(self):
        adicionar_frame = tk.Frame(self.root)
        adicionar_frame.pack(padx=10, pady=5, fill="x")
        adicionar_frame.configure(background='red')

        # Labels do primeiro frame
        tk.Label(adicionar_frame, background='red', text="Descrição da Tarefa:").pack(side="left")
        self.descricao_entry = tk.Entry(adicionar_frame, width=40)
        self.descricao_entry.pack(side="left", padx=5)
        self.descricao_entry.configure(background='red')

        tk.Label(adicionar_frame, background='red', text="Data de Início (DD/MM/YYYY):").pack(side="left")
        self.dt_ini_entry = tk.Entry(adicionar_frame, width=12)
        self.dt_ini_entry.pack(side="left", padx=5)
        self.dt_ini_entry.configure(background='red')

        tk.Label(adicionar_frame, background='red', text="Data de Fim (DD/MM/YYYY):").pack(side="left")
        self.dt_fim_entry = tk.Entry(adicionar_frame, width=12)
        self.dt_fim_entry.pack(side="left", padx=5)
        self.dt_fim_entry.configure(background='red')

        tk.Label(adicionar_frame, background='red', text="Status:").pack(side="left")
        self.status_combobox = ttk.Combobox(adicionar_frame, values=["A fazer", "Em andamento", "Concluído"])
        self.status_combobox.pack(side="left", padx=5)
        self.status_combobox.set("A fazer")
        self.status_combobox.configure(background='red')


        # Botões do primeiro frame
        self.adicionar_button = tk.Button(adicionar_frame, background='red', text="Adicionar", command=self.adicionar_tarefa)
        self.adicionar_button.pack(side="left", padx=5)
        self.adicionar_button.configure(background='red')

        self.remover_button = tk.Button(adicionar_frame, text="Remover Concluídas", command=self.remover_concluidas)
        self.remover_button.pack(side="right", padx=5)
        self.remover_button.configure(background='red')


        # Frame para lista de tarefas
        lista_frame = tk.Frame(self.root)
        lista_frame.pack(padx=10, pady=5, fill="both", expand=True)
        lista_frame.configure(background="red")

        self.tarefas_treeview = ttk.Treeview(lista_frame,
                                             columns=("ID", "Descrição", "Data de Início", "Data de Fim", "Status"),
                                             show="headings")
        self.tarefas_treeview.pack(fill="both", expand=True)
        self.tarefas_treeview.heading("ID", text="ID")
        self.tarefas_treeview.heading("Descrição", text="Descrição")
        self.tarefas_treeview.heading("Data de Início", text="Data de Início")
        self.tarefas_treeview.heading("Data de Fim", text="Data de Fim")
        self.tarefas_treeview.heading("Status", text="Status")


        # Botão para lista de tarefas
        self.alterar_status_button = tk.Button(lista_frame, text="Alterar Status", command=self.alterar_status_tarefas)
        self.alterar_status_button.pack(side="bottom", pady=5)
        self.alterar_status_button.configure(background="red")

    def adicionar_tarefa(self):
        desc = self.descricao_entry.get()
        dt_ini = self.formatar_data(self.dt_ini_entry.get())
        dt_fim = self.formatar_data(self.dt_fim_entry.get())
        status = self.status_combobox.get()

        if desc and dt_ini and dt_fim:
            nova_tarefa = Tarefa(desc=desc, dt_ini=dt_ini, dt_fim=dt_fim, status=status)
            self.db.insert(nova_tarefa)
            self.carregar_tarefas()
            self.limpar_campos()
        else:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")

    def formatar_data(self, data):
        if isinstance(data, str):
            dia, mes, ano = data.split("/")
            return f"{ano}-{mes}-{dia}"
        elif isinstance(data, datetime.date):
            return data.strftime("%d/%m/%Y")

    def carregar_tarefas(self):
        # Limpar o TreeView antes de carregar as tarefas
        for item in self.tarefas_treeview.get_children():
            self.tarefas_treeview.delete(item)

        # Obter todas as tarefas do banco de dados
        tarefas = self.db.select_all()
        if tarefas:
            for tarefa in tarefas:
                dt_ini_formatada = self.formatar_data(tarefa['dt_ini'])
                dt_fim_formatada = self.formatar_data(tarefa['dt_fim'])
                self.tarefas_treeview.insert("", tk.END, values=(
                    tarefa['id'], tarefa['descricao'], dt_ini_formatada, dt_fim_formatada, tarefa['status']))
    def limpar_campos(self):
        self.descricao_entry.delete(0, tk.END)
        self.dt_ini_entry.delete(0, tk.END)
        self.dt_fim_entry.delete(0, tk.END)
        self.status_combobox.set("A fazer")

    def remover_concluidas(self):
        tarefas_concluidas = self.db.select_concluidas()
        if tarefas_concluidas:
            for tarefa in tarefas_concluidas:
                self.db.delete(tarefa['id'])
            self.carregar_tarefas()
            messagebox.showinfo("Tarefas Removidas", "Tarefas concluídas removidas com sucesso.")
        else:
            messagebox.showinfo("Nenhuma Tarefa Concluída", "Não há tarefas concluídas para remover.")

    def alterar_status_tarefas(self):
        selecionado = self.tarefas_treeview.selection()
        if selecionado:
            id_tarefa = self.tarefas_treeview.item(selecionado)['values'][0]
            novo_status = self.status_combobox.get()
            self.db.update_status(id_tarefa, novo_status)
            self.carregar_tarefas()
        else:
            messagebox.showwarning("Nenhuma Tarefa Selecionada",
                                   "Por favor, selecione uma tarefa para atualizar o status.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TarefasApp(root)
    root.mainloop()

