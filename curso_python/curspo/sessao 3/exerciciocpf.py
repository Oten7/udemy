# """
# Calculo do primeiro dígito do CPF
# CPF: 746.824.890-70
# Colete a soma dos 9 primeiros dígitos do CPF
# multiplicando cada um dos valores por uma
# contagem regressiva começando de 10

# Ex.:  746.824.890-70 (746824890)
#    10  9  8  7  6  5  4  3  2
# *  7   4  6  8  2  4  8  9  0
#    70  36 48 56 12 20 32 27 0

# Somar todos os resultados: 
# 70+36+48+56+12+20+32+27+0 = 301
# Multiplicar o resultado anterior por 10
# 301 * 10 = 3010
# Obter o resto da divisão da conta anterior por 11
# 3010 % 11 = 7
# Se o resultado anterior for maior que 9:
#     resultado é 0
# contrário disso:
#     resultado é o valor da conta

# O primeiro dígito do CPF é 7
# """
import re
import sys
# cpf_enviado_usuario = '746.824.890-70'  \
#     .replace('.', '') \
#     .replace('-', '') \
#     .replace(' ', '')
entrada = input('Digite o CPF (apenas números): ')
cpf_enviado_usuario = re.sub(
    r'[^0-9]', 
    '',
    entrada
)
entrada_e_sequencial = entrada == entrada[0] * len(entrada)
if entrada_e_sequencial:
    print('Você enviou dados sequenciais. Isso não é um CPF válido.')
    sys.exit()  
nove_digitos = cpf_enviado_usuario[:9]
contador_regressivo = 10

resultado_digito_1 = 0

for digito in nove_digitos:
    resultado_digito_1 += int(digito) * contador_regressivo
    contador_regressivo -= 1
p_digito = ((resultado_digito_1 * 10) % 11)
p_digito = p_digito if p_digito <= 9 else 0

dez_digitos = nove_digitos + str(p_digito)
contador_regressivo_2 = 11
resultado_digito_2 = 0

for digito in dez_digitos:
    resultado_digito_2 += int(digito) * contador_regressivo_2
    contador_regressivo_2 -= 1

s_digito = ((resultado_digito_2 * 10) % 11)
s_digito = s_digito if s_digito <= 9 else 0

cpf_gerado_pelo_calculo = f'{nove_digitos}{p_digito}{s_digito}'
if cpf_enviado_usuario == cpf_gerado_pelo_calculo:
    print(f'CPF válido: {cpf_gerado_pelo_calculo}')
else:
    print(f'CPF inválido: {cpf_gerado_pelo_calculo}')
