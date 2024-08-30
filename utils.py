from aplicacao import *
from enlace import enlace

getData = enlace.getData()

def fragmenta(mensagem : bytes):
    tamanho = len(mensagem)
    inteiro = tamanho // 50
    resto = tamanho % 50
    fragmentos = []
    if inteiro > 0:    
        for i in range(inteiro - 1):
            fragmentos.append(mensagem[i:50 * (i + 1)])
    if resto>0:
        fragmentos.append(mensagem[50*inteiro:])

    return fragmentos

def carrega_pacote(com1):
    head, tamanho_head = com1.getData(12)
    tamanho_payload = int.from_bytes(head[2], byteorder='big')

        #pegando o payload
    payload,_ = com1.getData(tamanho_payload)

        #pegando o eop
    eop,_ = com1.getData(3)

    return head, payload, eop

#----------------------CLIENT------------------------
def make_pack(fragmentos : list):
    head = bytearray(12)
    eop = b'x46\x49\x4D'
    head[0] = len(fragmentos)
    pacotes = []
    for fragmento in fragmentos:
        index = fragmento.index()
        head[1] = index + 1
        head[2] = len(fragmento)
        head[3] = 0
        payload = fragmento
        pacote = bytearray([head, payload, eop])
        pacotes.append(pacote)
    
    return pacotes
#---------------------SERVER-------------------------



def verifica_pack(head, payload, eop):

    qtd_pacotes = head[0]
    numero_pacote = head[1]
    tamanho_payload = head[2]

