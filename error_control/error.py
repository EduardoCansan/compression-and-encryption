#Error_Simulator

import random
class error_simulator:

    #seleciona os bits manualmente para inverter
    def inverter_bit(self, entrada, posicoes):
        # verifica se a posição informada existe na mensagem
        for posicao in posicoes:
            if posicao < 0 or posicao >= len(entrada):
                return "Error!"
                
        # converte a string para lista para permitir alterações
        lista_entrada = list(entrada)
        
        for posicao in posicoes:
            if lista_entrada[posicao] == "1":
                lista_entrada[posicao] = "0"
            else:
                lista_entrada[posicao] = "1"
        
        nova_msg = "".join(lista_entrada)
        return nova_msg, posicoes

    # insere erros em posições aleatórias da mensagem
    #entrada: sequência de bits
    #quantidade: número de bits que serão alterados
    def inserir_erros_aleatorios(self, entrada, quantidade):
        # verifica se a quantidade de erros é maior que a mensagem
        if len(entrada) < quantidade:
            return "Error: The number of positions chosen is greater than the number of characters in the input"

        # sorteia posições aleatórias sem repetir
        posicoes = random.sample(range(len(entrada)), quantidade)

        # converte a string para lista para permitir alterações
        lista_entrada = list(entrada)

        # percorre todas as posições sorteadas
        for i in posicoes:
            # inverte cada bit escolhido - 1 vira 0 e 0 vira 1
            if lista_entrada[i] == "1":
                lista_entrada[i] = "0"
            else:
                lista_entrada[i] = "1"

        # junta novamente todos os bits em uma string
        nova_msg = "".join(lista_entrada)
        # retorna a mensagem modificada e as posições alteradas
        return nova_msg, posicoes