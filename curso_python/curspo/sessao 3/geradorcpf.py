import random

for _ in range(100):
    nove_digitos = ''
    for i in range(9):
        nove_digitos += str(random.randint(0, 9))


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
    print(cpf_gerado_pelo_calculo)
