import math

class Golomb:
    @staticmethod
    def _text_to_decimals(text: str) -> list[int]:
        return [ord(char) for char in text]

    @classmethod
    def encode(cls, symbol_str: str, k : int) -> str:
        #! CODIFICACAO

        if k < 1 or (k & (k - 1)) != 0:
            raise ValueError("K precisa ser potencia de 2")

        decimal_text = cls._text_to_decimals(symbol_str)
        encodes = []

        for entrada_simbolo in decimal_text:
            if entrada_simbolo < 0:
                raise ValueError("invalid input.")

            #* dividindo o simbolo pelo divisor K
            #* quociente = numero de zeros no prefixo
            quociente = entrada_simbolo // k
            #* resto = valor que vira o sufixo
            resto = entrada_simbolo % k

            #* Prefixo (unario) - + '1' = Stopbit
            unario = '0' * quociente + '1'

            #* quantidade de bits do sufixo = log2(K)
            num_bits = int(math.log2(k))

            #* sufixo = resto convertido para binario com num_bits digitos
            sufixo = format(resto, f'0{num_bits}b')

            encodes.append(unario + sufixo)

        return ''.join(encodes)

    #* divide a string binária em codewords individuais
    #* para o decode funcionar corretamente
    @staticmethod
    def split_codewords(bits: str, k: int) -> list[str]:
        num_bits = int(math.log2(k))
        codewords = []
        i = 0
        
        while i < len(bits):
            # Encontra o stopbit '1'
            j = i
            while j < len(bits) and bits[j] == '0':
                j += 1
            
            if j < len(bits):  # Encontrou o stopbit
                # codeword = prefixo (0's + stopbit 1) + sufixo (num_bits)
                codeword = bits[i:j+1+num_bits]
                codewords.append(codeword)
                i = j + 1 + num_bits
            else:
                break
        
        return codewords

    @classmethod
    def decode(cls, codeword_str: str, k : int) -> str:
        #! DECODIFICACAO

        if k < 1 or (k & (k - 1)) != 0:
            raise ValueError("K precisa ser potencia de 2")

        #* Inputs: bits
        caracteres_permitidos = set("01")
        valido = all(c in caracteres_permitidos for c in codeword_str)
        if not valido:
            raise ValueError("invalid input.")

        codewords = cls.split_codewords(codeword_str, k)
        chars = []

        for entrada_codeword in codewords:
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
            Num = q * k + R

            chars.append(chr(Num))

        return ''.join(chars)
