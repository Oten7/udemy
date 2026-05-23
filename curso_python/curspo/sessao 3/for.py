# texto = 'Python'
#
#
# novo_texto = ''
# for letra in texto:
#     novo_texto += f'*{letra}'
#     print(letra)
# print(novo_texto + '*')
#------------------------------
# numeros =  range(1, 11)
#
# for numero in numeros:
#     print(numero)
#-------------------------------
# texto =  'Neto'
# interador =  iter(texto)
#
# while True:
#     try:
#         print(next(interador))
#     except StopIteration:
#         break

# for letra in texto:
#     print(letra)
#------------------------------------

# for i in range(10):
#     if i == 2:
#         print('i é 2, pulando...')
#         continue
#
#     if i == 8:
#         print('i é 8, o else nao executara')
#         break
#
#     for j in range(1, 3):
#         print(i,j)
#
# else:
#     print('for commpleto com sucesso')

valor = 904
contador = 0

for i in range(valor):
    if i % 3 == 0:
        contador += 1

print(contador)