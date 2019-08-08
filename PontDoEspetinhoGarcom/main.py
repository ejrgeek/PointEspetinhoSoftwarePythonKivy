#coding: utf-8

import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivy.utils import get_color_from_hex as hex
from datetime import datetime as dt
import socket
import pickle

Config.set('kivy', 'window_icon', 'img/icone.png')
Config.set('kivy', 'exit_on_escape', '0')

Window.clearcolor = hex("#e9e9bb")
Window.size = (320, 568)
Config.write()

dt = dt.now()
ip = "192.168.0.101"
porta = 3305

def msg_suporte(mensagem):
    mensagem += "\t"
    client = nexmo.Client(key="d22e80ad", secret="gkP38HU7m6KrK7wq")
    client.send_message({
        'from': 'Point do Espetingo',
        'to': '+5583999909409',
        'text': mensagem,
    })


#####     Tela Principal     #####
class Principal(ScreenManager):
    def click_login(self):

        user = self.ids.user.text
        senha = self.ids.senha.text

        query = "SELECT * FROM funcionarios where user = '%s' and senha = '%s';" %(user, senha)
        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        data = tcp.recv(65535)
        queryBD = pickle.loads(data)
        tcp.close()

        for tb_id, tb_data_criado, tb_nome, tb_cpf, tb_user, tb_senha, tb_telefone, tv_endereco, tb_vendas, tb_anotacoes in queryBD:
            if tb_user == user and tb_senha == senha:
                self.ids.user.text = ""
                self.ids.senha.text = ""
                self.current = "Adm"

#####     1 Tela     #####
class AdmApp(Screen):
    pass

#####     1.1 Tela     #####
class PedidoGerenciadorApp(Screen):
    pass

#####     1.1.2 Tela     #####
class FazerPedidoApp(Screen):

    def realizar_pedido(self):

        dia, mes, ano = dt.day, dt.month, dt.year
        data = "%s/%s/%s" %(dia, mes, ano)

        mesa = self.ids.mesa.text
        pedidoTotal = ""

        # Primeira linha de pedido
        pedidoUm = self.ids.pedido1.text
        quantUm = self.ids.quant1.text
        valorUm = self.ids.valor1.text
        quantUm = int(quantUm)
        valorUm = float(valorUm)
        valorTotal = valorUm*quantUm
        pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoUm, quantUm, valorUm)

        if (self.ids.pedido2.text != " " and self.ids.quant2.text != " " and self.ids.valor2.text != " "):
            # Segunda linha de pedido
            pedidoDois = self.ids.pedido2.text
            quantDois = self.ids.quant2.text
            valorDois = self.ids.valor2.text
            quantDois = int(quantDois)
            valorDois = float(valorDois)
            valorTotal += valorDois*quantDois
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoDois, quantDois, valorDois)

        if (self.ids.pedido3.text != " " and self.ids.quant3.text != " " and self.ids.valor3.text != " "):
            # Terceira linha de pedido
            pedidoTres = self.ids.pedido3.text
            quantTres = self.ids.quant3.text
            valorTres = self.ids.valor3.text
            quantTres = int(quantTres)
            valorTres = float(valorTres)
            valorTotal += valorTres * quantTres
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoTres, quantTres, valorTres)

        if (self.ids.pedido4.text != " " and self.ids.quant4.text != " " and self.ids.valor4.text != " "):
            # Quarta linha de pedido
            pedidoQuatro = self.ids.pedido4.text
            quantQuatro = self.ids.quant4.text
            valorQuatro = self.ids.valor4.text
            quantQuatro = int(quantQuatro)
            valorQuatro = float(valorQuatro)
            valorTotal += valorQuatro * quantQuatro
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoQuatro, quantQuatro, valorQuatro)

        if (self.ids.pedido5.text != " " and self.ids.quant5.text != " " and self.ids.valor5.text != " "):
            # Quninta linha de pedido
            pedidoCinco = self.ids.pedido5.text
            quantCinco = self.ids.quant5.text
            valorCinco = self.ids.valor5.text
            quantCinco = int(quantCinco)
            valorCinco = float(valorCinco)
            valorTotal += valorCinco * quantCinco
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoCinco, quantCinco, valorCinco)

        if (self.ids.pedido6.text != " " and self.ids.quant6.text != " " and self.ids.valor6.text != " "):
            # Quninta linha de pedido
            pedidoSeis = self.ids.pedido6.text
            quantSeis = self.ids.quant6.text
            valorSeis = self.ids.valor6.text
            quantSeis = int(quantSeis)
            valorSeis = float(valorSeis)
            valorTotal += valorSeis * quantSeis
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoSeis, quantSeis, valorSeis)



        query = "INSERT INTO pedidos (dia,mesa,pedido,valorTotal) VALUES ('%s','%s','%s','%.2f');" %(data,mesa,pedidoTotal,valorTotal)
        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        tcp.close()

        #zerando dados
        self.ids.mesa.text = ""
        self.ids.pedido1.text = ""
        self.ids.quant1.text = ""
        self.ids.valor1.text = ""
        #####################
        self.ids.pedido2.text = " "
        self.ids.quant2.text = " "
        self.ids.valor2.text = " "
        #####################
        self.ids.pedido3.text = " "
        self.ids.quant3.text = " "
        self.ids.valor3.text = " "
        #####################
        self.ids.pedido4.text = " "
        self.ids.quant4.text = " "
        self.ids.valor4.text = " "
        #####################
        self.ids.pedido5.text = " "
        self.ids.quant5.text = " "
        self.ids.valor5.text = " "
        #####################
        self.ids.pedido6.text = " "
        self.ids.quant6.text = " "
        self.ids.valor6.text = " "

    def atualizar_pedido(self):
        mesaPesq = self.ids.mesa.text
        pedidoTotal = ""

        # Primeira linha de pedido
        pedidoUm = self.ids.pedido1.text
        quantUm = self.ids.quant1.text
        valorUm = self.ids.valor1.text
        quantUm = int(quantUm)
        valorUm = float(valorUm)
        valorTotal = valorUm * quantUm
        pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoUm, quantUm, valorUm)

        if (self.ids.pedido2.text != " " and self.ids.quant2.text != " " and self.ids.valor2.text != " "):
            # Segunda linha de pedido
            pedidoDois = self.ids.pedido2.text
            quantDois = self.ids.quant2.text
            valorDois = self.ids.valor2.text
            quantDois = int(quantDois)
            valorDois = float(valorDois)
            valorTotal += valorDois * quantDois
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoDois, quantDois, valorDois)

        if (self.ids.pedido3.text != " " and self.ids.quant3.text != " " and self.ids.valor3.text != " "):
            # Terceira linha de pedido
            pedidoTres = self.ids.pedido3.text
            quantTres = self.ids.quant3.text
            valorTres = self.ids.valor3.text
            quantTres = int(quantTres)
            valorTres = float(valorTres)
            valorTotal += valorTres * quantTres
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoTres, quantTres, valorTres)

        if (self.ids.pedido4.text != " " and self.ids.quant4.text != " " and self.ids.valor4.text != " "):
            # Quarta linha de pedido
            pedidoQuatro = self.ids.pedido4.text
            quantQuatro = self.ids.quant4.text
            valorQuatro = self.ids.valor4.text
            quantQuatro = int(quantQuatro)
            valorQuatro = float(valorQuatro)
            valorTotal += valorQuatro * quantQuatro
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoQuatro, quantQuatro, valorQuatro)

        if (self.ids.pedido5.text != " " and self.ids.quant5.text != " " and self.ids.valor5.text != " "):
            # Quninta linha de pedido
            pedidoCinco = self.ids.pedido5.text
            quantCinco = self.ids.quant5.text
            valorCinco = self.ids.valor5.text
            quantCinco = int(quantCinco)
            valorCinco = float(valorCinco)
            valorTotal += valorCinco * quantCinco
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoCinco, quantCinco, valorCinco)

        if (self.ids.pedido6.text != " " and self.ids.quant6.text != " " and self.ids.valor6.text != " "):
            # Quninta linha de pedido
            pedidoSeis = self.ids.pedido6.text
            quantSeis = self.ids.quant6.text
            valorSeis = self.ids.valor6.text
            quantSeis = int(quantSeis)
            valorSeis = float(valorSeis)
            valorTotal += valorSeis * quantSeis
            pedidoTotal += "%s | Quantidade: %i | Valor: %.2f\n" % (pedidoSeis, quantSeis, valorSeis)

        valorTotalAtt = valorTotal

        query = "SELECT * FROM pedidos WHERE mesa = '%s';" %(mesaPesq)
        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        data = tcp.recv(65535)
        queryBD = pickle.loads(data)
        tcp.close()

        for numPedido, dia, mesa, pedido, valorTotal in queryBD:
            pedidoAtt = pedido
            valorTotalAtt += valorTotal

        pedidoAtt += "Novos Pedidos:\n"
        pedidoAtt += pedidoTotal
        query = "UPDATE pedidos SET pedido = '%s', valorTotal = '%.2f' WHERE mesa = '%s';" %(pedidoAtt, valorTotalAtt, mesaPesq)

        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        tcp.close()

        # zerando dados
        self.ids.mesa.text = ""
        self.ids.pedido1.text = ""
        self.ids.quant1.text = ""
        self.ids.valor1.text = ""
        #####################
        self.ids.pedido2.text = " "
        self.ids.quant2.text = " "
        self.ids.valor2.text = " "
        #####################
        self.ids.pedido3.text = " "
        self.ids.quant3.text = " "
        self.ids.valor3.text = " "
        #####################
        self.ids.pedido4.text = " "
        self.ids.quant4.text = " "
        self.ids.valor4.text = " "
        #####################
        self.ids.pedido5.text = " "
        self.ids.quant5.text = " "
        self.ids.valor5.text = " "
        #####################
        self.ids.pedido6.text = " "
        self.ids.quant6.text = " "
        self.ids.valor6.text = " "

#####     1.1.3 Tela     ##### FALTA
class PedidoAltDelApp(Screen):

    def pesq_produto(self):
        pesqMesa = self.ids.pesqMesa.text

        query = "SELECT * FROM pedidos WHERE mesa = '%s';" %(pesqMesa)

        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        data = tcp.recv(65535)
        queryBD = pickle.loads(data)
        tcp.close()

        for numPedido, dia, mesa, pedido, valorTotal in queryBD:
            numPedido = str(numPedido)
            valorTotal = str(valorTotal)
            self.ids.dataPedido.text = dia
            self.ids.mesaPedido.text = mesa
            self.ids.numPedido.text = numPedido
            self.ids.valorPedido.text = valorTotal
            self.ids.pedidos.text = pedido
            self.ids.remover.disabled = False


    def remover_produto(self):
        pesq = self.ids.pesqMesa.text
        query = "DELETE FROM pedidos WHERE mesa = '%s';" %(pesq)

        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        tcp.close()
        self.ids.dataPedido.text = ""
        self.ids.mesaPedido.text = ""
        self.ids.numPedido.text = ""
        self.ids.valorPedido.text = ""
        self.ids.pedidos.text = ""
        self.ids.remover.disabled = True

#####     1.6 Tela     #####
class Suporte(Screen):

    def enviar_mensagem(self):
        mensagem = self.ids.mensagem.text
        msg_suporte(mensagem)
        self.ids.mensagem.text = ""

#####     1.7 Tela     #####
class Info(Screen):
    pass

class MainApp(App):

    def build(self):
        self.icon = "img/icone.png"
        return Principal()

janela = MainApp()
janela.title = "Point do Espetinho"

if __name__ == '__main__':
    janela.run()