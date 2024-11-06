import sqlite3

from Alunos import criar_arquivo


def conectar():
    return sqlite3.connect('usuarios.db.db')



def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



def pessoa_existe(nome, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM pessoas WHERE nome = ? AND email = ?
    ''', (nome, email))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None



def inserir_pessoa(nome, idade, email):
    if not pessoa_existe(nome, email):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pessoas (nome, idade, email)
            VALUES (?, ?, ?)
        ''', (nome, idade, email))
        conn.commit()
        conn.close()
        print("Pessoa inserida com sucesso!")
    else:
        print(f"A pessoa com nome '{nome}' e email '{email}' já está cadastrada.")



def consultar_pessoa_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM pessoas WHERE nome = ?
    ''', (nome,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados



def alterar_pessoa(id_pessoa, novo_nome, nova_idade, novo_email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pessoas
        SET nome = ?, idade = ?, email = ?
        WHERE id = ?
    ''', (novo_nome, nova_idade, novo_email, id_pessoa))
    conn.commit()
    conn.close()



def verificar_id_existe(id_pessoa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pessoas WHERE id = ?', (id_pessoa,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def excluir_pessoa(id_pessoa):
    if verificar_id_existe(id_pessoa):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pessoas WHERE id = ?', (id_pessoa,))
        conn.commit()
        conn.close()
        print("Pessoa excluída com sucesso!")
    else:
        print(f"Pessoa com ID {id_pessoa} não encontrada no banco de dados.")




def validar_nome(nome):
    nome = nome.strip()
    return all(caractere.isalpha() or caractere.isspace() for caractere in nome) and nome != ""



def validar_idade(idade):
    try:
        idade = int(idade)
        if idade > 0:
            return idade
        else:
            print("A idade deve ser um número positivo.")
            return None
    except ValueError:
        print("Por favor, insira uma idade válida (número).")
        return None



def validar_email(email):
    if "@" in email and "." in email:
        return email
    else:
        print("Email inválido. Por favor, insira um email válido.")
        return None


def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Inserir nova pessoa")
        print("2. Consultar pessoa pelo nome")
        print("3. Alterar pessoa")
        print("4. Excluir pessoa")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            while not validar_nome(nome):
                print("Nome inválido. O nome não pode conter números ou caracteres especiais.")
                nome = input("Nome: ")

            idade = input("Idade: ")
            idade = validar_idade(idade)
            while idade is None:
                idade = input("Idade: ")
                idade = validar_idade(idade)

            email = input("Email: ")
            email = validar_email(email)
            while email is None:
                email = input("Email: ")
                email = validar_email(email)

            inserir_pessoa(nome, idade, email)

        elif escolha == '2':
            nome = input("Digite o nome da pessoa que deseja consultar: ")
            while not validar_nome(nome):
                print("Nome inválido. O nome não pode conter números ou caracteres especiais.")
                nome = input("Digite o nome da pessoa que deseja consultar: ")

            pessoas = consultar_pessoa_por_nome(nome)
            if pessoas:
                print("\n--- Pessoa(s) Encontrada(s) ---")
                for pessoa in pessoas:
                    print(f"ID: {pessoa[0]}, Nome: {pessoa[1]}, Idade: {pessoa[2]}, Email: {pessoa[3]}")
            else:
                print("Nenhuma pessoa encontrada com esse nome.")

        elif escolha == '3':
            id_pessoa = input("ID da pessoa a ser alterada: ")
            try:
                id_pessoa = int(id_pessoa)
            except ValueError:
                print("ID inválido. Deve ser um número.")
                continue

            nome = input("Novo nome: ")
            while not validar_nome(nome):
                print("Nome inválido. O nome não pode conter números ou caracteres especiais.")
                nome = input("Novo nome: ")

            idade = input("Nova idade: ")
            idade = validar_idade(idade)
            while idade is None:
                idade = input("Nova idade: ")
                idade = validar_idade(idade)

            email = input("Novo email: ")
            email = validar_email(email)
            while email is None:
                email = input("Novo email: ")
                email = validar_email(email)

            alterar_pessoa(id_pessoa, nome, idade, email)
            print("Pessoa alterada com sucesso!")

        elif escolha == '4':
            id_pessoa = input("ID da pessoa a ser excluída: ")
            try:
                id_pessoa = int(id_pessoa)
                excluir_pessoa(id_pessoa)
            except ValueError:
                print("ID inválido. Deve ser um número.")

        elif escolha == '5':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")





if __name__ == "__main__":
    criar_tabela()
    menu()
