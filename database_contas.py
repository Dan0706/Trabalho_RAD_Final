import psycopg2


class DatabaseContas:
    def __init__(self):
        self.connection = None

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="063486",
                host="127.0.0.2",
                port="5432",
                database="contas"
            )
        except (Exception, psycopg2.Error) as error:
            print("Falha ao se conectar ao Banco de Dados", error)
            self.connection = None

    def fecharConexao(self):
        if self.connection:
            self.connection.close()

    def verificarLogin(self, username, password):
        self.abrirConexao()
        if not self.connection:
            return False

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM contas WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result is not None
        except (Exception, psycopg2.Error) as error:
            print("Erro na consulta ao Banco de Dados", error)
            return False
        finally:
            if cursor:
                cursor.close()
            self.fecharConexao()

    def cadastrarUsuario(self, username, password):
        self.abrirConexao()
        if not self.connection:
            return False

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO contas (username, password) VALUES (%s, %s)", (username, password))
            self.connection.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Erro ao cadastrar usuário", error)
            return False
        finally:
            if cursor:
                cursor.close()
            self.fecharConexao()
