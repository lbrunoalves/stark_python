create database stark;
use stark;

CREATE TABLE tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(150) NOT NULL,
    dt_ini DATE NOT NULL,
    dt_fim DATE NOT NULL,
    status ENUM('A fazer', 'Em andamento', 'Concluído') NOT NULL
);

describe tarefas;
select * from tarefas;