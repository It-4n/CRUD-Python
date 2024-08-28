import mysql.connector

# CONECTANDO AO BANCO DE DADOS
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123',
    database='crud'
)

cursor = conexao.cursor()

# CREATE
def create(cursor, conexao):
    nome = input("Nome do livro: ")
    autor = input("Autor: ")
    genero = input("Gênero(s): ")

    comando_create = 'INSERT INTO Livros (Nome, Autor, Genero) VALUES (%s, %s, %s)'
    valores = (nome, autor, genero)

    try:
        cursor.execute(comando_create, valores)
        conexao.commit()
        print()
        print("*Dados inseridos com sucesso!*")
    except mysql.connector.Error as err:
        print()
        print(f"*Erro ao inserir dados: {err}*")

# READ
def read(cursor):
    comando_read = 'SELECT * FROM Livros'

    if cursor.rowcount > 0:
        try:
            cursor.execute(comando_read)
            resultados = cursor.fetchall()

            for row in resultados:
                print(row)
        except mysql.connector.Error as err:
            print()
            print(f"*Erro ao consultar dados: {err}*")
    else:
        print()
        print("*Não existem livros cadastrados.*")

# UPDATE
def update(cursor, conexao):
    id = input("Informe o ID do livro que deseja atualizar: ")

    nome = input("Novo nome do livro: ")
    autor = input("Novo autor: ")
    genero = input("Novo(s) gênero(s): ")

    comando_update = 'UPDATE Livros SET Nome = %s, Autor = %s, Genero = %s WHERE ID = %s'
    valores = (nome, autor, genero, id)

    try:
        cursor.execute(comando_update, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print()
            print("*Dados atualizados com sucesso!*")
        else:
            print()
            print("*Nenhum livro encontrado com o ID fornecido.*")
    except mysql.connector.Error as err:
        print(f"*Erro ao atualizar dados: {err}*")

# DELETE
def delete(cursor, conexao):
    id = input("Informe o ID do livro a ser apagado: ")

    comando_delete = 'DELETE FROM Livros WHERE ID = %s'
    valor = (id,)

    try:
        cursor.execute(comando_delete, valor)
        conexao.commit()
        print()
        print("*Dados apagados com sucesso!*")
    except mysql.connector.Error as err:
        print()
        print(f"*Erro ao apagar dados: {err}*")

def default():
    print("Opção inválida. Por favor, escolha uma opção válida do menu.")

# MAPEAMENTO DAS OPÇÕES PARA FUNÇÕES
switch = {
    1: lambda: create(cursor, conexao),
    2: lambda: read(cursor),
    3: lambda: update(cursor, conexao),
    4: lambda: delete(cursor, conexao)
}

# LOOP DO MENU
while True:
    print("\nEscolha uma opção:")
    print("1 - Cadastrar novo livro")
    print("2 - Listar livros cadastrados")
    print("3 - Atualizar dados de um livro")
    print("4 - Apagar um livro")
    print("0 - Sair")
    print()

    try:
        opcao = int(input("Digite a opção ('0' para sair): "))
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        continue

    if opcao == 0:
        print("Saindo...")
        break

    if opcao in switch:
        switch[opcao]()
    else:
        default()

# FECHANDO CURSOR E CONEXÃO
cursor.close()
conexao.close()