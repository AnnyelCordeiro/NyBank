import datetime
from random import randint
import mysql.connector as mql

''' Na classe 'Banco' irá fazer as operações com o Banco de Dados'''

class Cliente():
    def __init__(self,nome,cpf):
        self._nome = nome
        self._cpf = cpf

    @property
    def get_nome(self):
        return self._nome
    
    @get_nome.setter
    def set_nome(self,n):
        self._nome = n

    @property
    def get_cpf(self):
        return self._cpf
    
    @get_cpf.setter
    def set_cpf(self,cpf):
        self._cpf = cpf
        
class Conta(Cliente):
    __slots__ = ['_numero','_titular','saldo','_limite','_historico','_senha','_login','_conexao_db','_cursor']
    
    _total_contas = 0
    
    
    def __init__(self,saldo = 0 ,limite = 1000):

        self._numero = 0
        self.saldo = 0
        self._limite = 1000
        #self._historico = ''
        self._senha = 0
        self._login = 0
        self.conexao_db = mql.connect(host = 'localhost', port=3306, database = 'mydb', user = 'nyel', password = '26241730',autocommit = True)
        self.cursor = self.conexao_db.cursor()
        Conta._total_contas += 1

    @staticmethod
    def get_total_contas():
        return Conta._total_contas
    
    @property
    def get_numero(self):
        return self._numero

    @get_numero.setter
    def set_numero(self,n):
        self._numero = n

    @property
    def get_titular(self):
        return self._titular

    @get_titular.setter
    def set_titular(self,t):
        self._titular = t

    @property
    def get_limite(self):
        return self._limite
    
    @get_limite.setter
    def set_limite(self,l):
        self._limite = l

    @property
    def get_historico(self):
        return self._historico

    @get_historico.setter
    def set_historico(self,h):
        self._historico = h

    @property
    def get_senha(self):
        return self._senha
    
    @get_senha.setter
    def set_senha(self,s):
        self._senha = s

    @property
    def get_login(self):
        return self._login
    
    @get_login.setter
    def set_login(self,l):
        self._login = l

    def add_conta(self, usuario, senha, nome, cpf, saldo = 0.0, limite = 1000.0):
        if not self.verificarCPF(cpf):
            if not self.verificarUsuario(usuario):
                self.titular = Cliente(nome, cpf)
                self.historico = Historico()
                data = datetime.datetime.today().strftime("%d/%m/%y %H:%M")
                while True:
                    numero = randint(100, 999)
                    if not self.verificarNumero(numero):
                        self.numero = numero
                        break
                query = f'INSERT INTO cliente(cpf, nome, usuario, senha, numero, saldo, limite, historico) VALUES ("{cpf}", "{nome}", "{usuario}", MD5("{senha}"), {numero}, {saldo}, {limite}, "Data de de abertura: {data}")'
                self.cursor.execute(query)
                self.cursor.execute('select * from cliente')
                print(self.cursor.fetchall())
                return True, "Cadastro realizado com sucesso."
            else:
                return False, 'Usuário já estar cadastrado.'
        else:
            return False, 'CPF já estar cadastrado.'

    def login(self, login, senha):

        flag = self.verificarUsuario(login, senha, False)
        if flag[0]:
            self.cursor.execute(f'SELECT nome, saldo, numero FROM Conta WHERE login = "{login}"')
            Resultado = self.cursor.fetchall()
            print(Resultado)
            return True, Resultado
        else:
            return flag

    def verifica_saldo(self, numero):

        query = f'SELECT saldo, limite from Conta WHERE numero_conta = {numero}'
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        if resultado:
            return resultado
        else:
            return False

    def atualiza_saldo(self, numero, saldo, limite, flag = True):
        saldo = self.verifica_saldo(numero)
        if flag:
            valor += saldo[0][0]
        else:
            valor = saldo[0][0] - valor
        query = f'UPDATE Conta SET saldo = {valor} WHERE numero_conta = {numero}'
        self.cursor.execute(query)

    def verifica_historico(self, numero):
        query = f'SELECT numero_conta WHERE Historico WHERE numero_conta = {numero}'
        self.cursor.execute(query)
        flag = self.cursor.fetchall()
        return flag

    def atualiza_historico(self, numero,hist):
        flag = self.verifica_historico(numero)
        hist = flag[0][0] + hist
        query = f'UPDATE Historico SET tipo_operacao = "{hist}" WHERE numero_conta = {numero}'
        self.cursor.execute(query)

    def verificarUsuario(self, login, senha = None, UserPassword = True):
        if UserPassword:
            self.cursor.execute(f'SELECT login FROM Conta WHERE login = "{login}"')
            exists = self.cursor.fetchall()
            if exists:
                return True    
            return False
        else:
            self.cursor.execute(f'SELECT login, senha FROM Conta WHERE login = "{login}" and senha = MD5("{senha}")')
            exists = self.cursor.fetchall()
            if exists:
                return True
            return False

    def verificaSenha(self, senha, numero):
        self.cursor.execute(f'SELECT senha, numero FROM Conta WHERE senha = MD5("{senha}") AND numero_conta = {numero}')
        exists = self.cursor.fetchall()
        if exists:
            return True
        else:
            return False
    
    def verificarCPF(self, cpf):
        self.cursor.execute(f'SELECT cpf FROM Conta WHERE cpf = "{cpf}"')
        exists = self.cursor.fetchall()
        if exists:
            return True
        else:
            return False

    def verificarNumero(self, numero):
        self.cursor.execute(f'SELECT numero FROM Conta WHERE numero_conta = "{numero}"')
        exists = self.cursor.fetchall()
        if exists:
            return True
        else:
            return False

    def deposita(self,quantidade, t = 0):
        if self._limite < quantidade or quantidade <= 0 or self.saldo + quantidade > self.limite:
            data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            return False, "Não foi possível fazer o deposito."
        else:
            self.saldo += quantidade
            data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            if t:
                self.historico.trasacoes = f" Deposito\n      Valor: {quantidade:.2f}\n       Data: {data}"
            return True, "Deposito realizado com sucesso."

    def saque(self,quantidade,senha,t = 0):
        if quantidade > self.saldo or quantidade <= 0:
            data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            #self.historico.trasacoes = f"Tentativa de saque de {quantidade} na data e hora {data}"
            return False, "Valor maior que o saldo ou quantidade menor que 0."
        else:
            self.saldo -= quantidade
            data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            if t:
                self.historico.trasacoes = f" Saque\n      Valor: {quantidade:.2f}     Data: {data}"
            return True, "Saque realizado com sucesso."


    def extrato(self):
        print(f'Conta:{self._numero}  Saldo:{self.saldo}')
        self._historico.transacao.append(f'Pedido de extrato as {datetime.datetime.now()}')
        

    def transfere(self,destino,quantidade,senha):
        retirou = self.saque(quantidade, False)
        if retirou:
            destino.depositar(quantidade, False)
            data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.historico.trasacoes = f" Transferencia\n       Enviou\n       Valor: {quantidade:.2f}\n       Data: {data}"
            destino.historico.trasacoes = f" Transferencia\n       Recebeu: {self.numero}\n       Valor: {quantidade:.2f}\n       Data: {data}"
            return True, "Transferencia realizada com sucesso."
        else:
            return False, "Não foi possivel finalizar a transferencia."
        '''
        if self.saque(quantidade,senha,1):
            return destino.deposita(quantidade)
        else:
            return False
        '''

class Historico:
    def __init__(self):
        self.data_abertura = datetime.datetime.now()
        self.transacao = []

    def imprime(self):
        extrato = (f'Data abertura: {self.data_abertura}\nTransações:\n')
        for i in self.transacao:
            extrato += i
        return extrato
'''
def gera_numero(b):
    n = randint(100,999)
    for i in b.contas:
        if b.contas[i].get_numero == n:
            return gera_numero()
    return n
'''

def confirma_login(l,s,b):
    if l in b.contas:
        if b.contas[l].get_senha == s:
            return True
        else:   
            return False
    else:
        return False
