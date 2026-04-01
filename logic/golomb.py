import math

#! CODIFICACAO

#* Inputs: simbolo e divisor K 

while True:
    entrada_simbolo = int(input("digite um numero positivo (simbolo): "))
    if entrada_simbolo >= 0:
        break
    print("entrada invalalida.")

while True:
    entrada_divisor = int(input("digite o divisor (K): "))
    if entrada_divisor >= 1:
        break
    print("entrada invalalida.")

#* dividindo o simbolo pelo divisor K
#* quociente = numero de zeros no prefixo
quociente = entrada_simbolo // entrada_divisor
#* resto = valor que vira o sufixo
resto = entrada_simbolo % entrada_divisor

# teste quociente e resto
# print(f"quociente: {quociente} resto: {resto}")

#* Prefixo (unario) - + '1' = Stopbit
unario = '0' * quociente + '1'

# teste unario
# print(f"unario: {unario}")

#* quantidade de bits do sufixo = log2(K)
num_bits = int(math.log2(entrada_divisor))

#* sufixo = resto convertido para binario com num_bits digitos
sufixo = format(resto, f'0{num_bits}b')

#testes
#print(num_bits, sufixo)

print(unario + sufixo)

#! DECODIFICACAO

#Testes:
#Número: 89
#K: 64
#Codeword: 01011001

#* Inputs: bits e "K"
while True:
    entrada_codeword = str(input("digite os bits: "))
    caracteres_permitidos = set("01")
    valido = all(c in caracteres_permitidos for c in entrada_codeword)
    if valido == True:
        break
    print("entrada invalalida.")

while True:
    entrada_divisor_decode = int(input("digite o divisor (K): "))
    if entrada_divisor_decode >= 1:
        break
    print("entrada invalalida.")

#* decodificar o prefixo (unario)
#* q = contador = stopbit
q = 0
for i in entrada_codeword:
    if i == '0':
        q += 1
    else:
        break

#teste printar a posicao do stopbit
#print(q)

#* decodificar o sufixo
sufixo = (entrada_codeword[q+1:])

#* transformando o sufixo str em int base 2(0,1)
R = int(sufixo, 2)

#* reconstruindo o numero original
#* q = quociente (numero de zeros no prefixo)
#* entrada_divisor_decode = K (divisor)
#* R = resto (sufixo convertido de binario para decimal)
Num = q * entrada_divisor_decode + R
print(Num)