#usado para contar o termo mais comum de cada pedaco no decode
from collections import Counter 

class repetition_ri:

    # Codifica utilizando repetição
    #entrada: sequência de bits
    #repeticao: quantidade de vezes que cada bit será repetido
    def encode(self, entrada, repeticao):
        # variavel da mensagem codificada
        msg_encode = ""
        # percorre todos os bits da entrada
        for i in range(len(entrada)):
            # Repete o bit pela quantidade de vezes informada
            msg_encode = msg_encode + entrada[i] * repeticao
        # Retorna a mensagem protegida
        return msg_encode

    # Decodifica uma mensagem protegida por repetição
    #entrada: mensagem recebida
    #repeticao: quantidade utilizada na codificação
    def decode(self, entrada, repeticao):
        # Verifica se a mensagem pode ser dividida corretamente
        if len(entrada) % repeticao != 0:
            return "O valor do numero da repeticao, precisa ser divisivel pela \nquantidade de caracteres da codeword"
        else:
            # variavel da mensagem recuperada
            msg_decode = ""
            # percorre a mensagem em blocos do tamanho da repetição
            for i in range(0, len(entrada), repeticao):
                # Seleciona um grupo de bits
                pedaco = entrada[i:i+repeticao]
                # conta quantas vezes cada valor aparece
                counter = Counter(pedaco)
                # descobre qual valor aparece mais vezes
                mais_comum = counter.most_common(1)
                # guarda apenas o bit mais frequente
                resultado = mais_comum[0][0]
                # adiciona o resultado à mensagem final
                msg_decode += resultado
            # retorna a mensagem recuperada
            return msg_decode

# ============= TESTES =============            
# ri = repetition_ri()

# encode = ri.encode("10101", 3)
# print("encode: ", encode)

# decode = ri.decode("111000111000111", 4)
# print("decode: ", decode)