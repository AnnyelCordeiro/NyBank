import datetime
from random import randint
import mysql.connector as mql
from bank import *

class Banco():
    ''' 
    A classe Banco instância um objeto Banco capaz de acessar um Banco de Dados para registro
    e transações financeiras como saque, depósitos e tranferências.
    '''

    '''    
        __slots__ : list
        Define todos os atributos que podem ser criados na classe.
    '''
    __slots__ = ['conexao_db', 'cursor']
    
    def __init__(self):
        '''
    conexao_db : 
        Armazena uma instância da classe do Banco de Dados.
    cursor :
        Cursor para percorrer o Banco de Dados.
        '''
        self.conexao_db = mql.connect(host = 'localhost', port=3306, database = 'mydb', user = 'nyel', password = '26241730',autocommit = True)
        self.cursor = self.conexao_db.cursor()

    def adiciona_conta(self, usuario, senha, nome, cpf, saldo = 0.0):
        '''
        Faz a verificação do CPF, se existe ou não, então se o CPF não constar 
        cria uma conta e adiciona ao Banco de Dados.
        :param usuario : str
            Usuário que está sendo cadastrado na conta.
        :param senha : str
            Senha utilizada pelo usuário.
        :param nome : str
            Nome do usuário.
        :param cpf : str
            CPF do usuário.
        :param saldo : float
            saldo inicial do usuário.
        :return : list
            True,mensagem -> cadastro realizado.
            False,mensagem -> cadastro não realizado.
        '''
        if not self.verificarCPF(cpf):
            if not self.verificarUsuario(usuario,senha):
                self.titular = Cliente(nome, cpf)
                self.historico = Historico()
                data = datetime.datetime.today().strftime("%d/%m/%y %H:%M")
                saldo = float(saldo)
                query = f'INSERT INTO Conta(cpf, titular, login, senha, saldo) VALUES ("{cpf}", "{nome}", "{usuario}", MD5("{senha}"), {saldo})'
                self.cursor.execute(query)
                self.cursor.execute('select * from Conta')
                print(self.cursor.fetchall())
                return True, "Cadastro realizado com sucesso."
            else:
                return False, 'Usuário já estar cadastrado.'
        else:
            return False, 'CPF já estar cadastrado.'

    def login(self, login, senha):
        '''
        Verifica se o Usuário existe, se existir o usuário entra na conta.
        :param login : str
            O usuário que deseja fazer o login.
        :param senha: str
            A senha do usuário para acessar a conta.
        :return : list
            True -> O login, saldo, número da conta que foi acessada.
            False -> O usuário e senha que foi enviado para ser verificado.
        '''
        flag = self.verificarUsuario(login, senha)
        print(flag)
        if flag:
            self.cursor.execute(f'SELECT login, saldo, numero_conta FROM Conta WHERE login = "{login}"')
            Resultado = self.cursor.fetchall()
            print(Resultado)
            return True, Resultado
        else:
            return flag

    def get_saldo(self, numero):
        '''
        Verifica o saldo do usuário.
        :param numero : str
            Numero da conta em que irá ser verificado o saldo.
        :return : bool
            True -> retorna o saldo
            False -> caso não tenha saldo a verificar.
        '''
        self.cursor.execute(f'SELECT saldo FROM Conta WHERE numero_conta = {numero}')
        flag = self.cursor.fetchall()
        if flag:
            return flag
        else:
            return False
    
    def set_saldo(self, numero, valor, flag = True):
        '''
        Primeiro verifica o saldo do usuário e após verificar ele atualiza somando 
        ou subtraindo o saldo.
        :param numero : str
            Número da conta que será atualizado saldo. 
        :param valor : float
            Valor a ser somado ou subtraido no saldo.
        :param flag : bool
            Verifica se é True ou False, ele soma se for True e se for False ele subtrai do saldo. 
        '''
        valor = float(valor)
        saldo = self.get_saldo(numero)
        if flag: 
            self.cursor.execute(f'UPDATE Conta SET saldo = saldo + {valor} WHERE numero_conta = {numero}')
        else:
            self.cursor.execute(f'UPDATE Conta SET saldo = saldo - {valor} WHERE numero_conta = {numero}')
    
    def depositar(self,  numero, valor, flag=True):
        '''
        Faz o depósito na conta e insere a operação na tabela de Histórico no Banco de Dados.
        :param numero : str
            Número da conta a ser feito o déposito
        :param valor : float
            valor a ser depositado na conta
        :param flag : bool
            Serve para verificar se realmente é um depósito
        :return : bool
            True -> Se conseguiu realizar o depósito
            False -> Caso não tenha conseguido
        '''
        valor = float(valor)
        flag2 = self.get_saldo(numero)
        if valor <= 0:
            return False, "Não foi possível fazer o deposito."
        else:
            if flag == True:
                tipo = "Deposito"
            else:
                tipo = "Transferência"
            self.cursor.execute(f'UPDATE Conta SET saldo = saldo + {valor} WHERE numero_conta = {numero}')
            self.cursor.execute(f'INSERT INTO Historico(tipo_operacao,data,valor,Conta_numero_conta) VALUES ("{tipo}","{datetime.datetime.today().strftime("%d/%m/%y %H:%M")}",{valor},{numero})')
            return True, "Deposito realizado com sucesso."

    def sacar(self, numero, valor, senha, flag=True):
        '''
        Faz o saque na conta e insere a operação na tabela de Histórico no Banco de Dados.
        :param numero : str
            Número da conta a ser feito o déposito
        :param valor : float
            valor a ser depositado na conta
        :param senha : str
            senha do usuário que está fazendo o saque.
        :param flag : bool
            Serve para verificar se realmente é um depósito
        :return : bool
            True -> Se conseguiu realizar o depósito
            False -> Caso não tenha conseguido
        '''
        valor = float(valor)
        
        flag2 = self.get_saldo(numero)
        print(flag2)
        if valor <= 0 and valor > self.get_saldo(numero):
            return False, "Valor maior que o saldo ou valor menor que 0."
        else:
            if self.verificaSenha(senha, numero):
                if flag == True:
                    tipo = "Saque"
                else:
                    tipo = "Transferência"
                self.cursor.execute(f'UPDATE Conta SET saldo = saldo - {valor} WHERE numero_conta = {numero}')
                self.cursor.execute(f'INSERT INTO Historico(tipo_operacao,data,valor,Conta_numero_conta) VALUES ("{tipo}","{datetime.datetime.today().strftime("%d/%m/%y %H:%M")}",{valor},{numero})')
                return True, "Saque realizado com sucesso."
            return False, "Senha invalida."

    def transferir(self, numero, senha, destino, valor):
        '''
        Faz a transferência de uma conta para outra e insere a operação na tabela de Histórico no Banco de Dados.
        :param numero : str
            Número da conta a ser feita a transferência.
        :param senha : str
            senha do usuário que está fazendo o saque.
        :param destino : str
            Número de destino da transferência.
        :param valor : float
            valor a ser depositado na conta
        :return : bool
            True, mensagem -> Se conseguiu realizar a transferência
            False, mensagem -> Caso não tenha conseguido realizar a transferência
        '''
        valor = float(valor)
        retirou = self.sacar(numero, valor, senha, False)
        if retirou[0]:
            self.depositar(destino, valor, False)
            return True, "Transferencia realizada com sucesso."
        else:
            return False, "Não foi possivel finalizar a transferencia."

    def mostra_his(self,numero):
        '''
        Extrai o histórico no Banco de dados e serve para mostrar na tela
        :param numero : str
            Número da conta que deseja-se ser extraido o histórico e é trazido pois é a chave extrangeira no Banco de Dados.
        :return : str
            result -> retorna a pesquisa no Banco de Dados.
        '''
        query = f"SELECT * FROM Historico WHERE Conta_numero_conta = '{numero}'"
        result = self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(query)
        return result

    def verifica_saldo(self, numero):
        '''
        Verifica o saldo no Banco de Dados
        :param numero : str
            Número da conta de verificação do saldo.
        :returns : list 
            resultado -> retorna o resultado da busca no banco de dados.
            False -> Se não funciona retorna false
        '''
        query = f'SELECT saldo from Conta WHERE numero_conta = {numero}'
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        if resultado:
            return resultado
        else:
            return False

    def atualiza_saldo(self, numero, saldo, flag = True):
        '''
        Verifica o e atualiza saldo no Banco de Dados
        :param numero: str
            Conta a ser atualizada saldo
        :param  saldo : str
            Saldo atual
        :param flag : bool
            Verificar se é para somar ou pra subtrair
        '''
        saldo = self.verifica_saldo(numero)
        if flag:
            valor += saldo[0][0]
        else:
            valor = saldo[0][0] - valor
        query = f'UPDATE Conta SET saldo = {valor} WHERE numero_conta = {numero}'
        self.cursor.execute(query)
        
    def verificarUsuario(self, login, senha, UserPassword = True):
        '''
        Faz a verificação se o usuário existe ou não
        :param login : str
            O usuário a ser verificado
        :param senha : str
            A senha do usuário para ser verificado
        :param UserPassword : bool
            True para que exista um usuário e ir fazer a pesquisa no banco de dados
        :return: list
            True, mensagem -> Existe um usuário 
            False, mensagem -> Não existe o usuário
        '''
        if UserPassword:
            self.cursor.execute(f'SELECT login FROM Conta WHERE login = "{login}"')
            exists = self.cursor.fetchall()
            if exists:
                return True
            return False
        else:
            self.cursor.execute(f'SELECT login FROM Conta WHERE login = "{login}" and senha = MD5("{senha}")')
            exists = self.cursor.fetchall()
            if exists:
                return True,"Existe"
            return False,"Usuario ou senha inexistente"

    def verificaSenha(self, senha, numero):
        '''
        Verifica se a senha está correta
        :param senha : str
            Senha do usuário
        :param numero : str
            Número da conta a ser verificado a senha.
        :return : list
            True, mensagem -> Senha esteja correta
            False, mensagem -> Senha está incorreta
        '''
        self.cursor.execute(f'SELECT senha, numero_conta FROM Conta WHERE senha = MD5("{senha}") AND numero_conta = {numero}')
        exists = self.cursor.fetchall()
        if exists:
            return True,"Senha correta"
        else:
            return False,"Senha Incorreta"
    
    def verificarCPF(self, cpf):
        '''
        Verifica o CPF no banco de dados
        :param cpf : str
            CPF a ser verificado
        :return : bool
            True -> o CPF está correto
            False -> o CPF está incorreto
        '''
        self.cursor.execute(f'SELECT cpf FROM Conta WHERE cpf = "{cpf}"')
        exists = self.cursor.fetchall()
        if exists:
            return True
        else:
            return False

    def verificarNumero(self, numero):
        '''
        Verifica o número no banco de dados
        :param numero : str
            Número a ser verificado
        :return : bool
            True -> o Número está correto
            False -> o Número está incorreto
        '''
        self.cursor.execute(f'SELECT numero_conta FROM Conta WHERE numero_conta = "{numero}"')
        exists = self.cursor.fetchall()
        if exists:
            return True
        else:
            return False