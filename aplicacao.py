#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from utils import *
from enlaceRx import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM15"                  # Windows(variacao de)

imageW = 'imgs/img.png'
def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        print("Abriu a comunicação")
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(1)
           
       #-------- VERIFICANDO SE ESTÁ ATIVO ------------
        pacote0 = com1.sendData(make_pack_server(True))
        com1.rx.clearBuffer()
        #---------RECEBENDO AS MENSAGENS -------------
        lista_payload = []
        head, payload, eop = carrega_pacote(com1)
        tamanho_da_mensagem = head[0]

        verifica = verifica_pack(head,eop, 1)
        if verifica:
                lista_payload.append(payload)
                pacote = make_pack_server(verifica)
                com1.sendData(pacote)
        else:
            pacote = make_pack_server(verifica)
            com1.sendData(pacote)
        print('Recebi pacote 1')

        if verifica:
            for i in range(tamanho_da_mensagem - 1):

                # time.sleep(.1)
                # print(com1.rx.getBufferLen())
                # start_time = time.time()
                # while (com1.rx.getBufferLen() < 15):
                #     atraso = time.time() - start_time
                #     if atraso > 5:
                #         com1.sendData(pacote)
                #         com1.rx.clearBuffer()
                #         time.sleep(1)
                    

                head, payload, eop = carrega_pacote(com1)
                print(head)
                verifica = verifica_pack(head, eop, i+2)
                if verifica:
                    lista_payload.append(payload)
                    pacote = make_pack_server(verifica)
                    com1.sendData(pacote)
                    print(pacote)
                else:
                    pacote = make_pack_server(verifica)
                    com1.sendData(pacote)
                print(f'Recebi pacote {i+2}')

            payload_completo = b''.join(lista_payload)
            f = open(imageW, 'wb')
            f.write(payload_completo)
            #fecha arquivo de imagem
            f.close()

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
