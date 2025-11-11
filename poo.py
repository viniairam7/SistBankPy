from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    
    def gerar_relatorio(self, saldo):
        if not self._transacoes:
            return "Não foram realizadas movimentações."
        
        extrato_str = ""
        for transacao in self._transacoes:
            extrato_str += f"{transacao['data']}\t{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}\n"
        
        extrato_str += f"\nSaldo:\t\tR$ {saldo:.2f}"
        return extrato_str

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saque=500, limite_diario_saques=3):
        super().__init__(numero, cliente)
        self._limite_saque = limite_saque
        self._limite_diario_saques = limite_diario_saques
        self._numero_saques_hoje = 0

    def sacar(self, valor):
        if valor > self._limite_saque:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self._limite_saque:.2f}. @@@")
            return False
        
        if self._numero_saques_hoje >= self._limite_diario_saques:
            print(f"\n@@@ Operação falhou! Número máximo de {self._limite_diario_saques} saques diários atingido. @@@")
            return False

        sucesso_no_saque = super().sacar(valor)
        
        if sucesso_no_saque:
            self._numero_saques_hoje += 1
            return True
        
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

def exibir_menu():
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
    return input(textwrap.dedent(menu))

def filtrar_cliente_por_cpf(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta cadastrada! @@@")
        return None
    return cliente.contas[0]

def realizar_deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacao.registrar(conta)

def realizar_saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacao.registrar(conta)

def exibir_extrato_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    relatorio = conta.historico.gerar_relatorio(conta.saldo)
    print(relatorio)
    print("==========================================")

def criar_novo_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente_existente = filtrar_cliente_por_cpf(cpf, clientes)

    if cliente_existente:
        print(f"\n@@@ Já existe um usuário com o CPF {cpf}! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(novo_cliente)

    print(f"\n=== Usuário {nome} criado com sucesso! ===")

def criar_nova_conta(contas, clientes):
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! Crie o usuário antes de criar a conta. @@@")
        return

    numero_conta = len(contas) + 1
    nova_conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)
    
    print(f"\n=== Conta {numero_conta} (Agência {nova_conta.agencia}) criada com sucesso para {cliente.nome}! ===")

def listar_contas_cadastradas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada no sistema. @@@")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print(textwrap.dedent(str(conta)))
        print("-------------------------------------------------")
    print("===================================================")

def main():
    clientes = []
    contas = []

    print("Bem-vindo ao Banco DIO (Versão POO)!")

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            realizar_deposito(clientes)
        elif opcao == "s":
            realizar_saque(clientes)
        elif opcao == "e":
            exibir_extrato_cliente(clientes)
        elif opcao == "nu":
            criar_novo_cliente(clientes)
        elif opcao == "nc":
            criar_nova_conta(contas, clientes)
        elif opcao == "lc":
            listar_contas_cadastradas(contas)
        elif opcao == "q":
            print("\nObrigado por usar nosso sistema. Até logo!")
            break
        else:
            print("\n@@@ Operação inválida! Por favor, selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()
