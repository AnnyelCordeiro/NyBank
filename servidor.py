import socket
#from bank import *
import threading
from banco import *

class ClientThread(threading.Thread):
    '''
    Objetos para instanciar o Servidor
    '''
    def __init__(self,clientesock,clienteaddress):
        threading.Thread.__init__(self)
        self.clientesock = clientesock  
        self.clienteaddress = clienteaddress

    def run(self):
        '''
        o servidor recebe uma mensagem do cliente e retorna uma resposta se necessario.
        se a mensagem recebida for uma string vazia, o servidor é encerrado.
        '''
        flag = True
        while flag:
            try:
                recebe = self.clientesock.recv(1024 * 1024).decode().split("*") #define o tamanho dos pacotes recebidos
                print(f"recebe completo: {recebe}")
                metodo = recebe.pop(0)
                print(metodo)
                if(metodo):
                    if metodo =='exit':
                        self.clientesock.close()
                        flag = False
                    else:    
                        banco = Banco()
                        print(banco)
                        print(f"recebe sem o metodo: {recebe}")
                        func = getattr(banco, metodo)
                        re = func(*recebe)
                        print(f"re {re}")
                        self.clientesock.send(f'{re}'.encode()) #'utf-8'
            except Exception as e:
                print(e)

class Servidor():
    
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.bind((self.host,self.port))

    def go(self):
        '''
        Inicia conexão e abre para receber os metodos do cliente
        enviar para o servidor e retornar o desejo que o cliente pede. 
        '''
        flag = True
        while(flag):
            try:
                self.serv_socket.listen(10)
                print('[WAITING CONNECTION...]')
                clientesock,clienteaddress = self.serv_socket.accept()
                print(f'{clienteaddress} CONNECTED')
                novo = ClientThread(clientesock,clienteaddress)
                novo.start()
            except Exception as error:
                print(error)
                return False,'CONNECTION ERROR'

if __name__ == "__main__":
    server = Servidor('localhost',8045) #10.180.47.34
    server.go()
    
    '''
    Parte de conexão de uma única tela.
    '''

    '''
    host = 'localhost' 
    port = 8139
    addr = (host, port)
    self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o socket
    self.serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reinicia o socket
    self.serv_socket.bind(addr) #define as portas e quais ips podem se conectar com o servidor
    self.serv_socket.listen(10) #define o limite de conexões
    print("aguardando conexão...")
    con, cliente = self.serv_socket.accept() #servidor aguardando conexão
    print("conectado")
    print("aguardando mensagem...")
    while True:
        try:
            recebe = con.recv(2048).decode().split("*") #define o tamanho dos pacotes recebidos
            print(f"recebe completo: {recebe}")
            metodo = recebe.pop(0)
            print(metodo)
            if(metodo == ""):
                continue
            banco = Banco()
            print(banco)
            print(f"recebe sem o metodo: {recebe}")
            func = getattr(banco, metodo)
            re = func(*recebe)
            print(f"re {re}")
            con.send(f'{re}'.encode('utf-8')) #'utf-8'
            self.serv_socket.close()
        except Exception as e:
            print(e)
    '''