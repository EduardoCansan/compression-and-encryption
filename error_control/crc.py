from operator import xor

class crc_generator:
    gerador_crc = "10011" #valor setado pela descricao do trabalho
    
    #Funcao que faz o calculo usando o XOR
    def funcao_xor(self, entrada, gerador_crc):
        resultado_xor = ""
        
        #LOOP que faz o xor nos bits de mesma posicao da entrada e do gerador
        for i in range(len(entrada)):
            if i < len(gerador_crc):
                # int() converte o caractere em número para a função xor funcionar
                bit_calculado = xor(int(entrada[i]), int(gerador_crc[i]))
                # str() transforma o número de volta em texto para juntar na string
                resultado_xor += str(bit_calculado)
            
        return resultado_xor

    #Funcao que faz o resto da logica de divisão do CRC
    def divisao_crc(self, entrada):

        # Pega o primeiro bloco de bits com base no tamanho do gerador
        bloco_atual = entrada[:len(self.gerador_crc)]

        # Marca qual será o próximo bit da entrada a ser acrescentado
        i_proximo_bit = len(self.gerador_crc)

        # Continua enquanto ainda houver bits da entrada para processar
        while i_proximo_bit < len(entrada):

            # Se o primeiro bit do bloco for 1, faz XOR com o gerador
            if bloco_atual[0] == str("1"):
                resultado = self.funcao_xor(bloco_atual, self.gerador_crc)
            # Se o primeiro bit for 0, apenas remove esse bit inicial
            else:
                resultado = bloco_atual[1:]

            # Remove zeros à esquerda para manter o resto o mais compacto possível
            while len(resultado) > 1 and resultado[0] == str("0"):
                resultado = resultado[1:]

            # Completa o bloco com novos bits da entrada até atingir o tamanho do gerador
            while (len(resultado) < len(self.gerador_crc) and i_proximo_bit < len(entrada)):
                resultado = resultado + entrada[i_proximo_bit]
                i_proximo_bit += 1

            # O bloco atual vira o resultado obtido nesta etapa
            bloco_atual = resultado

        # Se o último bloco ainda tiver o tamanho completo do gerador, faz uma última divisão
        if len(bloco_atual) == len(self.gerador_crc):
            resultado = self.funcao_xor(bloco_atual, self.gerador_crc)

            # Remove zeros à esquerda do resto final
            while len(resultado) > 1 and resultado[0] == str("0"):
                resultado = resultado[1:]

            bloco_atual = resultado

        # Retorna o resto da divisão, que é o CRC parcial/final
        return bloco_atual

    def calcular_crc(self, entrada):
        # Calcula quantos bits "0" precisam ser adicionados ao final
        bits_reservados = len(self.gerador_crc) - 1
        # Acrescenta esses 0s para preparar a mensagem antes da divisao
        crc_com_bits = entrada + ("0" * bits_reservados)

        # Faz a divisão CRC para obter o resto
        crc = self.divisao_crc(crc_com_bits)

        # Garante que o CRC tenha o tamanho esperado, completando com zeros à esquerda se necessário
        while len(crc) < len(self.gerador_crc) - 1:
            crc = "0" + crc

        # Mantém somente os últimos bits para garantir o tamanho esperado do CRC
        crc = crc[-(len(self.gerador_crc) - 1):]

        # Retorna apenas o valor do CRC calculado
        return crc

    def gerar_mensagem_crc(self, entrada):
        # Calcula o CRC da entrada original
        crc = self.calcular_crc(entrada)
        # Junta a mensagem original com o CRC no final
        resultado_mensagem = entrada + crc
        # Retorna a mensagem completa
        return resultado_mensagem

    def verificar_crc(self, entrada):
        # Roda a divisão CRC sobre a mensagem recebida
        resultado = self.divisao_crc(entrada)

        # Se o resto for vazio ou só tiver zeros, a mensagem é considerada válida
        if len(resultado) == 0 or set(resultado) == {"0"}:
            print("CRC VALIDO")
        else:
            # Caso contrário, houve erro na transmissão ou no conteúdo
            print("ERRO DETECTADO")
            print("Resto:", resultado)

        # Retorna o resto final da verificação
        return resultado


# criado instacia da classe 101100
meu_crc = crc_generator()

crc = meu_crc.calcular_crc("101100")
print("CRC FINAL:", crc)

msg = meu_crc.gerar_mensagem_crc("101100")
print("mensagem crc:", msg)

verificacao = meu_crc.verificar_crc("101100")



#==================== COMPATIBILIDADE ================

#compatível com os algoritmos de compressão:

# bits = golomb.encode("ABC")

# crc = crc_generator()

# mensagem = crc.gerar_mensagem_crc(bits)

# Ou:

# bits = huffman.encode("ABC")

# mensagem = crc.gerar_mensagem_crc(bits)