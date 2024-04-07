LIMITE_SAQUE = 3
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0 



while True:
    opcao = input(menu)

    if opcao == "d":
        print("Depositar")
    elif opcao == "s":
        print("Sacar")
    elif opcao == "e":
        print("Extrato")
    elif opcao == "q"
        print("Saindo")
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")