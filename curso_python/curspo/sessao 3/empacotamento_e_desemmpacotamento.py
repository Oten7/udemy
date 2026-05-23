# _,nome1, *_ = ["jose", "pedro", "maria"]
# print(nome1)
# ===================================

# nomes =[ 'Neto', 'Maria', 'Pedro']
# # nomes = tuple(nomes)
# print(nomes[-1])
# print(nomes)
#=====================================

# lista = ["jose", "pedro", "maria"]
# lista.append("joao")

# # lista_enumerada = enumerate(lista)

# for indice, nome in enumerate(lista):
#     print(f"{indice}: {nome}")


# for item in enumerate(lista):
#     indice, nome = item
#     print(f"{indice}: {nome}")


# for tupla_enumerada in enumerate(lista):
#     print(f"For da tupla:")
#     for valor in tupla_enumerada:
#         print(f"\t{valor}")
#=====================================

#desempacotamento em chammadas

string = "ABCDE"
lista = ['Maria', 'Helena', 1, 2, 3, 'Eduarda']
tupla = 'Pythom', 'é', 'vida'


# p, b, *_, ap, u = lista 
# print(p, u, ap)

print(*lista)


