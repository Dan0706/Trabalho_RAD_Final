import psycopg2


class DatabaseProdutos:
    def __init__(self):
        self.connection = None

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="063486",
                host="127.0.0.2",
                port="5432",
                database="estoque"
            )
        except (Exception, psycopg2.Error) as error:
            print("Falha ao se conectar ao Banco de Dados", error)
            self.connection = None

    def fecharConexao(self):
        if self.connection:
            self.connection.close()

    def listarProdutos(self):
        self.abrirConexao()
        if not self.connection:
            return []

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT  id, nome, quantidade, preco FROM produtos")
            produtos = cursor.fetchall()
            return produtos
        except (Exception, psycopg2.Error) as error:
            print("Erro ao listar produtos", error)
            return []
        finally:
            if cursor:
                cursor.close()
            self.fecharConexao()

    def adicionarProduto(self, nome, quantidade, preco):
        self.abrirConexao()
        if not self.connection:
            return False

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (%s, %s, %s)",
                           (nome, quantidade, preco))
            self.connection.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Erro ao adicionar produto", error)
            return False
        finally:
            if cursor:
                cursor.close()
            self.fecharConexao()

    def atualizarProduto(self, produto_id, nome=None, quantidade=None, preco=None):
        self.abrirConexao()
        if not self.connection:
            return False

        cursor = None
        try:
            cursor = self.connection.cursor()


            updates = []
            values = []

            if nome is not None:
                updates.append("nome = %s")
                values.append(nome)
            if quantidade is not None:
                updates.append("quantidade = %s")
                values.append(quantidade)
            if preco is not None:
                updates.append("preco = %s")
                values.append(preco)


            if not updates:
                print("Nenhum campo foi modificado.")
                return False


            values.append(produto_id)

            
            query = f"UPDATE produtos SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar produto", error)
            return False
        finally:
            if cursor:
                cursor.close()
            self.fecharConexao()

    def excluirProduto(self, produto_id):
        self.abrirConexao()
        if not self.connection:
            return False

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
            self.connection.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Erro ao excluir produto", error)
            return False
        finally:
            if cursor:
                cursor.close()
            self.fecharConexao()
