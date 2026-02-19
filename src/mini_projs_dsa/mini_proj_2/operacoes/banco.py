from entidades.cliente import Cliente
from entidades.conta import Conta, ContaCorrente, ContaPoupanca
from utilitarios.exceptions import ContaInexistenteError


class Banco:
    """
    Classe que gerencia as operações do banco.
    Demonstra Composição, pois "tem" clientes e contas.
    """

    def __init__(self, nome: str):

        self.nome = nome

        # chave: CPF, valor: objeto Cliente
        self._clientes = {}

        # chave: número da conta, valor: objeto Conta
        self._contas = {}

    def adicionar_cliente(self, nome: str, cpf: str) -> Cliente:
        """Cria e adiciona um novo cliente ao banco."""

        if cpf in self._clientes:
            print("Erro: Cliente com este CPF já cadastrado.")
            return self._clientes[cpf]

        novo_cliente = Cliente(nome, cpf)
        self._clientes[cpf] = novo_cliente

        print(f"Cliente {nome} adicionado com sucesso!")

        return novo_cliente

    def criar_conta(self, cliente: Cliente, tipo: str) -> Conta | None:
        """Cria uma nova conta para um cliente existente."""

        numero_conta = Conta.get_total_contas() + 1

        if tipo.lower() == "corrente":
            nova_conta = ContaCorrente(numero_conta, cliente)

        elif tipo.lower() == "poupanca":
            nova_conta = ContaPoupanca(numero_conta, cliente)

        else:
            print("Tipo de conta inválido. Escolha 'corrente' ou 'poupanca'.")
            return None

        self._contas[numero_conta] = nova_conta

        cliente.adicionar_conta(nova_conta)
        print(f"Conta {tipo} nº {numero_conta} criada para o cliente {cliente.nome}.")

        return nova_conta

    def buscar_conta(self, numero_conta: int) -> Conta:
        """Busca uma conta pelo seu número."""

        conta = self._contas.get(numero_conta)

        if not conta:
            raise ContaInexistenteError(numero_conta)
        return conta

    def buscar_cliente(self, cpf: str) -> Cliente | None:
        """Busca um cliente pelo CPF."""

        return self._clientes.get(cpf)
