class Escolhedor:

    def __init__(self, palavra):
        self.palavra = palavra
        self.palavraMascarada = '*'*len(palavra)
        self.vidas = 5

    def validarLetra(self, letra):
        palavraQuebrada = list(self.palavraMascarada)
        acertou = False
        for i in range(len(palavraQuebrada)):
            if letra == self.palavra[i]:
                acertou = True
                palavraQuebrada[i] = letra
        self.palavraMascarada = ''.join(palavraQuebrada)
        if not acertou:
            self.vidas -= 1
        return [acertou, self.vidas, self.palavraMascarada]
    
    def validarPalavra(self, palavraChute):
        if (self.palavra != palavraChute):
            self.vidas -= 1
            acertou = False
        else:
            self.palavraMascarada = self.palavra
            acertou = True
        return [acertou, self.vidas, self.palavraMascarada]
        


