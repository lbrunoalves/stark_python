class Tarefa:
    def __init__(self, id=None, desc: str = "", dt_ini: str = "", dt_fim: str = "", status: str = ""):
        self.id = id
        self.desc = desc
        self.dt_ini = dt_ini
        self.dt_fim = dt_fim
        self.status = status

