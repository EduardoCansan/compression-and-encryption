#Error_Simulator

import random
class error_simulator:

    # inverte apenas um bit da mensagem
    # entrada: sequência de bits
    # posicao: posição que será alterada
    def inverter_bit(self, entrada, posicao):
        # verifica se a posição informada existe na mensagem
        if len(entrada) <= posicao:
            return "Error: Posicao escolhida é maior que a quantidade de caracteres da entrada!"
        else:
            # Guarda o bit da posição escolhida
            caracter = entrada[posicao]
            # Inverte o bit - 1 vira 0 e 0 vira 1
            if caracter == "1":
                caracter = "0"
            else:
                caracter = "1"

            # pega a parte da mensagem antes do bit alterado
            palavra_antes = entrada[:posicao]
            # pega a parte da mensagem depois do bit alterado
            palavra_depois = entrada[posicao + 1:]
            
            # monta novamente a mensagem com o bit invertido
            palavra_final = palavra_antes + caracter + palavra_depois

            # retorna a nova mensagem e a posição alterada
            return palavra_final, posicao

    # insere erros em posições aleatórias da mensagem
    #entrada: sequência de bits
    #quantidade: número de bits que serão alterados
    def inserir_erros_aleatorios(self, entrada, quantidade):
        # verifica se a quantidade de erros é maior que a mensagem
        if len(entrada) < quantidade:
            return "Error: Quantidade de posicoes escolhida, maior que a quantidade de caracteres da entrada"
        else:
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


# ============= TESTES =============
# error = error_simulator()

# palavra_final, posicao = error.inverter_bit("10101101", 2)
# print(palavra_final, posicao)

# nova_msg, posicoes = error.inserir_erros_aleatorios("10101101", 2)
# print(nova_msg, posicoes)