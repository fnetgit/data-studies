from abc import ABC, abstractmethod
from datetime import datetime

from utilitarios.exceptions import SaldoInsuficienteError


class Conta(ABC):
    """
    Classe base abstrata para contas bancárias.
    Demonstra Herança e Encapsulamento.
    """

    _total_contas = 0

    def __init__(self, numero: int, cliente):

        self._numero = numero
        self._saldo = 0.0
        self._cliente = cliente
        self._historico = []
        Conta._total_contas += 1

    @property
    def saldo(self):
        """Getter para o saldo, permitindo acesso controlado."""
        return self._saldo

    @classmethod
    def get_total_contas(cls):
        """Método de classe para obter o número total de contas criadas."""

        return cls._total_contas

    def depositar(self, valor: float):

        if valor > 0:
            self._saldo += valor

            self._historico.append((datetime.now(), f"Depósito de R${valor:.2f}"))
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")

        else:
            print("Valor de depósito inválido.")

    @abstractmethod
    def sacar(self, valor: float):
        """Método abstrato para sacar um valor. Deve ser implementado pelas subclasses."""

    def extrato(self):
        """Exibe o extrato da conta."""
        print(f"\n--- Extrato da Conta Nº {self._numero} ---")
        print(f"Cliente: {self._cliente.nome}")
        print(f"Saldo atual: R${self._saldo:.2f}")
        print("Histórico de transações:")

        if not self._historico:
            print("Nenhuma transação registrada.")

        for data, transacao in self._historico:
            print(f"- {data.strftime('%d/%m/%Y %H:%M:%S')}: {transacao}")
        print("--------------------------------------\n")


class ContaCorrente(Conta):
    """
    Subclasse que representa uma conta corrente.
    Demonstra Polimorfismo ao sobrescrever o método sacar.
    """

    def __init__(self, numero: int, cliente, limite: float = 500.0):

        super().__init__(numero, cliente)

        self.limite = limite

    def sacar(self, valor: float):
        """Permite saque utilizando o saldo da conta mais o limite (cheque especial)."""

        if valor <= 0:
            print("Valor de saque inválido.")
            return

        saldo_disponivel = self._saldo + self.limite

        if valor > saldo_disponivel:
            raise SaldoInsuficienteError(
                saldo_disponivel, valor, "Saldo e limite insuficientes."
            )

        self._saldo -= valor

        self._historico.append((datetime.now(), f"Saque de R${valor:.2f}"))
        print(f"Saque de R${valor:.2f} realizado com sucesso.")


class ContaPoupanca(Conta):
    """Subclasse que representa uma conta poupança."""

    def sacar(self, valor: float):

        if valor <= 0:
            print("Valor de saque inválido.")
            return

        if valor > self._saldo:
            raise SaldoInsuficienteError(self._saldo, valor)

        self._saldo -= valor

        self._historico.append((datetime.now(), f"Saque de R${valor:.2f}"))
        print(f"Saque de R${valor:.2f} realizado com sucesso.")
