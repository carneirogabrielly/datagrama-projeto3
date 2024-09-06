from enlace import *
import time
from utils import *

serialName = "COM4"  # Configuração da porta correta
imageR = "imgs/image.png"

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
    
        # Ativa comunicação
        com1.enable()
        print("Abriu a comunicação")
        
        # Prevenção de erros
        time.sleep(.2)
        com1.sendData(b'00')  # Envia uma mensagem inicial
        time.sleep(1)   
                
        ##### VERIFICAR SE O SERVIDOR ESTÁ VIVO #####
        print("Verificando se o servidor está vivo")
        # Espera resposta do servidor
        verifica = True
        start_time = time.time()
        while verifica:
            tam = com1.rx.getBufferLen()
            atraso = time.time() - start_time
            if tam >= 1:
                print("Servidor está ativo.")
                break
            else:
                if atraso >= 5:
                    resposta = input("Servidor Inativo. Tentar novamente? s/n? ").lower()
                    if resposta == 's':
                        com1.sendData(b'01')  # Envia uma nova mensagem de verificação
                        print("Verificando se o servidor está vivo")
                        start_time = time.time()
                    elif resposta == 'n':
                        print("Encerrando comunicação")
                        com1.disable()
                        return  # Sai do programa se o usuário escolher 'n'
        
        com1.rx.clearBuffer()  # Limpa o buffer de recepção
        
        ##### FRAGMENTAÇÃO DA MENSAGEM #####
        mensagem = open(imageR, 'rb').read()  # Lê a imagem a ser enviada
        fragmentos = fragmenta(mensagem)
        pacotes = make_pack(fragmentos)  # Cria pacotes para serem enviados

        ##### ENVIO DOS PACOTES #####
        pacote_atual = 0  # Começa no primeiro pacote
        total_pacotes = len(pacotes)

        while verifica and pacote_atual < total_pacotes:
            try:
                # Envia o pacote atual
                com1.sendData(pacotes[pacote_atual])
                print(f"Pacote {pacote_atual + 1} de {total_pacotes} enviado.")
                
                # Espera a resposta do servidor
                head, _, eop = carrega_pacote(com1)
                
                # Verifica o pacote recebido do servidor
                if head[3] == 0:  # Confirmação de sucesso
                    print(f"Pacote {pacote_atual + 1} confirmado.")
                    pacote_atual += 1  # Passa para o próximo pacote
                else:
                    print(f"Erro com o pacote {pacote_atual + 1}. Tentando novamente.")
            
            except Exception as erro:
                print("Erro na comunicação: ", erro)
                print("Tentando reconectar...")
                
                reconectado = False
                tentativas = 0
                while tentativas < 5 and not reconectado:
                    try:
                        com1.sendData(b'01')  # Envia nova verificação
                        head, _, eop = carrega_pacote(com1)  # Espera resposta
                        if head[3] == 0:
                            print("Reconexão bem-sucedida!")
                            reconectado = True
                        else:
                            print("Servidor ainda inativo.")
                        tentativas += 1
                    except Exception as recon_error:
                        print(f"Tentativa {tentativas + 1} de reconexão falhou.")
                        time.sleep(1)  # Aguardar um segundo antes de tentar novamente

                if not reconectado:
                    print("Não foi possível reconectar. Encerrando transmissão.")
                    break  # Se não conseguir reconectar, interrompe a transmissão

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()
