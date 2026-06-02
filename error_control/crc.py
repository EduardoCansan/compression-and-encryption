from operator import xor

class crc_generator:
    # Entrada fixa para testar
    entrada = "101100"
    gerador_crc = "10011"
    
    bits_reservados = len(gerador_crc) - 1
    crc_com_bits = entrada + ("0" * bits_reservados)
    
    print("CRC com bits:", crc_com_bits)
    
    def calcular_crc(self, entrada, gerador_crc):
        resultado_xor = ""
        
        for i in range(len(entrada)):
            if i < len(gerador_crc):
                # int() converte o caractere em número para a função xor funcionar
                bit_calculado = xor(int(entrada[i]), int(gerador_crc[i]))
                # str() transforma o número de volta em texto para juntar na string
                resultado_xor += str(bit_calculado)
            
        return resultado_xor

# 1. Criamos a instância da classe
meu_gerador = crc_generator()
# 2. Chamamos a função passando os dados e usando os parênteses ()
resultado_final = meu_gerador.calcular_crc(meu_gerador.entrada, meu_gerador.gerador_crc)
print("Resultado do XOR:", resultado_final)