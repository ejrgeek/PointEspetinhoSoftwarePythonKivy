#coding: utf-8

import kivy
kivy.require("1.10.1")

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivy.utils import get_color_from_hex as hex
from datetime import datetime as dt
import socket
import pickle

dt = dt.now()
ip = "192.168.0.101"

Config.set('kivy', 'window_icon', 'img/icone.png')
Config.set('kivy', 'exit_on_escape', '0')

Window.clearcolor = hex("#e9e9bb")
#Window.size = (1024, 600)
Config.write()

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

        query = "SELECT * FROM admin where user = '%s' and senha = '%s';" % (user, senha)
        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        data = tcp.recv(65535)
        queryBD = pickle.loads(data)
        tcp.close()
        for tb_id, tb_nome, tb_user, tb_senha in queryBD:
            if tb_user == user and tb_senha == senha:
                self.ids.user.text = ""
                self.ids.senha.text = ""
                self.current = "Cozinha"

#####     1.0 Tela     #####
class CozinhaApp(Screen):
    pass

#####     1.0.1 Tela     #####
class PedidosApp(Screen):

    def ver_pedidos(self):

        query = "SELECT * FROM pedidos;"
        host = ip
        porta = 3305
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        desktopServer = (host, porta)
        tcp.connect(desktopServer)
        tcp.send(query.encode())
        data = tcp.recv(65535)
        queryBD = pickle.loads(data)
        tcp.close()

        mostraPedidos = ""
        for numPedido, dia, mesa, pedido, valorTotal in queryBD:
            mostraPedidos += "Numero do Pedido: %s\n" % numPedido
            mostraPedidos += "Data: %s\n" % dia
            mostraPedidos += "Mesa: %s\n" % mesa
            mostraPedidos += "Pedido:\n%s\n" % pedido
            mostraPedidos += "Valor Total: %s\n" % valorTotal
            mostraPedidos += "---------------------------\n"
        self.ids.cardPedidos.text = mostraPedidos

#####     1.0.2 Tela     ##### FALTA
class BuscarPedidoApp(Screen):
    def pesq_produto(self):
        pesqMesa = self.ids.pesqMesa.text

        query = "SELECT * FROM pedidos WHERE mesa = '%s';" % (pesqMesa)
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


#####     1.1 Tela     #####
class Suporte(Screen):

    def enviar_mensagem(self):
        mensagem = self.ids.mensagem.text
        msg_suporte(mensagem)
        self.ids.mensagem.text = ""

#####     1.2 Tela     #####
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
