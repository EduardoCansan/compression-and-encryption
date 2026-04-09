import math

class EliasGamma:
    @classmethod
    def encode(cls, symbol_str: str) -> str:
        #! CODIFICACAO
        while True:
            #* Inputs: simbolo
            entrada_simbolo = int(symbol_str)
            if entrada_simbolo <= 0:
                raise ValueError("invalid input.")
            #* k = floor(log2(N)) — numero de bits necessario menos 1
            k = int(math.log2(entrada_simbolo))
            #* Prefixo (unario) - k zeros + '1' = Stopbit
            unario = '0' * k + '1'
            #* sufixo = N em binario com k bits, sem o bit mais significativo
            sufixo = format(entrada_simbolo, f'0{k+1}b')[1:]
            print(unario + sufixo)
            continuar = input("do you want to encode another symbol? (y/n): ")
            if continuar.lower() != 'y':
                break
            symbol_str = input("symbol: ")

    @classmethod
    def decode(cls, codeword_str: str) -> str:
        #! DECODIFICACAO
        while True:
            #* Inputs: bits
            entrada_codeword = codeword_str
            caracteres_permitidos = set("01")
            valido = all(c in caracteres_permitidos for c in entrada_codeword)
            if not valido:
                raise ValueError("invalid input.")
            #* decodificar o prefixo (unario)
            #* k = contador de zeros ate o stopbit
            k = 0
            for i in entrada_codeword:
                if i == '0':
                    k += 1
                else:
                    break
            #* sufixo = k bits apos o stopbit
            sufixo = entrada_codeword[k+1:k+1+k]
            #* reconstruindo o numero original
            #* 2^k = bit mais significativo que foi removido no encode
            #* int(sufixo, 2) = valor do sufixo em decimal
            N = 2**k + (int(sufixo, 2) if sufixo else 0)
            print(N)
            continuar = input("do you want to decode another codeword? (y/n): ")
            if continuar.lower() != 'y':
                break
            codeword_str = input("codeword: ")