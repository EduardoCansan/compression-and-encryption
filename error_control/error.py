class error_simulator:

    def inverter_bit(self, entrada, posicao):
        
        caracter = entrada[posicao]
        print("posicao: ", posicao , "bit: ", entrada[posicao])
        
        if caracter == "1":
            caracter = "0"
        else:
            caracter = "1"
        
        palavra_antes = entrada[:posicao]
        palavra_depois = entrada[posicao + 1:]

        palavra_final = palavra_antes + caracter + palavra_depois

        return palavra_final

    def inserir_erros_aleatorios(self, entrada, quantidade):
        """
        Inserção automática de erro.

        Recebe:
            bits -> mensagem binária
            quantidade -> quantidade de erros a serem inseridos

        Deve:
            - escolher posições aleatórias da mensagem
            - inverter os bits dessas posições
            - evitar repetir a mesma posição (opcional)

        Retorna:
            mensagem binária modificada
        """
        pass

    def gerar_posicoes_erro(self, tamanho, quantidade):
        """
        (Opcional)

        Recebe:
            tamanho -> tamanho total da mensagem
            quantidade -> quantidade de posições desejadas

        Deve:
            - gerar posições aleatórias válidas
            - não repetir posições

        Retorna:
            lista com as posições sorteadas

        Exemplo:
            [2, 5, 8]
        """
        pass

#classe
error = error_simulator()

inverter = error.inverter_bit("10101111", 1)
print(inverter)