WITHDRAWAL_LIMIT = 3
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

balance  = 0
limit = 500
extract = ""
withdrawal_numbers = 0 



while True:
    option = input(menu)

    if option == "d":
        value = float(input("Informe o valor do deposito:"))

        if value > 0:
            balance += value
            extract += f"Desosito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado e inválido.")
    
    elif option == "s":
        value = float(input("Infome o valor do saque"))
        
        exceeded_balance =  value > balance
        exceeded_limit = value > limit
        execeeded_withdrawals = value > whitdrawal_numbers

        if execeed_balance:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif exceeded_limit:
            print("Operação falhou! Numero maximo de saques ecxcedido." )
        elif execeeded_withdrawals:
            print("Operação falhou! Número máximo de sques excedido.")
        elif valor > 0:
            balance -= value
            extract += f"Saques: R$ {valor:.2f}\n"
            withdrawal_numbers += 1
        else :
            print("Operação falhou! o valor informado e inválido.")

    elif option == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extract else extract)
        print(f"\nSaldo: R$ {balance:.2f}")
        print("==========================================")
    
    elif option == "q":
        break
   
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")