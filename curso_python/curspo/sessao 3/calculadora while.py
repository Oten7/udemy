while True:
    numero_1 = input("digite um numero: ")
    numero_2 = input("digite outro numero: ")
    operador = input("digite um operador (+-/*): ")

    numeros_validos = None
    num_1_float = 0
    num_2_float = 0

    try:
        num_1_float = float(numero_1)
        num_2_float = float(numero_2)
        numeros_validos = True
    except:
        numeros_validos = None

    if numeros_validos is None:
        print("numeros invalidos")
        continue

    operadores_validos = '+-/*'

    if len(operador) > 1:
        print("digite apenas um operador")
        continue

    if operador not in operadores_validos:
        print("operador invalido")
        continue
    print("realizando sua conta. Confira os resultados abaixo")
    print(" ")
    if operador == "+":
        print(f"{num_1_float} + {num_2_float} =",num_1_float + num_2_float)
    elif operador == "-":
        print(f"{num_1_float} - {num_2_float} =",num_1_float - num_2_float)
    elif operador == "*":
        print(f"{num_1_float} * {num_2_float} =",num_1_float * num_2_float)
    elif operador == "/":
        print(f"{num_1_float} / {num_2_float} =",num_1_float / num_2_float)
    else:
        print("se chegou aqui vc é burro e um pau no cu ")
    print(" ")
    sair = input("Quer sair? [s/n] ").lower().startswith('s')

    if sair is True:
        print("saindo")
        break