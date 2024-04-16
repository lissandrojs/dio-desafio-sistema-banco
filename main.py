from abc import ABC, abstractmethod
from datetime import datetime


class History:
    def __init__(self):
        self._transaction = []

    @property
    def transactions(self):
        return self._transaction
    
    def add_new_transactions(self, transaction):
        self._transaction.append({
            "tipo": transaction.__class__.__name__,
            "valor":transaction.value,
            "data": datetime.now()
            })

class Account:
    def __init__(self,number,client):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls,client,number):
        return cls(number,client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency
    
    @property
    def history(self):
        return self._history
    
    def withdraw(self,value):
        balance  = self.balance
        exceeded_balance =  value > balance

        if exceeded_balance:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif value > 0:
            print(f"Saque de R$: {value:.2f} realizado Realizado")
            self._balance -= value 
            return True 
        else :
            print("Operação falhou! o valor informado e inválido.")
        
        return False

    def  depost(self,value):
        if value > 0:
            self._balance += value
            print(f"Você depositou R$: {value:.2f}")
        else:
            print("Operação falhou! O valor informado e inválido.")
            False

        return True

class CurrentAccount(Account):
    def __init__(self,number,client,limit=500,limit_withdrawals=3):
        super.__init__(number,client)
        self._limit = limit
        self._limit_withdrawals = limit_withdrawals
    
    def withdraw(self,value):
        number_of_withdrawals = len([transaction for transaction in self.history.transactions if transaction["tipo"] ] == "saque")
        
        exceeded_limit = value > self.limit
        execeeded_withdrawals = number_of_withdrawals > self._limit

        if exceeded_limit:
            print("Operação falhou! Numero maximo de saques ecxcedido." )
        elif execeeded_withdrawals:
            print("Operação falhou! Número máximo de saques excedido.")
        else :
            return super().sacar(value)
        
        return False

    def __str__(self):
        return f"""
        Agência: {self.agency}
        C/C: {self.number}
        Titular: {self.client.name}
        """

class Client:
    def __init__(self,address):
        self.address = address
        self.accounts = []
    
    def make_transaction(self,account,transaction):
        transaction.register(account)

    def add_account(self,account):
        self.accounts.append(account)

class PrivateIndiavidual(Client):
    def __init__(self,cpf,name,date_of_birth):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.date_of_birth = date_of_birth

class Transaction(ABC):
        @property
        @abstractmethod
        def value(self):
            pass
        @classmethod
        @abstractmethod
        def register(self, account):
            pass
    

class Withdraw(Transaction):
    def __init__(self,value):
        return self._value - value

    @property
    def value(self):
        return self._value

    def register(self,account):
        success_transaction = account.withdraw(self.value)

        if success_transaction:
            account.history.add_new_transactions(self)

class Deposit(Transaction):
    def __init__(self,value):
        return self._value - value

    @property
    def value(self):
        return self._value

    def register(self,account):
        success_transaction = account.depost(self.value)

        if success_transaction:
            account.history.add_new_transactions(self)

def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair

    => """
    return input(menu)

def filter_client_bank(cpf,users):
    filter = [current_user for current_user in users if current_user.cpf == cpf]
    return filter[0] if filter else None

def to_withdraw(clients):
    cpf = input("Informe o CPF (somente números): ")
    client_bank = filter_client_bank(cpf,clients)

    if not client_bank:
        print("Cliente não encontrado ! ")
        return

    value = float("Informe o valor do saque: ")

    transaction = Withdraw(value)
    account = recover_customer_account(client_bank)
    
    if not account:
        return
    
    client_bank.make_transaction(account,transaction)

def deposit(clients):
    cpf = input("Informe o CPF (somente números): ")
    client_bank = filter_client_bank(cpf,clients)

    if not client_bank:
        print("!!! Usuario existente com esse CPF !!!")
        return

    value = float(input("Infome o valor do deposito: "))
    transaction = Deposit(value)

    account = recover_customer_account(client_bank)
    if not account:
        return 
    
    client_bank.make_transaction(account,transaction)

def recover_customer_account(client):
    if not client.account:
        print("Cliente não possui conta !")
        return
    
    return client.account[0]

def display_extract(clients):
    cpf = input("Informe o CPF (somente números): ")
    client_bank = filter_client_bank(cpf,clients)

    if not client_bank:
        print("!!! Usuario existente com esse CPF !!!")
        return

    account = recover_customer_account(client_bank)
    if not account:
        return 
    
    transactions = account.history.transactions 
    extract= ""
    
    print("\n================ EXTRATO ================")
    if not transactions:
        extract = "Nenhuma transação realizada"

    else:
        for  transaction in transactions :
            extract += f"\n\ {transaction['tipo']}:\n\tR$ {transaction['valor']:.2f}"


    print(extract)
    print(f"\nSaldo: R$ {account.balance:.2f}")
    print("==========================================")

def create_user(users):
    cpf = input("Informe o CPF (somente números): ")
    invalid_user = filter_client_bank(cpf,users)

    if invalid_user:
        print("!!! Usuario existente com esse CPF !!!")
        return

    name = input("Informe o nome completo: ")
    address = input("Informe o endereço (dd-mm-aaaa): ")
    birth_date = input("Informe a data de nascimento (logradouro, numero , bairro , cidades, estado): ")

    client = PrivateIndiavidual(name=name,date_of_birth=birth_date,address=address)
    users.append(client)
    print("Cliente Criado com sucesso!")



def create_account(number_account,users,accounts):
    cpf = input("Informe o CPF (somente números): ")
    valid_user = filter_client_bank(cpf,users)

    if not valid_user:
        print("Usuario não encontrado, Crie um usuário!!")
        return 

    account = CurrentAccount.new_account(client=users,number=number_account)
    accounts.append(account)
    users.accounts.append(account)
    print("Conta criada com sucesso! ")

def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(account)
        print("=" * 100)

def main():
    users = []
    accounts = []   

    while True:
        option = menu()

        if option == "d":
            deposit(users)
        
        elif option == "s":
           to_withdraw(users)

        elif option == "e":
            display_extract(users)

        elif option == "nu":
            create_user(users)

        elif option == "nc":
            number_account = len(accounts)
            create_account(number_account,users,accounts)

        elif option == "lc":
            list_accounts(accounts)    

        elif option == "q":
            break
    
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()