class hamming:
    #Usando o hamming assim como ensinado em sala de aula:
    # Hamming(7,4) - 4 bits de dados + 3 bits de paridade
    # Posicoes: 1 2 3 4 5 6 7
    # P P D P D D D
    TAMANHO_DADOS = 4
    TAMANHO_CODEWORD = 7
    
    # Valida a entrada
    @staticmethod
    def validar_entrada_binaria(entrada):
        # Se é vazia
        if not entrada:
            raise ValueError("The entrance cannot be empty.")

        # Se tem caracteres diferentes de 0 e 1
        if any(bit not in "01" for bit in entrada):
            raise ValueError("The input must contain only 0 and 1.")

    # Metodo para calcular o XOR de uma lista de bits (0 e 1)
    @staticmethod
    def xor_bits(bits):
        resultado = 0

        for bit in bits:
            resultado ^= int(bit)

        return str(resultado)

    # Separacao dos blocos, faz a separacao da string de entrada em blocos de tamanho definido
    # Assim conseguimos processar cada bloco de dados e gerar a codeword correspondente
    @staticmethod
    def separar_blocos(entrada, tamanho_bloco):
        return [
            entrada[i:i + tamanho_bloco]
            for i in range(0, len(entrada), tamanho_bloco)
        ]


    @classmethod
    def encode(cls, entrada):
        cls.validar_entrada_binaria(entrada)

        # Aqui é a lógica aplicada ao problema que estavamos tendo
        # Não pegava a string completa, apenas os blocos completos de 4 bits
        # O que fizemos for adicionar o resto da string (se tiver) ao final do resultado, sem passar pelo processo de codificação
        # Assim nao fica sobrando e dando erro, e os blocos de 4 bits são processados normalmente, gerando as codewords de 7 bits
        codewords = []
        tamanho_completo = len(entrada) - (len(entrada) % cls.TAMANHO_DADOS)
        blocos_completos = entrada[:tamanho_completo]
        resto = entrada[tamanho_completo:]

        # Cria as codewords para cada bloco de dados
        for bloco in cls.separar_blocos(blocos_completos, cls.TAMANHO_DADOS):
            codewords.append(cls.encode_bloco(bloco))

        return "".join(codewords) + resto


    @classmethod
    def encode_bloco(cls, bloco):
        if len(bloco) != cls.TAMANHO_DADOS:
            raise ValueError("Hamming block must have exactly 4 bits.")

        # Lógica para calcular os bits de paridade P1, P2 e P4 com base nos bits de dados D1, D2, D3 e D4
        d1, d2, d3, d4 = bloco

        p1 = cls.xor_bits([d1, d2, d4])
        p2 = cls.xor_bits([d1, d3, d4])
        p4 = cls.xor_bits([d2, d3, d4])

        return p1 + p2 + d1 + p4 + d2 + d3 + d4


    @classmethod
    def verificar_erro(cls, entrada):
        # Recalcula as paridades de uma codeword Hamming(7,4).
        # Retorna 0 quando nao existe erro ou a posicao 1..7 do bit errado.
        cls.validar_entrada_binaria(entrada)

        if len(entrada) != cls.TAMANHO_CODEWORD:
            raise ValueError("Hamming codeword must have exactly 7 bits.")

        s1 = int(cls.xor_bits([entrada[0], entrada[2], entrada[4], entrada[6]]))
        s2 = int(cls.xor_bits([entrada[1], entrada[2], entrada[5], entrada[6]]))
        s4 = int(cls.xor_bits([entrada[3], entrada[4], entrada[5], entrada[6]]))

        return s1 + (s2 * 2) + (s4 * 4)


    @classmethod
    def corrigir_erro(cls, entrada, posicao):
        if posicao < 1 or posicao > cls.TAMANHO_CODEWORD:
            raise ValueError("Invalid error position.")

        bits = list(entrada)
        indice = posicao - 1
        bits[indice] = "0" if bits[indice] == "1" else "1"

        return "".join(bits)

    # Remove as pariedades para retornar apenas os bits de dados
    @staticmethod
    def remover_bits_paridade(entrada):
        return entrada[2] + entrada[4] + entrada[5] + entrada[6]


    @classmethod
    def decode(cls, entrada):
        # Recebe uma sequencia Hamming(7,4), corrige um erro por bloco
        # retorna apenas os bits de dados reconstruidos.

        cls.validar_entrada_binaria(entrada)
        
        # Segue a mesma lógica para o erro anterior que tinhamos no encode
        dados = []
        tamanho_completo = len(entrada) - (len(entrada) % cls.TAMANHO_CODEWORD)
        blocos_completos = entrada[:tamanho_completo]
        resto = entrada[tamanho_completo:]

        # Para cada bloco de 7 bits, verifica se existe erro, corrige se necessário e extrai os 4 bits de dados.
        for bloco in cls.separar_blocos(blocos_completos, cls.TAMANHO_CODEWORD):
            posicao_erro = cls.verificar_erro(bloco)

            if posicao_erro:
                bloco = cls.corrigir_erro(bloco, posicao_erro)

            # Devolve o hamming completo corrigido, mas só adiciona os bits de dados ao resultado final
            dados.append(cls.remover_bits_paridade(bloco))

        return "".join(dados) + resto
