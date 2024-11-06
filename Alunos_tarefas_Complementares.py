import os

ARQUIVO = 'alunos.txt'

def criar_arquivo():
    arquivo = open(ARQUIVO, 'w')
    arquivo.close()
    print('Arquivo criado com sucesso!')
def cadastrar_aluno():

    nome = input("Digite o nome do aluno: ")
    email = input("Digite o email do aluno: ")
    curso = input("Digite o curso do aluno: ")

    with open(ARQUIVO, 'a') as arquivo:
        arquivo.write(f"{nome},{email},{curso}\n")
    print("Aluno cadastrado com sucesso!")


def listar_alunos():

    if not os.path.exists(ARQUIVO):
        print("Nenhum aluno cadastrado.")
        return

    with open(ARQUIVO, 'r') as arquivo:
        linhas = arquivo.readlines()
        if not linhas:
            print("Nenhum aluno cadastrado.")
            return

        print("Alunos cadastrados:")
        for linha in linhas:
            nome, email, curso = linha.strip().split(',')
            print(f"Nome: {nome}, Email: {email}, Curso: {curso}")


def buscar_aluno(nome_busca):

    if not os.path.exists(ARQUIVO):
        print("Nenhum aluno cadastrado.")
        return

    encontrado = False
    with open(ARQUIVO, 'r') as arquivo:
        for linha in arquivo:
            nome, email, curso = linha.strip().split(',')
            if nome.lower() == nome_busca.lower():
                print(f"Aluno encontrado: Nome: {nome}, Email: {email}, Curso: {curso}")
                encontrado = True
                break

    if not encontrado:
        print(f"Aluno com o nome '{nome_busca}' não encontrado.")


def menu():

    while True:
        print("\nMenu:")
        print("1. Cadastrar um novo aluno")
        print("2. Listar todos os alunos")
        print("3. Buscar um aluno pelo nome")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cadastrar_aluno()
        elif escolha == '2':
            listar_alunos()
        elif escolha == '3':
            nome_busca = input("Digite o nome do aluno que deseja buscar: ")
            buscar_aluno(nome_busca)
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

criar_arquivo()
if __name__ == "__main__":
    menu()