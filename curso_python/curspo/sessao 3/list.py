# string = 'ABCDE'
#
#
#
# lista = [123, True, 'Neto', 1.2, []]
# print(lista)

# lista = [10, 20, 30, 40 ]
# # del lista[2]
# # print(lista)
# lista.append(50)
# print(lista)
# lista_a = [1, 2, 3,]
# lista_b = [4, 5, 6]
# lista_c = lista_a + lista_b
# lista_a.extend(lista_b)
# print(lista_c)


# ------------------------------

# lista = ["jose", "pedro", "maria"]
# indice = range(len(lista))
    
# for indice in indice:
#     print(indice, lista[indice],type(lista[indice]))

#================================


"""
Lista de listas e seus índices
"""
salas = [
    # 0        1
    ['Maria', 'Helena', ],  # 0
    # 0
    ['Elaine', ],  # 1
    # 0       1       2
    ['Luiz', 'João', 'Eduarda', ],  # 2
]

# print(salas[1][0])
# print(salas[0][1])
# print(salas[2][2])
# print(salas[2][3][3])

for sala in salas:
    print(f'A sala é {sala}')
    for aluno in sala:
        print(aluno)