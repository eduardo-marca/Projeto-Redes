from adivinhador import Adivinhador
import sys
import socket

def formatarEnvio(texto:str):
    mensagem_bytes = texto.encode()
    tam = len(mensagem_bytes)
    tam_bytes = tam.to_bytes(2,'big')
    return tam_bytes + mensagem_bytes

def obterString(sock:socket):
    dados = sock.recv(2)
    tamanho = int.from_bytes(dados, 'big')
    dados = sock.recv(tamanho)
    return dados.decode()    

adv = None
mec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ('127.0.0.1',50000)
mec.connect(endereco)

mensagemEscolhedor = obterString(mec)

dados = mensagemEscolhedor.split('$')

if dados[0] != 's':
    print('Mensagem inesperada no adivinhador')
    sys.exit(-1)

adv = Adivinhador(dados[1], int(dados[2]))

terminou = False

while not terminou:

    op = input('Deseja chutar (c)letra ou (w)palavra?')

    match(op):

        case 'c':
            letra = adv.lerLetra()
            mensagem = 'c$' + letra
            dadosCodificados = formatarEnvio(mensagem)
            mec.send(dadosCodificados)
        case 'w':
            palavraChute = adv.lerPalavra()
            mensagem = 'w$' + palavraChute
            dadosCodificados = formatarEnvio(mensagem)
            mec.send(dadosCodificados)

    mensagemEscolhedor = obterString(mec)

    dados = mensagemEscolhedor.split('$')
    
    if dados[0] != 'r':
        print('Mensagem inesperada no adivinhador')
        sys.exit(-1)
        
    acertou = True if dados[1] == 'True' else False
    terminou = adv.receberResultado(acertou,int(dados[2]),dados[3])
    mensagem = 'f$' + str(terminou)
    dadosCodificados = formatarEnvio(mensagem)
    mec.send(dadosCodificados)