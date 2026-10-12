"""Hamming (31,26) com paridade par; posicoes 1..31."""
PARIDADES = (1, 2, 4, 8, 16)

def validar(bits, tamanho):
    if len(bits) != tamanho or any(bit not in "01" for bit in bits):
        raise ValueError(f"Entrada deve conter exatamente {tamanho} bits binarios.")

def posicoes_verificadas(paridade):
    return [i for i in range(1, 32) if i & paridade]

def codificar(dados):
    validar(dados, 26)
    palavra = ["0"] * 31
    indice = 0
    for posicao in range(1, 32):
        if posicao not in PARIDADES:
            palavra[posicao - 1] = dados[indice]
            indice += 1
    for paridade in PARIDADES:
        valor = 0
        for posicao in posicoes_verificadas(paridade):
            valor ^= int(palavra[posicao - 1])
        palavra[paridade - 1] = str(valor)
    return "".join(palavra)

def sindrome(palavra):
    validar(palavra, 31)
    resultado = 0
    for paridade in PARIDADES:
        valor = 0
        for posicao in posicoes_verificadas(paridade):
            valor ^= int(palavra[posicao - 1])
        if valor:
            resultado += paridade
    return resultado

def corrigir(palavra):
    posicao = sindrome(palavra)
    if not posicao:
        return palavra, 0
    bits = list(palavra)
    bits[posicao - 1] = "1" if bits[posicao - 1] == "0" else "0"
    return "".join(bits), posicao

def extrair_dados(palavra):
    validar(palavra, 31)
    return "".join(palavra[i - 1] for i in range(1, 32) if i not in PARIDADES)

def demonstracao():
    entradas = (
        "00000000000000000000000000",
        "11111111111111111111111111",
        "10110010101100101011001010",
    )
    for numero, entrada in enumerate(entradas, 1):
        palavra = codificar(entrada)
        print(f"Teste {numero}: entrada={entrada} | Hamming={palavra}")
        assert extrair_dados(palavra) == entrada
        assert sindrome(palavra) == 0
    correta = codificar(entradas[2])
    posicao_erro = 19
    alterada = list(correta)
    alterada[posicao_erro - 1] = "1" if alterada[posicao_erro - 1] == "0" else "0"
    recebida = "".join(alterada)
    recuperada, posicao = corrigir(recebida)
    print(f"Original: {correta}\nCom erro: {recebida}\nSindrome: {posicao:05b} = {posicao}\nCorrigida: {recuperada}")
    assert posicao == posicao_erro and recuperada == correta
    for p in PARIDADES:
        print(f"P{p}: posicoes={posicoes_verificadas(p)}; valor={correta[p-1]}")
    for entrada in entradas:
        correta = codificar(entrada)
        for i in range(31):
            corrompida = correta[:i] + ("1" if correta[i] == "0" else "0") + correta[i+1:]
            assert corrigir(corrompida) == (correta, i + 1)
    print("93 erros isolados corrigidos com sucesso.")

if __name__ == "__main__":
    demonstracao()
