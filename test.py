# Desafio - Otimizando o Sistema Bancário com Funções Python
# Este código é a solução completa para o desafio proposto.

import textwrap

def exibir_menu():
    """Exibe o menu de opções para o usuário."""
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExibir Extrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    => """
    # textwrap.dedent remove a indentação inicial da string
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    """
    Realiza a operação de depósito.
    Recebe saldo, valor e extrato como argumentos POSICIONAIS.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite_saque, numero_saques, limite_diario_saques):
    """
    Realiza a operação de saque.
    Recebe todos os argumentos como argumentos NOMEADOS (keyword-only).
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite_saque
    excedeu_saques = numero_saques >= limite_diario_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limITE:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {limite_saque:.2f}. @@@")
    elif excedeu_saques:
        print(f"\n@@@ Operação falhou! Número máximo de {limite_diario_saques} saques diários atingido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    Recebe saldo como POSICIONAL e extrato como NOMEADO.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def filtrar_usuario_por_cpf(cpf, usuarios):
    """Filtra e retorna um usuário da lista pelo CPF, se existir."""
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
    """Cria um novo usuário (cliente) para o banco."""
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario_por_cpf(cpf, usuarios)

    if usuario_existente:
        print(f"\n@@@ Já existe um usuário com o CPF {cpf}! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adiciona o novo usuário (como um dicionário) à lista de usuários
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print(f"\n=== Usuário {nome} criado com sucesso! ===")


def criar_conta(agencia, usuarios, contas):
    """Cria uma nova conta bancária vinculada a um usuário."""
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = filtrar_usuario_por_cpf(cpf, usuarios)

    if usuario:
        # O número da conta será sequencial (1, 2, 3...)
        numero_conta = len(contas) + 1
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        
        contas.append(conta)
        print(f"\n=== Conta {numero_conta} (Agência {agencia}) criada com sucesso para {usuario['nome']}! ===")
    else:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! Crie o usuário antes de criar a conta. @@@")


def listar_contas(contas):
    """Exibe uma lista de todas as contas cadastradas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada no sistema. @@@")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        linha = f"""\
            Agência: \t{conta['agencia']}
            C/C: \t\t{conta['numero_conta']}
            Titular: \t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
        print("-------------------------------------------------")
    print("===================================================")


def main():
    """Função principal que executa o sistema bancário."""
    # Constantes
    AGENCIA = "0001"
    LIMITE_SAQUE = 500
    LIMITE_DIARIO_SAQUES = 3

    # Variáveis de estado
    saldo = 0.0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    print("Bem-vindo ao Banco DIO!")

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            # A função 'depositar' retorna os novos valores
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            # A função 'sacar' retorna os novos valores
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite_saque=LIMITE_SAQUE,
                numero_saques=numero_saques,
                limite_diario_saques=LIMITE_DIARIO_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            # A função 'criar_usuario' modifica a LISTA 'usuarios'
            # Listas são mutáveis, então não precisamos retorná-la
            criar_usuario(usuarios)

        elif opcao == "nc":
            # A função 'criar_conta' modifica a LISTA 'contas'
            criar_conta(AGENCIA, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema. Até logo!")
            break

        else:
            print("\n@@@ Operação inválida! Por favor, selecione novamente a operação desejada. @@@")


# Ponto de entrada do programa: só executa 'main' se este script
# for rodado diretamente (e não importado como um módulo)
if __name__ == "__main__":
    main()