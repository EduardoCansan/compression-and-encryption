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

    # # 1. Criamos a instância da classe
    # meu_gerador = crc_generator()
    # # 2. Chamamos a função passando os dados e usando os parênteses ()
    # resultado_final = meu_gerador.calcular_crc(meu_gerador.entrada, meu_gerador.gerador_crc)
    # print("Resultado do XOR:", resultado_final)

    def calcular_crc(self, ):
        bits_reservados = len(self.gerador_crc) - 1
        crc_com_bits = self.entrada + ("0" * bits_reservados)
        #Entrada + 0s:  1011000000
        
        # print("Entrada + 0s: ", crc_com_bits)
        
        #10110
        bloco_atual = crc_com_bits[:len(self.gerador_crc)]
        
        #0
        i_proximo_bit = len(self.gerador_crc)
        
        # print(bloco_atual)
        # print(i_proximo_bit)
        
        while i_proximo_bit < len(crc_com_bits):
            if bloco_atual[0] == str("1"):
                resultado = self.funcao_xor(bloco_atual, self.gerador_crc)
            else:
                resultado = bloco_atual
            
            while resultado[0] == str("0"): #! VERIFICAR, PODE QUEBRAR SE FOR SÓ 0s, 00000
                resultado = resultado[1:]
            
            while len(resultado) < len(self.gerador_crc):
                resultado = resultado + crc_com_bits[i_proximo_bit]
                i_proximo_bit += 1
            
            bloco_atual = resultado
            
            # print("Bloco:", bloco_atual)
            # print("Indice:", i_proximo_bit)
            
        if len(bloco_atual) == len(self.gerador_crc):
            resultado = self.funcao_xor(bloco_atual, self.gerador_crc)
            while resultado[0] == str("0"): #! VERIFICAR, PODE QUEBRAR SE FOR SÓ 0s, 00000
                resultado = resultado[1:]
            bloco_atual = resultado
            # print("bloco final: ", bloco_atual)
        else: 
            return bloco_atual
            
        return bloco_atual

    def gerar_mensagem_crc(self):
        crc = self.calcular_crc()
        resultado_mensagem = self.entrada + crc
        return resultado_mensagem
    
    # def verificar_crc(self):
    #     entrada_verf = self.gerar_mensagem_crc()
        
        
#criado instacia da classe
meu_crc = crc_generator()
#chama funcao
crc = meu_crc.calcular_crc()
print("CRC FINAL: ", crc)

msg = meu_crc.gerar_mensagem_crc()
print("mensagem crc: ", msg)