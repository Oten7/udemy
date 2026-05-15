while True:
    sair = input("Quer sair? [s/n] ")
    sair = sair.lower()
    sair = sair.startswith('s')
    print(sair)