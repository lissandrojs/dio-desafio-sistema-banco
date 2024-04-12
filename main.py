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

def deposit(balance,value,extract,/):
    if value > 0:
        balance += value
        extract += f"Desosito: R$ {value:.2f}\n"
        print(f"Você depositou R$: {value:.2f}")
    else:
        print("Operação falhou! O valor informado e inválido.")
    return balance, extract

def to_withdraw(*,balance,value,extract,limit,withdrawal_numbers,withdrawal_limit):
    exceeded_balance =  value > balance
    exceeded_limit = value > limit
    execeeded_withdrawals = withdrawal_numbers > withdrawal_numbers

    if exceeded_balance:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif exceeded_limit:
        print("Operação falhou! Numero maximo de saques ecxcedido." )
    elif execeeded_withdrawals:
        print("Operação falhou! Número máximo de sques excedido.")
    elif value > 0:
        balance -= value
        extract += f"Saques: R$ {value:.2f}\n"
        withdrawal_numbers += 1
        print(f"Saque de R$: {value:.2f} realizado Realizado")
    else :
        print("Operação falhou! o valor informado e inválido.")
    
    return balance, extract

def display_extract(balance, /, *, extract):
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extract else extract)
            print(f"\nSaldo: R$ {balance:.2f}")
            print("==========================================")

def create_user(users):
    cpf = input("Informe o CPF (somente números): ")
    invalid_user = filter_user(cpf,users)

    if invalid_user:
        print("!!! Usuario existente com esse CPF !!!")
        return

    name = input("Informe o nome completo: ")
    address = input("Informe o endereço (dd-mm-aaaa): ")
    birth_date = input("Informe a data de nascimento (logradouro, numero , bairro , cidades, estado): ")

    users.append({
        "name": name,
        "address": address,
        "birth_date": birth_date,
        "cpf": cpf
        })    
    print("Usuário criado com sucesso!")

def create_account(agency,number_account,users):
    cpf = input("Informe o CPF (somente números): ")
    valid_user = filter_user(cpf,users)

    if valid_user:
        print("Conta Criada com sucesso !!")
        return {"agency": agency,"number_account": number_account,"user": valid_user}

    print("Usuario não encontrado, Crie um usuário!")

def filter_user(cpf,users):
    filter = [current_user for current_user in users if current_user["cpf"] == cpf]
    return filter[0] if filter else None

def list_accounts(accounts):
    for account in accounts:
        line = f"""
        Agência: {account['agency']}
        C/C: {account['number_account']}
        Titular: {account['user']['name']}
        """
        print(line)

def main():
    WITHDRAWAL_LIMIT = 3
    AGENCY = "0001"

    balance  = 0
    limit = 500
    extract = ""
    withdrawal_numbers = 0 
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            value = float(input("Informe o valor do deposito: "))

            balance, extract = deposit(balance,value,extract)
        
        elif option == "s":
            value = float(input("Infome o valor do saque: "))
            
            balance , extract = to_withdraw(
             balance=balance,
             value=value,
             extract=extract,
             limit=limit,
             withdrawal_numbers=withdrawal_numbers,
             withdrawal_limit=WITHDRAWAL_LIMIT   
            )

        elif option == "e":
            display_extract(balance,extract=extract)

        elif option == "nu":
            create_user(users)

        elif option == "nc":
            number_account = len(accounts) + 1
            account = create_account(AGENCY,number_account,users)

            if account:
                accounts.append(account)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break
    
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()