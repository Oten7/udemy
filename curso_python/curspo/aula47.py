nome = input("digite seu nome: ")
idade = (input("digite sua idade: "))

if nome and idade:
    print(f"Seu nome é  {nome}")
    print(f"Seu nome invetido é {nome[::-1]}")

    if ' ' in nome:
        print("Seu nome contem espaços")
    else:
        print('Seu nome nao contem espaços')

    print(f"Seu nome tem {len(nome)} letras")
    print(f"A primeira letra do seu nome é {nome[0]}")
    print(f"A ultima letra do seu nome é {nome[-1]}")

else:
    print("Desculpe, vc deixou cammpos vazios")