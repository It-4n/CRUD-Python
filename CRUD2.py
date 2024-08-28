import mysql.connector
import bcrypt

# CONECTANDO AO BANCO DE DADOS
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123',
    database='crud2'
)

cursor = conexao.cursor()

# CREATE
def create(cursor, conexao):
    nome = input("Digite o nome do funcionário: ")
    senha = input("Crie uma senha: ")

    # HASH DA SENHA
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    comando_create = 'INSERT INTO Funcionarios (Nome, Senha) VALUES (%s, %s)'
    valores = (nome, hash_senha)

    try:
        cursor.execute(comando_create, valores)
        conexao.commit()
        print("\n*Cadastro criado com sucesso!*")
    except mysql.connector.Error as err:
        print(f"\n*Erro ao criar cadastro: {err}*")

# READ
def read(cursor):
    comando_read = 'SELECT * FROM Funcionarios'

    try:
        cursor.execute(comando_read)
        resultados = cursor.fetchall()

        for row in resultados:
            print(row)
    except mysql.connector.Error as err:
        print()
        print(f"*Erro ao consultar dados: {err}*")

# UPDATE
def update(cursor, conexao):
    id = input("Informe o ID do funcionário cadastrado que deseja atualizar o nome: ")
    nome = input("Novo nome do funcionário: ")
    senha = input("Nova senha do funcionário: ")

    # HASH DA NOVA SENHA
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    comando_update = 'UPDATE Funcionarios SET Nome = %s, Senha = %s WHERE ID = %s'
    valores = (nome, hash_senha, id)

    try:
        cursor.execute(comando_update, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print("\n*Nome e senha atualizados com sucesso!*")
        else:
            print("\n*Nenhum funcionário encontrado com o ID fornecido.*")
    except mysql.connector.Error as err:
        print(f"*Erro ao atualizar dados: {err}*")

# DELETE
def delete(cursor, conexao):
    id = input("Informe o ID do funcionário a ser apagado: ")

    comando_delete = 'DELETE FROM Funcionarios WHERE ID = %s'
    valor = (id,)

    try:
        cursor.execute(comando_delete, valor)
        conexao.commit()
        print()
        print("*Dados apagados com sucesso!*")
    except mysql.connector.Error as err:
        print()
        print(f"*Erro ao apagar dados: {err}*")

# AUTHENTICATE
def authenticate(cursor):
    nome = input("Digite o nome do funcionário: ")
    senha = input("Digite a senha: ")

    comando_read = 'SELECT Senha FROM Funcionarios WHERE Nome = %s'
    valores = (nome,)

    try:
        cursor.execute(comando_read, valores)
        resultado = cursor.fetchone()
        if resultado:
            hash_banco = resultado[0]
            if bcrypt.checkpw(senha.encode('utf-8'), hash_banco.encode('utf-8')):
                print("\n*Autenticação bem-sucedida!*")
            else:
                print("\n*Senha incorreta!*")
        else:
            print("\n*Funcionário não encontrado!*")
    except mysql.connector.Error as err:
        print(f"*Erro ao autenticar: {err}*")

# DEFAULT
def default():
    print("Opção inválida. Por favor, escolha uma opção válida do menu.")

# MAPEAMENTO DAS OPÇÕES PARA FUNÇÕES
switch = {
    1: lambda: create(cursor, conexao),
    2: lambda: read(cursor),
    3: lambda: update(cursor, conexao),
    4: lambda: delete(cursor, conexao),
    5: lambda: authenticate(cursor)
}

# LOOP DO MENU
while True:
    print("\nEscolha uma opção:")
    print("1 - Cadastrar funcionário")
    print("2 - Listar funcionários cadastrados")
    print("3 - Atualizar dados de um funcionário")
    print("4 - Deletar um funcionário")
    print("5 - Autenticar funcionário")
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