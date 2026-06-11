class hamming:

    @staticmethod
    def validar_entrada_binaria(entrada):
        if not entrada:
            raise ValueError("A entrada nao pode ser vazia.")

        if any(bit not in "01" for bit in entrada):
            raise ValueError("A entrada precisa conter apenas 0 e 1.")


    @staticmethod
    def eh_posicao_paridade(posicao):
        return posicao > 0 and (posicao & (posicao - 1)) == 0


    @classmethod
    def encode(cls, entrada):
        """
        Recebe uma string binária.

        Exemplo:
        "1011"

        Deve:
        1. Separar os bits de dados.
        2. Calcular quantos bits de paridade são necessários.
        3. Inserir os bits de paridade nas posições:
           1, 2, 4, 8, 16...
        4. Calcular o valor de cada bit de paridade.
        5. Retornar a mensagem codificada.
        """

        cls.validar_entrada_binaria(entrada)

        qtd_paridade = cls.calcular_bits_paridade(len(entrada))
        palavra = cls.inserir_posicoes_paridade(entrada, qtd_paridade)

        return cls.gerar_paridades(palavra)


    @staticmethod
    def calcular_bits_paridade(tamanho_dados):
        """
        Recebe a quantidade de bits de dados.

        Deve:
        1. Descobrir quantos bits de paridade serão necessários.
        2. Utilizar a condição:

           2^r >= m + r + 1

           onde:
           m = bits de dados
           r = bits de paridade

        3. Retornar a quantidade de bits de paridade.
        """

        qtd_paridade = 0

        while (2 ** qtd_paridade) < tamanho_dados + qtd_paridade + 1:
            qtd_paridade += 1

        return qtd_paridade


    @classmethod
    def inserir_posicoes_paridade(cls, entrada, qtd_paridade):
        """
        Recebe:
        - entrada
        - quantidade de bits de paridade

        Deve:
        1. Criar uma nova palavra.
        2. Colocar bits de paridade (temporariamente 0)
           nas posições:
           1, 2, 4, 8, 16...

        3. Inserir os bits de dados nas demais posições.

        Exemplo:

        Entrada:
        1011

        Resultado temporário:
        P P 1 P 0 1 1

        Retornar a palavra montada.
        """

        tamanho_total = len(entrada) + qtd_paridade
        palavra = []
        indice_dados = 0

        for posicao in range(1, tamanho_total + 1):
            if cls.eh_posicao_paridade(posicao):
                palavra.append("0")
            else:
                palavra.append(entrada[indice_dados])
                indice_dados += 1

        return "".join(palavra)


    @classmethod
    def gerar_paridades(cls, palavra):
        """
        Recebe a palavra contendo os bits de paridade.

        Deve:
        1. Calcular cada bit de paridade.
        2. Utilizar XOR para descobrir a paridade.
        3. Atualizar os bits P da palavra.

        Exemplo:

        Posição 1 verifica:
        1,3,5,7...

        Posição 2 verifica:
        2,3,6,7...

        Posição 4 verifica:
        4,5,6,7...

        Retornar a palavra completa.
        """

        bits = list(palavra)
        tamanho = len(bits)
        posicao_paridade = 1

        while posicao_paridade <= tamanho:
            paridade = 0

            for posicao in range(1, tamanho + 1):
                if posicao & posicao_paridade:
                    paridade ^= int(bits[posicao - 1])

            bits[posicao_paridade - 1] = str(paridade)
            posicao_paridade *= 2

        return "".join(bits)


    @staticmethod
    def verificar_erro(entrada):
        """
        Recebe uma palavra codificada.

        Deve:
        1. Recalcular todas as paridades.
        2. Verificar quais paridades falharam.
        3. Montar a síndrome de erro.
        4. Retornar:

           0  -> sem erro

           ou

           posição do erro.
        """

        hamming.validar_entrada_binaria(entrada)

        posicao_erro = 0
        tamanho = len(entrada)
        posicao_paridade = 1

        while posicao_paridade <= tamanho:
            paridade = 0

            for posicao in range(1, tamanho + 1):
                if posicao & posicao_paridade:
                    paridade ^= int(entrada[posicao - 1])

            if paridade != 0:
                posicao_erro += posicao_paridade

            posicao_paridade *= 2

        return posicao_erro


    @staticmethod
    def corrigir_erro(entrada, posicao):
        """
        Recebe:
        - palavra recebida
        - posição do erro

        Deve:
        1. Inverter o bit da posição informada.
        2. Retornar a palavra corrigida.
        """

        if posicao < 1 or posicao > len(entrada):
            raise ValueError("Posicao de erro invalida.")

        bits = list(entrada)
        indice = posicao - 1
        bits[indice] = "0" if bits[indice] == "1" else "1"

        return "".join(bits)


    @classmethod
    def remover_bits_paridade(cls, entrada):
        """
        Recebe uma palavra Hamming válida.

        Deve:
        1. Remover posições:
           1,2,4,8,16...

        2. Manter apenas os bits de dados.

        Exemplo:

        0110011

        ↓

        1011

        Retornar apenas os dados.
        """

        dados = []

        for posicao, bit in enumerate(entrada, start=1):
            if not cls.eh_posicao_paridade(posicao):
                dados.append(bit)

        return "".join(dados)


    @classmethod
    def decode(cls, entrada):
        """
        Recebe uma palavra Hamming.

        Fluxo:

        1. Verificar erro.
        2. Se houver erro:
              corrigir.
        3. Remover bits de paridade.
        4. Retornar os dados originais.

        Também pode exibir:

        'Erro encontrado na posição X'

        'Mensagem corrigida'

        Retornar os bits recuperados.
        """

        cls.validar_entrada_binaria(entrada)

        posicao_erro = cls.verificar_erro(entrada)
        palavra_corrigida = entrada

        if posicao_erro:
            palavra_corrigida = cls.corrigir_erro(entrada, posicao_erro)

        return cls.remover_bits_paridade(palavra_corrigida)
