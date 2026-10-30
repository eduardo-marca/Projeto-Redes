class Adivinhador:

    def __init__(self, palavraMostrada, vidas):
        self.palavraMostrada = palavraMostrada
        self.vidas = vidas

    def lerLetra(self):
        letra = input('Digite sua letra chutada: ')
        letra = letra.lower()
        return letra
    
    def lerPalavra(self):
        validado = False
        while not validado:
            palavra = input('Digite sua palavra chute:')
            if (len(palavra) == len(self.palavraMostrada)):
                validado = True
        return palavra

    def receberResultado(self, acertou, vidas, palavraMostrada):
        if acertou:
            print('Você acertou o chute')
        else:
            print('Você errou')
        self.vidas = vidas
        self.palavraMostrada = palavraMostrada
        print('Palavra da forca:', palavraMostrada)
        print('Número de vidas:', str(vidas))
        if ('*' in self.palavraMostrada and self.vidas > 0):
            terminou = False
        elif('*' not in self.palavraMostrada):
            print('Adivinhador venceu!')
            terminou = True
        else:
            print('Adivinhador perdeu!')
            terminou = True
        return terminou