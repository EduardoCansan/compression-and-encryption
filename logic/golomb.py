import math

class Golomb:

    @classmethod
    def encode(cls, symbol_str: str) -> str:
        #! CODIFICACAO

        #* K perguntado uma vez, antes do loop
        while True:
            entrada_divisor = int(input("enter the divisor (K) - powers of 2 only: "))
            if entrada_divisor >= 1 and (entrada_divisor & (entrada_divisor - 1)) == 0: #somentes numeros em potencia de 2
                break
            print("invalid input.")

        while True:
            #* Inputs: simbolo
            entrada_simbolo = int(symbol_str)
            if entrada_simbolo < 0:
                raise ValueError("invalid input.")

            #* dividindo o simbolo pelo divisor K
            #* quociente = numero de zeros no prefixo
            quociente = entrada_simbolo // entrada_divisor
            #* resto = valor que vira o sufixo
            resto = entrada_simbolo % entrada_divisor

            #* Prefixo (unario) - + '1' = Stopbit
            unario = '0' * quociente + '1'

            #* quantidade de bits do sufixo = log2(K)
            num_bits = int(math.log2(entrada_divisor))

            #* sufixo = resto convertido para binario com num_bits digitos
            sufixo = format(resto, f'0{num_bits}b')

            print(unario + sufixo)

            continuar = input("do you want to encode another symbol? (y/n): ")
            if continuar.lower() != 'y':
                break
            symbol_str = input("symbol: ")

    @classmethod
    def decode(cls, codeword_str: str) -> str:
        #! DECODIFICACAO

        #* K perguntado uma vez, antes do loop
        while True:
            entrada_divisor_decode = int(input("enter the divisor (K) - powers of 2 only: "))
            if entrada_divisor_decode >= 1 and (entrada_divisor_decode & (entrada_divisor_decode - 1)) == 0: #somentes numeros em potencia de 2
                break
            print("invalid input.")

        while True:
            #* Inputs: bits
            entrada_codeword = codeword_str
            caracteres_permitidos = set("01")
            valido = all(c in caracteres_permitidos for c in entrada_codeword)
            if not valido:
                raise ValueError("invalid input.")

            #* decodificar o prefixo (unario)
            #* q = contador = stopbit
            q = 0
            for i in entrada_codeword:
                if i == '0':
                    q += 1
                else:
                    break

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

            continuar = input("do you want to decode another codeword? (y/n): ")
            if continuar.lower() != 'y':
                break
            codeword_str = input("codeword: ")