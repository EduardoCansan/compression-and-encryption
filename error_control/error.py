import random
class error_simulator:

    #apenas um caracter 
    def inverter_bit(self, entrada, posicao):
        if len(entrada) < posicao :
            return "Error: Posicao escolhida é maior que a quantidade de caracteres da entrada!"
        else:
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
        if len(entrada) < quantidade :
            return "Error: Quantidade de posicoes escolhida, maior que a quantidade de caracteres da entrada"
        else:
            #quantidade = num d posicoes mudadas
            posicoes = random.sample(range(len(entrada)), quantidade)
            
            lista_entrada = list(entrada)
            
            for i in posicoes:
                if lista_entrada[i] == "1":
                    lista_entrada[i] = "0"
                else:
                    lista_entrada[i] = "1"
            
            nova_msg = "".join(lista_entrada)
            
            saida = print(f"posicoes invertidas: {posicoes}", f"\n mensagem original:  {entrada}", f"\n mensagem modificada: {nova_msg}")
            
            return saida

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


error = error_simulator()

inverter = error.inverter_bit("10101101", 2)
print(inverter)

aleatorio = error.inserir_erros_aleatorios("10101101", 2)
print(aleatorio)