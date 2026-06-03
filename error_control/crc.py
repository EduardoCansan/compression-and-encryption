from operator import xor

class crc_generator:
    gerador_crc = "10011"
    
    def funcao_xor(self, entrada, gerador_crc):
        resultado_xor = ""
        
        for i in range(len(entrada)):
            if i < len(gerador_crc):
                # int() converte o caractere em número para a função xor funcionar
                bit_calculado = xor(int(entrada[i]), int(gerador_crc[i]))
                # str() transforma o número de volta em texto para juntar na string
                resultado_xor += str(bit_calculado)
            
        return resultado_xor

    def divisao_crc(self, entrada):

        bloco_atual = entrada[:len(self.gerador_crc)]

        i_proximo_bit = len(self.gerador_crc)

        while i_proximo_bit < len(entrada):

            if bloco_atual[0] == str("1"):
                resultado = self.funcao_xor(bloco_atual, self.gerador_crc)
            else:
                resultado = bloco_atual[1:]

            while len(resultado) > 1 and resultado[0] == str("0"):
                resultado = resultado[1:]

            while (len(resultado) < len(self.gerador_crc) and i_proximo_bit < len(entrada)):
                resultado = resultado + entrada[i_proximo_bit]
                i_proximo_bit += 1

            bloco_atual = resultado

        if len(bloco_atual) == len(self.gerador_crc):
            resultado = self.funcao_xor(bloco_atual, self.gerador_crc)

            while len(resultado) > 1 and resultado[0] == str("0"):
                resultado = resultado[1:]

            bloco_atual = resultado

        return bloco_atual

    def calcular_crc(self, entrada):
        bits_reservados = len(self.gerador_crc) - 1
        crc_com_bits = entrada + ("0" * bits_reservados)

        crc = self.divisao_crc(crc_com_bits)

        while len(crc) < len(self.gerador_crc) - 1:
            crc = "0" + crc

        return crc

    def gerar_mensagem_crc(self, entrada):
        crc = self.calcular_crc(entrada)
        resultado_mensagem = entrada + crc
        return resultado_mensagem

    def verificar_crc(self, entrada):
        entrada_verf = self.gerar_mensagem_crc(entrada)

        resultado = self.divisao_crc(entrada_verf)

        if len(resultado) == 0 or set(resultado) == {"0"}:
            print("CRC VALIDO")
        else:
            print("ERRO DETECTADO")
            print("Resto:", resultado)

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