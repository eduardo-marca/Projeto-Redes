from escolhedor import Escolhedor
import sys
import socket

def formatarEnvio(texto:str):
    mensagem_bytes = texto.encode()
    tam = len(mensagem_bytes)
    tam_bytes = tam.to_bytes(2,'big')
    return tam_bytes + mensagem_bytes

def obterString(sock:socket):
    dados = sock.recv(2)
    if not dados:
        sys.exit(-1)
    tamanho = int.from_bytes(dados, 'big')
    dados = sock.recv(tamanho)
    return dados.decode()

esc = None

escutador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ('127.0.0.1',50000)
escutador.bind(endereco)

escutador.listen()

mec, _ = escutador.accept()

palavra = input('Escolha a palavra: ')
esc = Escolhedor(palavra)

mensagem = "s$" + esc.palavraMascarada + "$" + str(esc.vidas)
dadosEnvio = formatarEnvio(mensagem)
mec.send(dadosEnvio)

terminou = False

while not terminou:

    mensagemAdivinhador = obterString(mec)
    dados = mensagemAdivinhador.split('$')

    match(dados[0]):

        case 'c':
            [acertou, vidas, palavraMascarada] = esc.validarLetra(dados[1])
            mensagem = 'r$' + str(acertou) + '$' + str(vidas) + '$' + palavraMascarada
            dadosEnvio = formatarEnvio(mensagem)
            mec.send(dadosEnvio)
        case 'w':
            [acertou, vidas, palavraMascarada] = esc.validarPalavra(dados[1])
            mensagem = 'r$' + str(acertou) + '$' + str(vidas) + '$' + palavraMascarada
            dadosEnvio = formatarEnvio(mensagem)
            mec.send(dadosEnvio)
        case _:
            print('recebi no escolhedor uma mensagem inesperada')
            sys.exit(-1)

    mensagemAdivinhador = obterString(mec)
    dados = mensagemAdivinhador.split('$')
    if dados[0] != 'f':
        print('recebi no escolhedor uma mensagem inesperada')
        sys.exit(-1)
    terminou = True if dados[1] == 'True' else False
