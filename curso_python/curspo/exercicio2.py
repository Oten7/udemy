#Faça um programa que pergunte a hora ao usuário e, baseando-se no horário
#descrito, exiba a saudação apropriada. Ex. 
#Bom dia 0-11, Boa tarde 12-17 e Boa noite 18-23.

horas = float(input("Digte a hora: "))

if horas <= 11:
    print(f"Bom Dia: Sao {horas:.2f}")

elif horas <= 17:
    print(f"Bom Tarde: Sao {horas:.2f}")
else:
    print(f"Bom Noite: Sao {horas:.2f}")