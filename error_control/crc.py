from operator import xor

class crc_generator:
    # Entrada fixa para testar
    entrada = "101100" 
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
                resultado = bloco_atual

            while len(resultado) > 0 and resultado[0] == str("0"):  #! VERIFICAR, PODE QUEBRAR SE FOR SÓ 0s, 00000
                resultado = resultado[1:]

            while len(resultado) < len(self.gerador_crc):
                resultado = resultado + entrada[i_proximo_bit]
                i_proximo_bit += 1

            bloco_atual = resultado

        if len(bloco_atual) == len(self.gerador_crc):
            resultado = self.funcao_xor(bloco_atual, self.gerador_crc)

            while len(resultado) > 0 and resultado[0] == str("0"):  #! VERIFICAR, PODE QUEBRAR SE FOR SÓ 0s, 00000
                resultado = resultado[1:]

            bloco_atual = resultado
        else:
            return bloco_atual

        return bloco_atual

    def calcular_crc(self):
        bits_reservados = len(self.gerador_crc) - 1
        crc_com_bits = self.entrada + ("0" * bits_reservados)

        return self.divisao_crc(crc_com_bits)

    def gerar_mensagem_crc(self):
        crc = self.calcular_crc()
        resultado_mensagem = self.entrada + crc
        return resultado_mensagem

    def verificar_crc(self):
        entrada_verf = self.gerar_mensagem_crc()

        resultado = self.divisao_crc(entrada_verf)

        if resultado == "":
            print("CRC VALIDO")
        else:
            print("ERRO DETECTADO")
            print("Resto:", resultado)

        return resultado


# criado instacia da classe
meu_crc = crc_generator()

crc = meu_crc.calcular_crc()
print("CRC FINAL:", crc)

msg = meu_crc.gerar_mensagem_crc()
print("mensagem crc:", msg)

verificacao = meu_crc.verificar_crc()