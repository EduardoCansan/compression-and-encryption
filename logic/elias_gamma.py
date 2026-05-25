import math

class EliasGamma:
    @staticmethod
    def _text_to_decimals(text: str) -> list[int]:
        return [ord(char) for char in text]

    @classmethod
    def encode(cls, symbol_str: str) -> str:
        #! CODIFICACAO
        decimal_text = cls._text_to_decimals(symbol_str)
        encodes = []

        for entrada_simbolo in decimal_text:
            if entrada_simbolo <= 0:
                raise ValueError("invalid input.")
            #* k = floor(log2(N)) — numero de bits necessario menos 1
            k = int(math.log2(entrada_simbolo))
            #* Prefixo (unario) - k zeros + '1' = Stopbit
            unario = '0' * k + '1'
            #* sufixo = N em binario com k bits, sem o bit mais significativo
            sufixo = format(entrada_simbolo, f'0{k+1}b')[1:]
            encodes.append(unario + sufixo)

        return ''.join(encodes)

    #* divide a string binária em codewords individuais
    #* para o decode funcionar corretamente
    @staticmethod
    def split_codewords(bits: str) -> list[str]:
        codewords = []
        i = 0
        
        while i < len(bits):
            # Encontra o stopbit '1'
            j = i
            while j < len(bits) and bits[j] == '0':
                j += 1
            
            if j < len(bits):  # Encontrou o stopbit
                k = j - i  # Número de zeros (tamanho do sufixo)
                # codeword = prefixo (0's + stopbit 1) + sufixo (k bits)
                codeword = bits[i:j+1+k]
                codewords.append(codeword)
                i = j + 1 + k
            else:
                break
        
        return codewords

    @classmethod
    def decode(cls, codeword_str: str) -> str:
        #! DECODIFICACAO
        #* Inputs: bits
        caracteres_permitidos = set("01")
        valido = all(c in caracteres_permitidos for c in codeword_str)
        if not valido:
            raise ValueError("invalid input.")

        codewords = cls.split_codewords(codeword_str)
        chars = []

        for entrada_codeword in codewords:
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
            chars.append(chr(N))

        return ''.join(chars)
