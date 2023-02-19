import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox
from servidor_cliente import *

from pos_login import Ui_Form as PosLogin
from tela_cadastro import Ui_Form as  TelaCadastro
from tela_deposito import Ui_Form as TelaDeposito
from tela_extrato import Ui_Form as TelaExtrato
from tela_inicial import Ui_Inicio_NyBank as TelaInicial
from tela_saque import Ui_Form as TelaSaque
from tela_transfere import Ui_Form as TelaTransfere
from bank import *

class UiMain(QtWidgets.QWidget):

    def setupUi(self,UiMain):
        '''
        Esta classe define a interface gráfica do usuário usando PyQt5.
        Ela é basicamente definida para servir como "empilhamento"(stack) de cada tela e sua respectiva posição. 
        Ele define uma janela principal (Main) e um layout de pilha de várias outras janelas (stack0 a stack6). 
        Elas podem ser alternadas dentro da janela principal. 
        Cada tela é definida em seu próprio arquivo de classe, como TelaCadastro, TelaLogin etc. 
        O método setupUi() é chamado para cada tela para configurar sua aparência e funcionamento, 
        e cada uma delas é adicionada ao layout de pilha por meio do método addWidget().

        Parameters
        ----------
        Main: Object

        Returns
        -------
        None
        '''

        UiMain.setObjectName("UiMain")
        UiMain.resize(640,480)

        self.QtStack = QtWidgets.QStackedLayout()
    
        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()

        self.tela_inicial = TelaInicial()
        self.tela_inicial.setupUi(self.stack0)

        self.tela_cadastro = TelaCadastro()
        self.tela_cadastro.setupUi(self.stack1)

        self.pos_login = PosLogin()
        self.pos_login.setupUi(self.stack2)

        self.tela_extrato = TelaExtrato()
        self.tela_extrato.setupUi(self.stack3)

        self.tela_deposito = TelaDeposito()
        self.tela_deposito.setupUi(self.stack4)

        self.tela_saque = TelaSaque()
        self.tela_saque.setupUi(self.stack5)

        self.tela_transfere = TelaTransfere()
        self.tela_transfere.setupUi(self.stack6)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)

class Main(QMainWindow,UiMain):
    
    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)
        '''
        Este trecho de código abaixo tenta se conectar a um servidor na máquina com o endereço IP 'localhost' e a porta 8042. Se a conexão for recusada, 
        uma caixa de mensagem será exibida informando que não foi possível se conectar ao servidor e a aplicação será encerrada usando sys.exit().
        '''
        try:
            self.server = server_cliente('localhost', 8045)
        except ConnectionRefusedError:
            QtWidgets.QMessageBox.information(None, 'ERROR', f'Não foi possível conectar ao servidor.'
                                                             f'\nVerifique a conexão e tente novamente')
            sys.exit()
        '''
        Este trecho de código abaixo define as conexões de sinal e slot para vários botões da interface do usuário. 
        Cada vez que um botão é clicado, ele chama a função correspondente que executa uma determinada ação. 
        Por exemplo, ao clicar no botão 'ButtonLogin' em 'Tela_Login', o método 'BotaoLogin' é chamado.
        '''

        # Interação tela inicial para tela de cadastro ou para a tela de usuario já cadastrado
        self.tela_inicial.ButtonLogin.clicked.connect(self.botLogin)
        self.tela_inicial.ButtonCadastrar.clicked.connect(self.abreTelaCadastro)
        self.tela_inicial.ButtonSair.clicked.connect(self.sairTelaInicial)
        # Interação de voltar da tela de cadastro para tela inicial
        self.tela_cadastro.ButtonCadastrar.clicked.connect(self.botaocad)
        self.tela_cadastro.ButtonVoltar.clicked.connect(self.abreTelaInicial)

        # Tela pós-login onde conecta para tela de  extrato, transferência, deposito, saque, e retorna para tela inicial
        self.pos_login.ButtonAtualizar.clicked.connect(self.BotaoAtualizar)
        self.pos_login.ButtonExtrato.clicked.connect(self.abreTelaExtrato)
        self.pos_login.ButtonTransferir.clicked.connect(self.abreTelaTransferencia)
        self.pos_login.ButtonDepositar.clicked.connect(self.abreTeladeposito)
        self.pos_login.ButtonSacar.clicked.connect(self.abreTelaSaque)
        self.pos_login.ButtonSair.clicked.connect(self.voltarTelaInicial)
        #self.pos_login.ButtonAtualizar.clicked.connect(self.mostra_Saldo)

        # Tela de extrato que volta para tela de login ou para tela de usuario
        self.tela_extrato.ButtonVoltar.clicked.connect(self.voltarTelaPosLogin)        
        self.tela_extrato.ButtonSair.clicked.connect(self.voltarTelaInicial)

        # Tela de transferência que volta para tela de login ou para tela de usuario
        self.tela_transfere.ButtonTransferir.clicked.connect(self.botTransfere)
        self.tela_transfere.ButtonVoltar.clicked.connect(self.voltarTelaPosLogin)        
        self.tela_transfere.ButtonSair.clicked.connect(self.voltarTelaInicial)

        # Tela de saque que volta para tela de login ou para tela de usuario
        self.tela_saque.ButtonSacar.clicked.connect(self.botSaque)
        self.tela_saque.ButtonVoltar.clicked.connect(self.voltarTelaPosLogin)        
        self.tela_saque.ButtonSair.clicked.connect(self.voltarTelaInicial)

        # Tela de deposito que volta para tela de login ou para tela de usuario
        self.tela_deposito.ButtonDepositar.clicked.connect(self.botDeposito)
        self.tela_deposito.ButtonVoltar.clicked.connect(self.voltarTelaPosLogin)        
        self.tela_deposito.ButtonSair.clicked.connect(self.voltarTelaInicial)

    
    def request_server(self, request):
        '''
        Essa função envia uma requisição de mensagem para o servidor com a request como parâmetro. 
        Em seguida, aguarda uma resposta de até 2048 bytes do servidor e a converte em uma string. 
        Então, remove todos os caracteres desnecessários da resposta e retorna como uma lista de palavras.

        Parameters
        ----------
        request :str

        Returns
        -------
        flag
        '''
        self.server.send(request.encode())
        recv = self.server.recv(2048)
        flag = recv.decode()
        flag = flag.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").replace("'", '').split()
        return flag

    def exit(self):
        '''
        Botão para sair do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.request_server('exit')
        sys.exit()
    
    def concatenar(self, string):
        '''
        Este é um método chamado concatenar que recebe uma string como entrada e concatena todos os caracteres da string, 
        exceto o primeiro caractere (índice 0), com um caractere de espaço entre cada caractere.
        A string concatenada resultante é então retornada.

        Parameters
        ----------
        string: Str

        Returns
        -------
        noti
        '''
        noti = ''
        for i in range(1,len(string)):
            noti += string[i] + "\n"
        return noti
    
    def BotaoAtualizar(self):       
        '''
        Este é um método chamado BotaoAtualizar que é acionado quando o botão "Atualizar" é clicado na tela principal do sistema. 
        Ele cria uma solicitação contendo o número da conta do usuário e o tipo de solicitação, que é "verificarSaldo", e envia essa solicitação para o servidor.

        Em seguida, ele recebe uma resposta do servidor contendo o saldo atualizado da conta. 
        O saldo é formatado como um número de ponto flutuante com duas casas decimais e exibido na tela principal do sistema, 
        na label denominada "labelSaldo".

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''        
        solicit = f'get_saldo*{self.numero}'
        flag = self.request_server(solicit)
        self.Tela_Principal.labelSaldo.setText(f"R$ {float(flag[0]):.2f}")
        
    def botaocad(self):
        '''
        Este é um método chamado botaocad que é acionado quando o botão "Cadastrar" é clicado na tela de cadastro. 
        Ele recupera os valores dos campos de entrada para nome, cpf, 
        usuário e senha da tela de cadastro e verifica se todos os campos estão preenchidos. 
        Se algum campo estiver vazio, uma notificação será exibida na tela.

        Se todos os campos estiverem preenchidos, o código verifica se o CPF tem 11 dígitos e se é composto apenas por números. 
        Em seguida, a senha é codificada em utf-8 e criptografada usando o algoritmo MD5. 
        Uma solicitação é enviada ao servidor contendo as informações do novo usuário a ser adicionado. 
        A resposta do servidor é concatenada em uma string e exibida na tela de cadastro.

        Independentemente de ter sucesso ou falhar, todos os campos da tela de cadastro são limpos para que um novo usuário possa ser adicionado. 
        Se o CPF não atender aos parâmetros necessários, uma notificação informando isso é exibida na tela

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        nome = self.tela_cadastro.lineNome.text()
        cpf = self.tela_cadastro.lineCpf.text()
        usuario = self.tela_cadastro.lineUsuario.text()
        senha = self.tela_cadastro.lineSenha.text()
        if nome != '' and cpf != '' and usuario != '' and senha != '':
            if cpf.isdigit() and len(cpf) == 11:
                solicit = f'adiciona_conta*{usuario}*{senha}*{nome}*{cpf}'
                flag = self.request_server(solicit)
                noti = self.concatenar(flag)
                self.tela_cadastro.lineNome.setText("")
                self.tela_cadastro.lineCpf.setText("")
                self.tela_cadastro.lineUsuario.setText("")
                self.tela_cadastro.lineSenha.setText("")
                self.tela_cadastro.labelNotificacao.setText(noti)
            else:
                self.tela_cadastro.labelNotificacao.setText("O CPF não atendo os parametros.")
        else:
            self.tela_cadastro.labelNotificacao.setText("Todos os espaços devem ser preenchidos.")
        self.tela_cadastro.lineNome.setText("")
        self.tela_cadastro.lineCpf.setText("")
        self.tela_cadastro.lineUsuario.setText("")
        self.tela_cadastro.lineSenha.setText("")    

    def botSaque(self):
        '''
        O método botsaque é chamado quando o usuário clica no botão "Sacar" na tela de operações. 
        Ele pega o valor e a senha inseridos pelo usuário, verifica se o valor é um número válido e codifica a senha usando o algoritmo MD5. 
        Em seguida, constrói uma mensagem com o número da conta, o valor e a senha codificada e envia uma solicitação ao servidor. 
        Se a operação for bem-sucedida, uma mensagem de notificação é exibida na tela de operações, caso contrário, 
        uma mensagem de senha inválida é exibida. Por fim, os campos de valor e senha são limpos.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        valor = self.tela_saque.lineSaldo.text()
        senha = self.tela_saque.lineSenha.text()
        numero = self.tela_saque.lineSaldo_2.text()
        if valor != '' and senha != '':
            try:
                solicit = f'sacar*{numero}*{valor}*{senha}'
                flag = self.request_server(solicit)
                if flag:
                    noti = self.concatenar(flag)
                    self.tela_saque.labelNotificacao.setText(noti)
                else:
                    self.tela_saque.labelNotificacao.setText('Senha invalida.')
            except:
                self.tela_saque.labelNotificacao.setText('Informe somente números no espaço do valor.')
                self.tela_saque.lineSaldo.setText('')
                self.tela_saque.lineSenha.setText('')
        else:
            self.tela_saque.labelNotificacao.setText("Todos os espaços devem estar preenchidos.")
        self.tela_saque.lineSaldo.setText('')
        self.tela_saque.lineSenha.setText('')

    def botDeposito(self):
        '''
        Este é um método chamado botDeposito que é acionado quando o botão "Depositar" é clicado na tela de depósito. 
        Ele verifica se o campo de valor não está vazio e se contém apenas dígitos. 
        Se for o caso, uma solicitação de depósito é enviada ao servidor com o número da conta e o valor do depósito. 
        O campo de notificação da tela de depósito é atualizado com a mensagem retornada pelo servidor e, em seguida, o campo de valor é limpo. 
        Se o campo de valor estiver vazio ou não contiver apenas dígitos, uma mensagem apropriada é exibida no campo de notificação.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        valor = float(self.tela_deposito.lineSaldo.text())
        numero = self.tela_deposito.lineSaldo_2.text()
        print(type(valor))
        if valor != '':
            try:
                solicit = f'depositar*{numero}*{valor}'
                flag = self.request_server(solicit)
                noti = self.concatenar(flag)
                self.tela_deposito.labelNotificacao.setText(noti)
            except Exception as e:
                print(e)    
                self.tela_deposito.labelNotificacao.setText("Informe somente números.")
                self.tela_deposito.lineSaldo.setText('')
        else:
            self.tela_deposito.labelNotificacao.setText("Todos os espaços devem ser preenchidos.")
        self.tela_deposito.lineSaldo.setText('')

    def botTransfere(self):
        '''
        Este é um método chamado botTransfere que é acionado quando o botão "Transferir" é pressionado na tela. 
        Ele pega o valor que foi inserido no campo de valor (lineSaldo), 
        a senha (lineSenha) e o número da conta de destino (lineNumero) da tela de transferência e verifica se todos eles foram preenchidos. 
        Se estiverem preenchidos, ele verifica se os campos de valor e número da conta contêm apenas números. 
        Se ambos forem numéricos, a senha é codificada em UTF-8 e convertida em um hash md5. Em seguida, 
        é criada uma solicitação de transferência com o número da conta de origem (self.numero), a senha hash, 
        o número da conta de destino e o valor a ser transferido. 
        Essa solicitação é enviada para o servidor por meio do método request_server() e a resposta é armazenada na variável flag. 
        Em seguida, a notificação de transferência é exibida na tela de transferência com a mensagem da resposta do servidor. 
        Caso contrário, a notificação informa que apenas números devem ser inseridos nos campos de valor e número da conta, 
        ou que todos os campos devem ser preenchidos. 
        Em todos os casos, os campos de valor, senha e número da conta são redefinidos.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        valor = self.tela_transfere.lineSaldo.text()
        senha = self.tela_transfere.lineSenha.text()
        numero_destino = self.tela_transfere.lineNumero.text()
        numero = self.tela_transfere.lineNumero_2.text()
        if valor != '' and senha != '' and numero != '':
            if valor.replace('.','').isdigit() and numero.replace('.','').isdigit():
                solicit = f'transferir*{numero}*{senha}*{numero_destino}*{valor}'
                flag = self.request_server(solicit)
                noti = self.concatenar(flag)

                self.tela_transfere.labelNotificacao.setText(noti)
            else:
                self.tela_transfere.labelNotificacao.setText("Informe somente números")
        else:
            self.tela_transfere.labelNotificacao.setText("Todos os espaços devem ser preenchidos.")
        self.tela_transfere.lineSaldo.setText('')
        self.tela_transfere.lineSenha.setText('')
        self.tela_transfere.lineNumero.setText('')
        

    def botLogin(self):
        '''
        Este é um método chamado botLogin que é acionado quando o botão "Login" é clicado na tela de login. 
        Ele recupera os valores dos campos de entrada para usuário e senha da tela de login e verifica se ambos estão preenchidos. 
        Se algum campo estiver vazio, uma notificação será exibida na tela.

        Se ambos os campos estiverem preenchidos, o código codifica a senha em utf-8 e a criptografa usando o algoritmo MD5. 
        Em seguida, é criada uma solicitação contendo as informações de login do usuário e enviada para o servidor. 
        A resposta do servidor é recebida e processada. 
        Se o primeiro elemento da resposta for 'True', o login é bem-sucedido e o usuário é direcionado para a tela principal do sistema.

        Caso contrário, uma notificação informando que o login falhou é exibida na tela de login. 
        Independentemente de ter sucesso ou falhar, os campos da tela de login são limpos para que um novo login possa ser feito.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        usuario = self.tela_inicial.lineUsuario.text()
        senha = self.tela_inicial.lineSenha.text()
        if usuario != '' and senha != '':
            solicit = f'login*{usuario}*{senha}'
            flag = self.request_server(solicit)
            if flag[0] == 'True':
                self.pos_login.labelNome.setText(f"Olá, {flag[1]}")
                self.pos_login.labelSaldo.setText(f"R$ {float(flag[2]):.2f}")
                self.pos_login.labelNumero.setText(f"Conta {(flag[3])}")
                global n_atual 
                n_atual = flag[3]
                self.QtStack.setCurrentIndex(2)
            else:
                noti = self.concatenar(flag)
                self.tela_inicial.labelNotificacao.setText(noti)
        else:
            self.tela_inicial.labelNotificacao.setText("Todos os espaços devem ser preenchidos.")
        self.tela_inicial.lineUsuario.setText("")
        self.tela_inicial.lineSenha.setText("")
    
    def abreTelaInicial(self):
        '''
        Botão que direciona para a tela inicial do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(0)

    def abreTelaCadastro(self):
        '''
        Botão que direciona para a tela de cadastro do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(1)

    def abrePosLogin(self,l):
        '''
        Botão que direciona para a tela de usuário do sistema (pós login).

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(2)
    
    def abreTelaExtrato(self):
        '''
        Função responsável por abrir a tela de extrato do usuário após ser clicado o botão extrato.
        É responsável por obter o histórico de transações bancárias do cliente e exibi-las na tela de histórico.
        Para isso, é feita uma solicitação ao servidor bancário com o número da conta do cliente e o tipo de solicitação, que é "historico". 
        Em seguida, o resultado é passado para a função concatenar que formata as informações em uma string para ser exibida na tela.
        Por fim, a string formatada é atribuída ao widget de texto TextHistorico da tela de histórico e a tela de histórico é exibida.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        solicit = f'mostra_his*{n_atual}'
        print(n_atual)
        flag = self.request_server(solicit)
        print(flag)
        noti = self.concatenar(flag)
        self.tela_extrato.TextHistorico.setText(noti)
        self.QtStack.setCurrentIndex(3)

    def abreTeladeposito(self):
        '''
        Botão/Função que direciona para a tela de depósito do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(4)

    def abreTelaSaque(self):
        '''
        Botão/Função que direciona para a tela de saque do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(5)

    def abreTelaTransferencia(self):
        '''
        Botão/Função que direciona para a tela de transferência do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(6)

    def voltarTelaInicial(self):
        '''
        Botão/Função que volta para a tela inicial do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(0)
        
    def sairTelaInicial(self):
        '''
        Botão de saída da tela inicial e encerramento do sistema.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.exit()
        
    def voltarTelaPosLogin(self):
        '''
        Botão/Função que direciona a volta para a tela de usuário do sistema(pós login).

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.QtStack.setCurrentIndex(2)

if __name__ == "__main__":
    '''
    Esse trecho de código é o ponto de entrada do programa. 
    Ele verifica se o módulo atual é o módulo principal (ou seja, não foi importado como um módulo em outro arquivo) e, se for, 
    cria uma instância do aplicativo QApplication e a janela principal Main, e inicia o loop de eventos do aplicativo chamando app.exec_(). 
    Quando a janela principal é fechada, o loop de eventos termina e a execução do programa é encerrada.
    '''
    app = QApplication(sys.argv)
    show_main = Main()
    
    sys.exit(app.exec_())
