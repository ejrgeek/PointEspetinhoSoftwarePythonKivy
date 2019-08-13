# coding: utf-8

import kivy

kivy.require("1.10.1")

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.utils import get_color_from_hex as hex
import nexmo
import webbrowser as web
from datetime import datetime as dt
import sqlite3 as sql

dt = dt.now()
urlBD = "C:/Users/ejrfl/Dropbox/bd_pointEsp/pointesp.db"
conn = sql.connect(urlBD)
cursor = conn.cursor()
conn.close()

def disconectBD():
    return conn.close()


Config.set('kivy', 'window_icon', 'img/icone.png')
Config.set('kivy', 'exit_on_escape', '0')

Window.clearcolor = hex("#e9e9bb")
Window.size = (1366, 768)
Config.write()


def msg_suporte(mensagem):
    mensagem += "\t"
    client = nexmo.Client(key="key", secret="keySecrete")
    client.send_message({
        'from': 'Destinatario',
        'to': 'number',
        'text': mensagem,
    })


#####     Tela Principal     ##### COMPLETO
class Principal(ScreenManager):
    teclaEnterFuncao = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Principal, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if keycode == 40:  # 40 - Enter key pressed
            if (self.ids.user.text == "" or  self.ids.senha.text == ""):
                self.ids.infoSenhaUser.text = "Preencha os campos"
            else:
                self.click_login()

    def click_login(self):

        validar = False
        user = self.ids.user.text
        senha = self.ids.senha.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE user = ? AND senha = ?", (user, senha))
        for tb_id, tb_nome, tb_user, tb_senha in cursor.fetchall():
            if tb_user == user and tb_senha == senha:
                self.ids.user.text = ""
                self.ids.senha.text = ""
                self.current = "Adm"
                validar = True

        if validar == True:
            self.ids.infoSenhaUser.text = ""
        else:
            self.ids.infoSenhaUser.text = "Usuario e/ou Senha errados"
        disconectBD()

#####     1 Tela     #####
class AdmApp(Screen):
    pass


#####     1.1 Tela     #####
class CaixaApp(Screen):
    pass


#####     1.1.1 Tela     #####
class PedidosApp(Screen):

    def ver_pedidos(self):
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos")
        mostraPedidos = "\n"
        for numPedido, dia, mesa, pedido, valorTotal in cursor.fetchall():
            mostraPedidos += "Numero do Pedido: %s\n" % numPedido
            mostraPedidos += "Data: %s\n" % dia
            mostraPedidos += "Mesa: %s\n" % mesa
            mostraPedidos += "Pedido:\n%s\n" % pedido
            mostraPedidos += "Valor Total: %s\n" % valorTotal
            mostraPedidos += "---------------------------\n"

        self.ids.cardPedidos.text = mostraPedidos
        disconectBD()


#####     1.1.2 Tela     #####
class FazerPedidoApp(Screen):

    def realizar_pedido(self):

        dia, mes, ano = dt.day, dt.month, dt.year
        data = f"{dia}/{mes}/{ano}"

        mesaPesq = self.ids.mesa.text
        pedidoTotal = ""

        # Primeira linha de pedido
        pedidoUm = self.ids.pedido1.text
        quantUm = self.ids.quant1.text
        valorUm = self.ids.valor1.text
        quantUm = int(quantUm)
        valorUm = float(valorUm)
        valorTotal = valorUm * quantUm
        pedidoTotal += f"{pedidoUm} | Quantidade: {quantUm} | Valor: {valorUm}\n"

        if (self.ids.pedido2.text != "" and self.ids.quant2.text != "" and self.ids.valor2.text != ""):
            # Segunda linha de pedido
            pedidoDois = self.ids.pedido2.text
            quantDois = self.ids.quant2.text
            valorDois = self.ids.valor2.text
            quantDois = int(quantDois)
            valorDois = float(valorDois)
            valorTotal += valorDois * quantDois
            pedidoTotal += f"{pedidoDois} | Quantidade: {quantDois} | Valor: {valorDois}\n"

        if (self.ids.pedido3.text != "" and self.ids.quant3.text != "" and self.ids.valor3.text != ""):
            # Terceira linha de pedido
            pedidoTres = self.ids.pedido3.text
            quantTres = self.ids.quant3.text
            valorTres = self.ids.valor3.text
            quantTres = int(quantTres)
            valorTres = float(valorTres)
            valorTotal += valorTres * quantTres
            pedidoTotal += f"{pedidoTres} | Quantidade: {quantTres} | Valor: {valorTres}\n"

        if (self.ids.pedido4.text != "" and self.ids.quant4.text != "" and self.ids.valor4.text != ""):
            # Quarta linha de pedido
            pedidoQuatro = self.ids.pedido4.text
            quantQuatro = self.ids.quant4.text
            valorQuatro = self.ids.valor4.text
            quantQuatro = int(quantQuatro)
            valorQuatro = float(valorQuatro)
            valorTotal += valorQuatro * quantQuatro
            pedidoTotal += f"{pedidoQuatro} | Quantidade: {quantQuatro} | Valor: {valorQuatro}\n"

        if (self.ids.pedido5.text != "" and self.ids.quant5.text != "" and self.ids.valor5.text != ""):
            # Quninta linha de pedido
            pedidoCinco = self.ids.pedido5.text
            quantCinco = self.ids.quant5.text
            valorCinco = self.ids.valor5.text
            quantCinco = int(quantCinco)
            valorCinco = float(valorCinco)
            valorTotal += valorCinco * quantCinco
            pedidoTotal += f"{pedidoCinco} | Quantidade: {quantCinco} | Valor: {valorCinco}\n"

        if (self.ids.pedido6.text != "" and self.ids.quant6.text != "" and self.ids.valor6.text != ""):
            # Quninta linha de pedido
            pedidoSeis = self.ids.pedido6.text
            quantSeis = self.ids.quant6.text
            valorSeis = self.ids.valor6.text
            quantSeis = int(quantSeis)
            valorSeis = float(valorSeis)
            valorTotal += valorSeis * quantSeis
            pedidoTotal += f"{pedidoSeis} | Quantidade: {quantSeis} | Valor: {valorSeis}\n"
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO pedidos (dia,mesa,pedido,valorTotal)
                          VALUES(?,?,?,?)""", (data, mesaPesq, pedidoTotal, valorTotal))
        conn.commit()
        disconectBD()
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
        pedidoTotal += f"{pedidoUm} | Quantidade: {quantUm} | Valor: {valorUm}\n"

        if (self.ids.pedido2.text != " " and self.ids.quant2.text != " " and self.ids.valor2.text != " "):
            # Segunda linha de pedido
            pedidoDois = self.ids.pedido2.text
            quantDois = self.ids.quant2.text
            valorDois = self.ids.valor2.text
            quantDois = int(quantDois)
            valorDois = float(valorDois)
            valorTotal += valorDois * quantDois
            pedidoTotal += f"{pedidoDois} | Quantidade: {quantDois} | Valor: {valorDois}\n"

        if (self.ids.pedido3.text != " " and self.ids.quant3.text != " " and self.ids.valor3.text != " "):
            # Terceira linha de pedido
            pedidoTres = self.ids.pedido3.text
            quantTres = self.ids.quant3.text
            valorTres = self.ids.valor3.text
            quantTres = int(quantTres)
            valorTres = float(valorTres)
            valorTotal += valorTres * quantTres
            pedidoTotal += f"{pedidoTres} | Quantidade: {quantTres} | Valor: {valorTres}\n"

        if (self.ids.pedido4.text != " " and self.ids.quant4.text != " " and self.ids.valor4.text != " "):
            # Quarta linha de pedido
            pedidoQuatro = self.ids.pedido4.text
            quantQuatro = self.ids.quant4.text
            valorQuatro = self.ids.valor4.text
            quantQuatro = int(quantQuatro)
            valorQuatro = float(valorQuatro)
            valorTotal += valorQuatro * quantQuatro
            pedidoTotal += f"{pedidoQuatro} | Quantidade: {quantQuatro} | Valor: {valorQuatro}\n"

        if (self.ids.pedido5.text != " " and self.ids.quant5.text != " " and self.ids.valor5.text != " "):
            # Quninta linha de pedido
            pedidoCinco = self.ids.pedido5.text
            quantCinco = self.ids.quant5.text
            valorCinco = self.ids.valor5.text
            quantCinco = int(quantCinco)
            valorCinco = float(valorCinco)
            valorTotal += valorCinco * quantCinco
            pedidoTotal += f"{pedidoCinco} | Quantidade: {quantCinco} | Valor: {valorCinco}\n"

        if (self.ids.pedido6.text != " " and self.ids.quant6.text != " " and self.ids.valor6.text != " "):
            # Quninta linha de pedido
            pedidoSeis = self.ids.pedido6.text
            quantSeis = self.ids.quant6.text
            valorSeis = self.ids.valor6.text
            quantSeis = int(quantSeis)
            valorSeis = float(valorSeis)
            valorTotal += valorSeis * quantSeis
            pedidoTotal += f"{pedidoSeis} | Quantidade: {quantSeis} | Valor: {valorSeis}\n"

        valorTotalAtt = valorTotal

        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE mesa = ?", [mesaPesq])
        for numPedido, dia, mesa, pedido, valorTotal in cursor.fetchall():
            pedidoAtt = pedido
            valorTotalAtt += valorTotal
        pedidoAtt += "Novos Pedidos:\n"
        pedidoAtt += pedidoTotal
        cursor.execute("""UPDATE pedidos SET pedido = :pedido, valorTotal = :valorTotal WHERE mesa = :mesa""",
                       {'pedido': pedidoAtt, 'mesa': mesaPesq, 'valorTotal': valorTotalAtt})
        conn.commit()
        disconectBD()
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
    def pesq_pedido(self):
        pesq = self.ids.pesqMesa.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE mesa = ?", [pesq])

        for numPedido, dia, mesa, pedido, valorTotal in cursor.fetchall():
            numPedido = str(numPedido)
            valorTotal = str(valorTotal)
            self.ids.dataPedido.text = dia
            self.ids.mesaPedido.text = mesa
            self.ids.numPedido.text = numPedido
            self.ids.valorPedido.text = valorTotal
            self.ids.pedidos.text = pedido
            self.ids.pedidos.disabled = False
            self.ids.remover.disabled = False
            self.ids.imprimir.disabled = False
            self.ids.pagar.disabled = False
        disconectBD()

    def remover_pedido(self):
        pesq = self.ids.pesqMesa.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE mesa = ?", [pesq])
        conn.commit()
        disconectBD()
        self.ids.dataPedido.text = ""
        self.ids.mesaPedido.text = ""
        self.ids.numPedido.text = ""
        self.ids.valorPedido.text = ""
        self.ids.pedidos.text = ""
        self.ids.remover.disabled = True
        self.ids.imprimir.disabled = True
        self.ids.pagar.disabled = True

    def imprimir_pedido(self):
        pesq = self.ids.pesqMesa.text

        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE mesa = ?", [pesq])

        numPedidoPago = 0
        diaPago = ""
        mesaPago = ""
        pedidoPago = ""
        valorTotalPago = 0.0

        for numPedido, dia, mesa, pedido, valorTotal in cursor.fetchall():
            numPedidoPago = numPedido
            diaPago = dia
            mesaPago = mesa
            pedidoPago = pedido
            valorTotalPago = valorTotal
        disconectBD()

        bannerNota = "POINT DO ESPETINHO\n" \
                     "ORG: José Filho e Leila Sousa\n" \
                     "-------------------------------------\n" \
                     f"Data do Pedido: {diaPago}\n" \
                     f"Numero do Pedido: {numPedidoPago}\n" \
                     f"Mesa: {mesaPago}\n" \
                     f"\nPedidos: \n{pedidoPago}\n" \
                     "--------------------\n" \
                     f"Valor Total: {valorTotalPago}\n\n" \
                     "AGRADEÇEMOS A PREFERÊNCIA\n" \
                     "VOLTE SEMPRE!\n" \
                     "\nEndereço:\n" \
                     "Rua Luciander Rocha Melo de Lucena\n" \
                     "N° 16,  Centro, 58800-710"
        arq = open("C:/Users/ejrfl/Dropbox/bd_pointEsp/imprimir/nota.txt", "w")
        assert isinstance(bannerNota, object)
        arq.writelines(bannerNota)
        arq.close()
        web.open("file:///C:/Users/ejrfl/Dropbox/bd_pointEsp/imprimir/nota.txt")

    def pagar_pedido(self):
        pesq = self.ids.pesqMesa.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE mesa = ?", [pesq])

        diaPago = ""
        mesaPago = ""
        pedidoPago = ""
        valorTotalPago = 0.0

        for numPedido, dia, mesa, pedido, valorTotal in cursor.fetchall():
            diaPago = dia
            mesaPago = mesa
            pedidoPago = pedido
            valorTotalPago = valorTotal
        conn.commit()

        cursor.execute("INSERT INTO pedidosPagos (dia, mesa, pedido, valorTotal) VALUES (?, ?, ?, ?)",
                       (diaPago, mesaPago, pedidoPago, valorTotalPago))
        conn.commit()

        cursor.execute("DELETE FROM pedidos WHERE mesa = ?", ([pesq]))
        conn.commit()
        disconectBD()

        self.ids.dataPedido.text = ""
        self.ids.mesaPedido.text = ""
        self.ids.numPedido.text = ""
        self.ids.valorPedido.text = ""
        self.ids.pedidos.text = ""
        self.ids.remover.disabled = True
        self.ids.imprimir.disabled = True
        self.ids.pagar.disabled = True


#####     1.1.4 Tela     #####
class CardapioApp(Screen):

    def espetinhos(self):
        self.ids.card.text = ""
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cardapio WHERE tipo == 'Espetinho'")
        itens = "\n"
        for id, codigo, tipo, nome, detalhes, valor in cursor.fetchall():
            itens += f"CODIGO: {codigo} | ESPETINHO: {nome} | VALOR: {valor} Reais\n"
            itens += "-" * 100 + "\n"
        self.ids.card.text = itens
        disconectBD()

    def porcoes(self):
        self.ids.card.text = ""
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cardapio WHERE tipo == 'Porção'")
        itens = "\n"
        for id, codigo, tipo, nome, detalhes, valor in cursor.fetchall():
            itens += f"CODIGO: {codigo} | PORCAO: {nome} | VALOR: {valor} Reais\n"
            itens += "-" * 100 + "\n"
        self.ids.card.text = itens
        disconectBD()

    def caldos(self):
        self.ids.card.text = ""
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cardapio WHERE tipo == 'Caldos'")
        itens = "\n"
        for id, codigo, tipo, nome, detalhes, valor in cursor.fetchall():
            itens += f"CODIGO: {codigo} | CALDO: {nome} | VALOR: {valor} Reais\n"
            itens += "-" * 100 + "\n"
        self.ids.card.text = itens
        disconectBD()

    def bebidas(self):
        self.ids.card.text = ""
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cardapio WHERE tipo == 'Bebida'")
        itens = "\n"
        for id, codigo, tipo, nome, detalhes, valor in cursor.fetchall():
            itens += f"CODIGO: {codigo} | BEBIDA: {nome} | VALOR: {valor} Reais\n"
            itens += "-" * 100 + "\n"
        self.ids.card.text = itens
        disconectBD()


#####     1.1.5 Tela     #####
class CardapioAddApp(Screen):

    def cadastro_cardapio(self):
        tipoCardapio = self.ids.tipoCardapio.text
        valorCardapio = self.ids.valorCardapio.text
        nomeCardapio = self.ids.nomeCardapio.text
        codigoCardapio = self.ids.codigoCardapio.text
        detalheCardapio = self.ids.detalheCardapio.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO cardapio (codigo, tipo, nome, detalhes, valor)
                          VALUES (?,?,?,?,?)""",
                       (codigoCardapio, tipoCardapio, nomeCardapio, detalheCardapio, valorCardapio))
        conn.commit()
        disconectBD()
        self.ids.tipoCardapio.text = ""
        self.ids.valorCardapio.text = ""
        self.ids.nomeCardapio.text = ""
        self.ids.codigoCardapio.text = ""
        self.ids.detalheCardapio.text = ""


#####     1.1.6 Tela     #####
class CardapioAltDelApp(Screen):

    def pesq_cardapio(self):
        pesq = self.ids.pesqCardapio.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cardapio WHERE codigo = ?", (pesq,))

        for id, codigo, tipo, nome, detalhes, valor in cursor.fetchall():
            codigo = str(codigo)
            valor = str(valor)
            self.ids.tipoCardapio.text = tipo
            self.ids.codigoCardapio.text = codigo
            self.ids.nomeCardapio.text = nome
            self.ids.valorCardapio.text = valor
            self.ids.detalheCardapio.text = detalhes
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
        disconectBD()

    def alterar_cardapio(self):
        self.ids.tipoCardapio.disabled = False
        self.ids.nomeCardapio.disabled = False
        self.ids.valorCardapio.disabled = False
        self.ids.detalheCardapio.disabled = False
        self.ids.salvar.disabled = False

    def aplicar(self):
        codigo = self.ids.pesqCardapio.text
        tipoCardapio = self.ids.tipoCardapio.text
        valorCardapio = self.ids.valorCardapio.text
        nomeCardapio = self.ids.nomeCardapio.text
        detalheCardapio = self.ids.detalheCardapio.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""UPDATE cardapio SET tipo = :tipo, nome = :nome, detalhes = :detalhes,
                        valor = :valor WHERE codigo = :codigo""",
                       {'tipo': tipoCardapio, 'nome': nomeCardapio, 'detalhes': detalheCardapio, 'valor': valorCardapio,
                        'codigo': codigo})
        conn.commit()

        pesq = self.ids.pesqCardapio.text
        cursor.execute("SELECT * FROM pedidos WHERE numPedido = ?", (pesq,))

        for id, codigo, tipo, nome, detalhes, valor in cursor.fetchall():
            self.ids.tipoCardapio.text = tipo
            self.ids.codigoCardapio.text = codigo
            self.ids.nomeCardapio.text = nome
            self.ids.valorCardapio.text = valor
            self.ids.detalheCardapio.text = detalhes
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
            self.ids.salvar.disabled = True
        disconectBD()
        self.ids.tipoCardapio.disabled = True
        self.ids.valorCardapio.disabled = True
        self.ids.nomeCardapio.disabled = True
        self.ids.detalheCardapio.disabled = True

    def remover_cardapio(self):

        pesq = self.ids.pesqCardapio.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cardapio WHERE codigo = ?", (pesq,))
        conn.commit()
        disconectBD()
        self.ids.tipoCardapio.text = ""
        self.ids.codigoCardapio.text = ""
        self.ids.nomeCardapio.text = ""
        self.ids.valorCardapio.text = ""
        self.ids.detalheCardapio.text = ""
        self.ids.remover.disabled = True
        self.ids.alterar.disabled = True
        self.ids.salvar.disabled = True


#####     1.2 Tela     #####
class FuncApp(Screen):
    pass


#####     1.2.1 Tela     #####
class CadastrarFunc(Screen):

    def cadastro_func(self):
        dia, mes, ano = dt.day, dt.month, dt.year
        data = f"{dia}/{mes}%s/{ano}"

        nome = self.ids.nome.text
        cpf = self.ids.cpf.text
        endereco = self.ids.endereco.text
        telefone = self.ids.telefone.text
        usuario = self.ids.userFunc.text
        senha = self.ids.senhaFunc.text
        anotacao = self.ids.anotacao.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO funcionarios(data_criado,nome,cpf,user,senha,telefone,endereco,anotacoes)
        VALUES(?,?,?,?,?,?,?,?)""", (data, nome, cpf, usuario, senha, telefone, endereco, anotacao))
        conn.commit()
        disconectBD()
        self.ids.nome.text = ""
        self.ids.cpf.text = ""
        self.ids.endereco.text = ""
        self.ids.telefone.text = ""
        self.ids.userFunc.text = ""
        self.ids.senhaFunc.text = ""
        self.ids.anotacao.text = ""


#####     1.2.2 Tela     #####
class Funcionarios(Screen):

    def pesq_func(self):
        pesq = self.ids.pesq.text
        if pesq == "":
            self.ids.nome.text = ""
            self.ids.cpf.text = ""
            self.ids.userFunc.text = ""
            self.ids.senhaFunc.text = ""
            self.ids.telefone.text = ""
            self.ids.endereco.text = ""
            self.ids.vendas.text = ""
            self.ids.anotacao.text = ""
            self.ids.alterar.disabled = True
            self.ids.remover.disabled = True
            self.ids.salvar.disabled = True
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", [pesq])

        for id, data_criado, nome, cpf, user, senha, telefone, endereco, vendas, anotacoes in cursor.fetchall():
            self.ids.nome.text = nome
            self.ids.cpf.text = cpf
            self.ids.userFunc.text = user
            self.ids.senhaFunc.text = senha
            self.ids.telefone.text = telefone
            self.ids.endereco.text = endereco
            if vendas == None:
                self.ids.vendas.text = "Vendas: 0"
            else:
                self.ids.vendas.text = f"Vendas: {vendas}"

            self.ids.anotacao.text = anotacoes
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
        disconectBD()

    def alterar_func(self):

        self.ids.nome.disabled = False
        self.ids.senhaFunc.disabled = False
        self.ids.telefone.disabled = False
        self.ids.endereco.disabled = False
        self.ids.anotacao.disabled = False
        self.ids.salvar.disabled = False

    def remover_func(self):
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        pesq = self.ids.pesq.text
        cursor.execute("DELETE FROM funcionarios WHERE cpf = ?", [pesq])
        conn.commit()
        disconectBD()
        self.ids.nome.text = ""
        self.ids.cpf.text = ""
        self.ids.userFunc.text = ""
        self.ids.senhaFunc.text = ""
        self.ids.telefone.text = ""
        self.ids.endereco.text = ""
        self.ids.vendas.text = ""
        self.ids.anotacao.text = ""
        self.ids.alterar.disabled = True
        self.ids.remover.disabled = True
        self.ids.salvar.disabled = True

    def aplicar(self):
        pesq = self.ids.pesq.text
        nome = self.ids.nome.text
        senha = self.ids.senhaFunc.text
        telefone = self.ids.telefone.text
        endereco = self.ids.endereco.text
        anotacao = self.ids.anotacao.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""UPDATE funcionarios
                SET nome = :nome, senha = :senha, telefone = :telefone,
                    endereco = :endereco, anotacoes = :anotacao
                WHERE cpf = :cpf""",
                       {'nome': nome, 'senha': senha, 'telefone': telefone, 'endereco': endereco, 'anotacao': anotacao,
                        'cpf': pesq})
        conn.commit()

        cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", [pesq])
        for id, data_criado, nome, cpf, user, senha, telefone, endereco, vendas, anotacoes in cursor.fetchall():
            self.ids.nome.text = nome
            self.ids.cpf.text = cpf
            self.ids.userFunc.text = user
            self.ids.senhaFunc.text = senha
            self.ids.telefone.text = telefone
            self.ids.endereco.text = endereco
            self.ids.vendas.text = f"Vendas: {vendas}"
            self.ids.anotacao.text = anotacoes
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
        disconectBD()
        self.ids.nome.disabled = True
        self.ids.senhaFunc.disabled = True
        self.ids.telefone.disabled = True
        self.ids.endereco.disabled = True
        self.ids.anotacao.disabled = True
        self.ids.salvar.disabled = True


#####     1.3 Tela     #####
class ClienteApp(Screen):
    pass


#####     1.3.1 Tela     #####
class CadastrarCliente(Screen):

    def cadastro_cliente(self):
        dia, mes, ano = dt.day, dt.month, dt.year
        data = f"{dia}/{mes}%s/{ano}"

        nome = self.ids.nome.text
        cpf = self.ids.cpf.text
        endereco = self.ids.endereco.text
        telefone = self.ids.telefone.text
        cidade = self.ids.cidade.text
        uf = self.ids.uf.text
        anotacao = self.ids.anotacao.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO clientes (data_criado,nome,cpf,telefone,endereco,cidade,uf,anotacoes)
        VALUES(?,?,?,?,?,?,?,?)""", (data, nome, cpf, telefone, endereco, cidade, uf, anotacao))
        conn.commit()
        disconectBD()
        self.ids.nome.text = ""
        self.ids.cpf.text = ""
        self.ids.endereco.text = ""
        self.ids.telefone.text = ""
        self.ids.cidade.text = ""
        self.ids.uf.text = ""
        self.ids.anotacao.text = ""


#####     1.3.2 Tela     #####
class Clientes(Screen):

    def pesq_func(self):

        pesq = self.ids.pesq.text
        if pesq == "":
            self.ids.nome.text = ""
            self.ids.cpf.text = ""
            self.ids.cidade.text = ""
            self.ids.uf.text = ""
            self.ids.telefone.text = ""
            self.ids.endereco.text = ""
            self.ids.debito.text = ""
            self.ids.anotacao.text = ""
            self.ids.alterar.disabled = True
            self.ids.remover.disabled = True
            self.ids.salvar.disabled = True
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?", [pesq])

        for id, data_criado, nome, cpf, telefone, endereco, cidade, uf, debito, anotacoes in cursor.fetchall():
            self.ids.nome.text = nome
            self.ids.cpf.text = cpf
            self.ids.telefone.text = telefone
            self.ids.endereco.text = endereco
            self.ids.cidade.text = cidade
            self.ids.uf.text = uf
            self.ids.debito.text = debito
            self.ids.anotacao.text = anotacoes
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
        disconectBD()

    def alterar_func(self):

        self.ids.nome.disabled = False
        self.ids.cidade.disabled = False
        self.ids.uf.disabled = False
        self.ids.telefone.disabled = False
        self.ids.endereco.disabled = False
        self.ids.anotacao.disabled = False
        self.ids.debito.disabled = False
        self.ids.salvar.disabled = False

    def remover_func(self):
        pesq = self.ids.pesq.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("delete from clientes where cpf = ?", [pesq])
        conn.commit()
        disconectBD()
        self.ids.nome.text = ""
        self.ids.cpf.text = ""
        self.ids.cidade.text = ""
        self.ids.uf.text = ""
        self.ids.telefone.text = ""
        self.ids.endereco.text = ""
        self.ids.debito.text = ""
        self.ids.anotacao.text = ""
        self.ids.alterar.disabled = True
        self.ids.remover.disabled = True
        self.ids.salvar.disabled = True

    def aplicar(self):
        pesq = self.ids.pesq.text
        nome = self.ids.nome.text
        telefone = self.ids.telefone.text
        endereco = self.ids.endereco.text
        cidade = self.ids.cidade.text
        uf = self.ids.uf.text
        debito = self.ids.debito.text
        anotacao = self.ids.anotacao.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""UPDATE clientes
                          SET nome = :nome, telefone = :telefone,
                          endereco = :endereco, cidade = :cidade,
                          uf = :uf, debito = :debito, anotacoes = :anotacao
                          where cpf = :cpf""",
                       {'nome': nome, 'telefone': telefone, 'endereco': endereco,
                        'cidade': cidade, 'uf': uf, 'debito': debito, 'anotacao': anotacao,
                        'cpf': pesq})
        conn.commit()

        cursor.execute("SELECT * FROM clientes WHERE cpf = ?", [pesq])
        for id, data_criado, nome, cpf, telefone, endereco, cidade, uf, debito, anotacoes in cursor.fetchall():
            self.ids.nome.text = nome
            self.ids.cpf.text = cpf
            self.ids.telefone.text = telefone
            self.ids.endereco.text = endereco
            self.ids.cidade.text = cidade
            self.ids.uf.text = uf
            self.ids.debito.text = debito
            self.ids.anotacao.text = anotacoes
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
        disconectBD()
        self.ids.nome.disabled = True
        self.ids.cidade.disabled = True
        self.ids.uf.disabled = True
        self.ids.telefone.disabled = True
        self.ids.endereco.disabled = True
        self.ids.anotacao.disabled = True
        self.ids.debito.disabled = True
        self.ids.salvar.disabled = True


#####     1.4 Tela     ##### FATLA
class RelatorioApp(Screen):

    def ver_relatorio_vendas(self):
        vendasTotal = 0
        dinheiroTotal = 0
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidosPagos")
        mostraPedidos = "\n"
        for numPedido, dia, mesa, pedido, valorTotal in cursor.fetchall():
            mostraPedidos += "Numero do Pedido: %s\n" % str(numPedido)
            mostraPedidos += "Data: %s\n" % str(dia)
            mostraPedidos += "Mesa: %s\n" % str(mesa)
            mostraPedidos += "Pedido:\n%s\n" % str(pedido)
            mostraPedidos += "Valor Total: %s\n" % str(valorTotal)
            mostraPedidos += "---------------------------\n"
            vendasTotal += 1
            dinheiroTotal += valorTotal
        disconectBD()
        self.ids.cardVendas.text = mostraPedidos
        vendasTotal = str(vendasTotal)
        self.ids.cardTotalVendas.text = vendasTotal
        dinheiroTotal = str(dinheiroTotal)
        self.ids.cardTotalDinheiro.text = dinheiroTotal

    def imprimir_relatorio(self):

        mes: int = dt.month
        ano: int = dt.year
        meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
                 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

        relatorio = self.ids.cardVendas.text
        numeroDeVendas = self.ids.cardTotalVendas.text
        dinheiroTotalEntrado = self.ids.cardTotalDinheiro.text

        bannerRelatorio = "POINT DO ESPETINHO\n" \
                          "ORG: José Filho e Leila Sousa\n" \
                          "--------------------------------------\n" \
                          "RELATÓRIO DE VENDAS MENSAL\n" \
                          f"MÊS CORRENTE AO RELATÓRIO: {meses[mes]} de {ano}\n" \
                          f"\nRELATÓRIO:\n{relatorio}\n" \
                          f"Número de Vendas: {numeroDeVendas}\n" \
                          f"Dinheiro Entrado: {dinheiroTotalEntrado} Reais\n" \
                          "--------------------------------------\n" \
                          "\nAPÓS GERAR O RELATORIO MENSAL, ENTRE EM CONATO COM O SUPORTE\n" \
                          "PARA REINICIAR O BANCO DE DADOS, PARA NÃO HAVER CONFLITO\n" \
                          "COM OS PRÓXIMOS RELATORIOS GERADOS.\n" \
                          "USE A GUIA DE SUPORTE DO PROGRAMA PARA ENTRAR EM CONTATO!\n"

        arq = open("C:/Users/ejrfl/Dropbox/bd_pointEsp/imprimir/relatorioMensal.txt", "w")
        assert isinstance(bannerRelatorio, object)
        arq.writelines(bannerRelatorio)
        arq.close()
        web.open("file:///C:/Users/ejrfl/Dropbox/bd_pointEsp/imprimir/relatorioMensal.txt")


#####     1.5 Tela     #####
class EstoqueApp(Screen):
    pass


#####     1.5.1 Tela     ##### FATLA
class EstoqueProdutosAdicionarApp(Screen):

    def cadastro_produto(self):
        nomeProduto = self.ids.nomeProduto.text
        codigoProduto = self.ids.codigoProduto.text
        descProduto = self.ids.descProduto.text
        quant = self.ids.quant.text
        anotacaoProduto = self.ids.anotacaoProduto.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO estoque (codigo, nome,descricao,quantidade, anotacao)
                          VALUES (?, ?, ?, ?, ?)""", (codigoProduto, nomeProduto, descProduto, quant, anotacaoProduto))
        conn.commit()
        disconectBD()
        self.ids.nomeProduto.text = ""
        self.ids.codigoProduto.text = ""
        self.ids.descProduto.text = ""
        self.ids.quant.text = ""
        self.ids.anotacaoProduto.text = ""


#####     1.5.2 Tela     ##### FATLA
class EstoqueProdutosAltDelApp(Screen):

    def pesq_produto(self):
        pesq = self.ids.pesqProduto.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (pesq,))

        for id, codigo, nome, descricao, quantidade, anotacao in cursor.fetchall():
            quantidade = str(quantidade)
            self.ids.nomeProduto.text = nome
            self.ids.codigoProduto.text = codigo
            self.ids.descProduto.text = descricao
            self.ids.quant.text = quantidade
            self.ids.anotacaoProduto.text = anotacao
            self.ids.alterar.disabled = False
            self.ids.remover.disabled = False
        disconectBD()

    def alterar_produto(self):
        self.ids.nomeProduto.disabled = False
        self.ids.descProduto.disabled = False
        self.ids.quant.disabled = False
        self.ids.anotacaoProduto.disabled = False
        self.ids.salvar.disabled = False

    def aplicar(self):
        codigo = self.ids.codigoProduto.text
        nome = self.ids.nomeProduto.text
        descricao = self.ids.descProduto.text
        quantidade = self.ids.quant.text
        anotacao = self.ids.anotacaoProduto.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("""UPDATE estoque SET nome = :nome, descricao = :descricao, quantidade = :quantidade,
                        anotacao = :anotacao WHERE codigo = :codigo""",
                       {'nome': nome, 'descricao': descricao, 'quantidade': quantidade, 'anotacao': anotacao,
                        'codigo': codigo})
        conn.commit()

        pesq = self.ids.pesqProduto.text
        cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (pesq,))

        for id, codigo, nome, descricao, quantidade, anotacao in cursor.fetchall():
            quantidade = str(quantidade)
            self.ids.nomeProduto.text = nome
            self.ids.codigoProduto.text = codigo
            self.ids.descProduto.text = descricao
            self.ids.quant.text = quantidade
            self.ids.anotacaoProduto.text = anotacao
        disconectBD()
        self.ids.alterar.disabled = False
        self.ids.remover.disabled = False
        self.ids.salvar.disabled = True
        self.ids.nomeProduto.disabled = True
        self.ids.descProduto.disabled = True
        self.ids.quant.disabled = True
        self.ids.anotacaoProduto.disabled = True

    def remover_produto(self):
        pesq = self.ids.pesqProduto.text
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estoque WHERE codigo = ?", (pesq,))
        conn.commit()
        disconectBD()
        self.ids.nomeProduto.text = ""
        self.ids.codigoProduto.text = ""
        self.ids.descProduto.text = ""
        self.ids.quant.text = ""
        self.ids.anotacaoProduto.text = ""
        self.ids.remover.disabled = True
        self.ids.alterar.disabled = True
        self.ids.salvar.disabled = True


#####     1.5.3 Tela     #####
class EstoqueProdutosVisualizarApp(Screen):

    def ver_estoque(self):
        conn = sql.connect(urlBD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estoque")
        estoque = ""
        for id, codigo, nome, descricao, quantidade, anotacao in cursor.fetchall():
            estoque = f"CODIGO: {codigo} | NOME: {nome} | QUANTIDADE: {quantidade}\n"
            estoque += "-" * 100 + "\n"
        self.ids.card.text = estoque
        disconectBD()


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
