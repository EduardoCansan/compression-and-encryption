#usado para contar o termo mais comum de cada pedaco no decode
from collections import Counter 

class repetition_ri:

    def encode(self, entrada, repeticao):
        msg_encode = ""
        
        for i in range(len(entrada)):
            msg_encode = msg_encode + entrada[i] * repeticao
        return msg_encode

    def decode(self, entrada, repeticao):
        #verificacao, a entrada precisa ser divisivel pela quantidade da repeticao
        if len(entrada) % repeticao != 0:
            raise ValueError(
                "O tamanho da entrada deve ser múltiplo da repetição."
            )
        
        msg_decode = ""
        
        for i in range(0, len(entrada), repeticao):
            pedaco = entrada[i:i+repeticao]
        
            counter = Counter(pedaco)
            mais_comum = counter.most_common(1)
            resultado = mais_comum[0][0]
            
            msg_decode+= resultado
            
        return msg_decode
    
ri = repetition_ri()

encode = ri.encode("10101", 3)
print(encode)

decode = ri.decode("111000111000111", 3)
print(decode)