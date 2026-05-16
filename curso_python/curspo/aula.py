str = 'Sebastiao Neto'


indice = 00
novo_str = ""
while indice < len(str):
    letra = str[indice]
    novo_str += f'*{letra}'
    indice += 1
print(novo_str)