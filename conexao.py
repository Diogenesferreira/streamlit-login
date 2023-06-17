import sqlite3 as sq
from pathlib import Path


class DataBase():
    def __init__(self, directory, name_db):
        self.diretorio = Path(directory)
        self.conn = sq.connect(self.diretorio / name_db)
        self.cur = self.conn.cursor()

    def criar_tabela(self, query):
        try:
            self.cur.execute(query)
        except sq.OperationalError:
            return False
        else:
            return True

    def criar_usuario(self, nome, cpf, usuario, senha):
        self.cur.execute(
            """INSERT INTO usuarios (nome, cpf, usuario, senha)
               VALUES (?, ?, ?, ?);
            """, (nome, cpf, usuario, senha)
        )
        self.conn.commit()
        return True

    def ver_usuarios(self):
        self.cur.execute("SELECT id, nome, cpf FROM usuarios ORDER BY id")
        return self.cur.fetchall()

    def fechar_conexao(self):
        self.conn.close()

    def usuario_existe(self, usuario):
        result = self.cur.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        return result is not None

    def autenticar_usuario(self, usuario):
        result = self.cur.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        return result[0] if result else None

    def autenticar_senha(self, usuario):
        result = self.cur.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        return result[0] if result else None

    def deletar_usuario(self, usuario):
        self.cur.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
        self.conn.commit()
        return True


"""
__init__(self, directory, name_db):
É o método de inicialização da classe. Ele recebe o diretório do banco de dados e o nome do arquivo do banco de dados como parâmetros. Ele cria uma conexão com o banco de dados usando o módulo sqlite3 e define o cursor para executar as consultas SQL.

criar_tabela(self, query):
Cria uma tabela no banco de dados com base na consulta SQL fornecida como parâmetro. Ele executa a consulta usando o cursor e captura a exceção OperationalError caso a tabela já exista. Retorna True se a tabela foi criada com sucesso e False se a tabela já existir.

criar_usuario(self, nome, cpf, usuario, senha):
Insere um novo usuário na tabela "usuarios" do banco de dados. Recebe o nome, CPF, usuário e senha como parâmetros. Executa uma consulta SQL para inserir os valores na tabela e, em seguida, faz o commit da transação. Retorna True se o usuário foi criado com sucesso.

ver_usuarios(self):
Executa uma consulta SQL para selecionar todos os usuários da tabela "usuarios" e retorna os resultados em forma de lista de tuplas.

fechar_conexao(self):
Fecha a conexão com o banco de dados.

usuario_existe(self, usuario):
Verifica se um determinado usuário existe na tabela "usuarios". Executa uma consulta SQL para selecionar o usuário com base no nome de usuário fornecido como parâmetro. Retorna True se o usuário existir no banco de dados.

autenticar_usuario(self, usuario):
Autentica o usuário com base no nome de usuário fornecido como parâmetro. Executa uma consulta SQL para selecionar o usuário com o nome de usuário especificado. Se o usuário existir, retorna o nome de usuário; caso contrário, retorna None.

autenticar_senha(self, usuario):
Autentica a senha do usuário com base no nome de usuário fornecido como parâmetro. Executa uma consulta SQL para selecionar a senha do usuário com o nome de usuário especificado. Se a senha existir, retorna a senha; caso contrário, retorna None.

deletar_usuario(self, usuario)
Recebe um usuario e o deleta do banco

"""