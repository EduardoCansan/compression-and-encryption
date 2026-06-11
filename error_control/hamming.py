class hamming:

    def encode(self, entrada):
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

        pass


    def calcular_bits_paridade(self, tamanho_dados):
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

        pass


    def inserir_posicoes_paridade(self, entrada, qtd_paridade):
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

        pass


    def gerar_paridades(self, palavra):
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

        pass


    def verificar_erro(self, entrada):
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

        pass


    def corrigir_erro(self, entrada, posicao):
        """
        Recebe:
        - palavra recebida
        - posição do erro

        Deve:
        1. Inverter o bit da posição informada.
        2. Retornar a palavra corrigida.
        """

        pass


    def remover_bits_paridade(self, entrada):
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

        pass


    def decode(self, entrada):
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

        pass