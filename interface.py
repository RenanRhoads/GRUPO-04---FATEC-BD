import os
from PyQt5 import QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import QRunnable, Qt
from matplotlib import pyplot as plt
from covid import tracker
from PyQt5.QtWidgets import *
from datetime import date, timedelta
from PyQt5.QtGui import QImage, QPixmap, QCursor, QPalette, QColor
from matplotlib.figure import Figure
from css import css
import requests
import shutil
import gzip
import logging
import sys
import random
import threading
import seaborn as sns
import tkinter as tk

# código simples para verificar o tamanho da tela do usuário.
root = tk.Tk()

_x = 1280  # root.winfo_screenwidth()
_y = 720  # root.winfo_screenheight()


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)

        local = os.path.dirname(os.path.abspath(__file__))  # Identicia o caminho atual onde o programa está rodando.
        url_git = local + r'\assets\icons\github.png'

        self.resize(400, 200)

        self.gitmage = QImage()

        self.image_git_label = QLabel(self)
        self.github = QPixmap(url_git)
        self.image_git_label.setPixmap(self.github)
        self.image_git_label.show()

        self.texto_help = QLabel(self)
        self.texto_help.setOpenExternalLinks(True)
        self.texto_help.setText(
            '''<a href='https://github.com/RenanRhoads/GRUPO-04---FATEC-BD'>Covid Tracker - Github</a>''')

        l = QGridLayout()
        l.addWidget(self.texto_help, 1, 2)
        l.addWidget(self.image_git_label, 1, 1)
        self.setLayout(l)


class Updating(QRunnable):
    """Função para atualizar os dados do programa."""

    def __init__(self, n):
        super().__init__()

    def atualizar(self):
        logging.info(f"Trabalhando no processo")
        path = os.path.expanduser('~\Documents\caso_full.csv.gz')
        output = os.path.expanduser('~\Documents\caso_full.csv')
        url = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'  # link para o arquivo fornecido pelo site Brasil.IO
        r = requests.get(url, allow_redirects=True)

        with open(path, 'wb') as f:
            f.write(r.content)
            logging.info("Main    : Inicializando a thread para atualizar o arquivo.")
            """Após o download do arquivo, salva na pasta documentos"""

        with gzip.open(path, 'rb') as f_in:
            with open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            """Extrai o arquivo da fila .GZ na pasta Documentos do usuário"""
            logging.info("Main    : Download e extração finalizados.")


class Window(QDialog):
    ano_selected: str
    cidade_selected: str

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setFixedSize(_x, _y)
        self.figure = plt.figure()

        # transforma o gráfico em uma figure.
        self.canvas = FigureCanvas(self.figure)

        # abaixo, opção de zoom e salvar uma imagem do gráfico.
        self.toolbar = NavigationToolbar(self.canvas, self)

        # botão que ativa a função plot, apenas para testes
        self.button = QPushButton('Gráfico por Mês (Selecione a opção "Todos" no filtro de Mês)')
        self.button.clicked.connect(self.item_usuario)

        self.hello = "Seja bem-vindo ao Covid Tracker!"
        self.select_texto = "Digite o nome de sua cidade:"
        self.texto = QLabel(self.hello, self)

        self.data = str(date.today().strftime("%d/%m/%Y"))

        self.data_less_1 = date.today() - timedelta(days=1)
        self.data_string = self.data_less_1.strftime("%y-%m-%d")

        self.atualizarButton = QPushButton(self)
        self.atualizarButton.clicked.connect(self.atualizar_dados)
        self.atualizarButton.setText("Atualizar dados.")
        self.grafButton = QPushButton(self)
        self.grafButton.clicked.connect(self.showGraf)
        self.grafButton.setText("Top 10 cidades")

        self.lista_header = QLabel(self.select_texto, self)

        self.lista = QComboBox(self)
        self.i = 0
        self.j = len(tracker.lista_cidades)

        while self.i < self.j:  # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1
        self.lista.setEditable(True)
        self.lista.resize(104, 22)

        self.lista_ano = QComboBox(self)
        self.r = 0
        self.s = len(tracker.lista_ano)

        while self.r < self.s:
            self.lista_ano.addItem(tracker.lista_ano[self.r])
            self.r += 1

        self.lista_ano.setEditable(False)

        self.lista_meses = QComboBox(self)
        self.a = 0
        self.b = len(tracker.lista_meses)

        while self.a < self.b:
            self.lista_meses.addItem(tracker.lista_meses[self.a])
            self.a += 1

        self.lista_meses.move(1163, 34)
        self.lista_meses.resize(104, 22)
        self.lista_meses.setEditable(False)

        self.cidade = self.lista.currentText()
        self.ano = self.lista_ano.currentText()
        self.mes = self.lista_meses.currentText()

        self.valor_cidade = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['ano'] == int(self.ano)].sum()

        """Filtro se altera com base na cidade que o usuário seleciona"""
        self.valor_dia = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].iloc[-1].sum()

        """Calcula a data atual - 1 para saber a quantidade de novas mortes """

        self.valor_mortes_sp = tracker.df['mortes'].sum()

        """ Total de óbitos no estado de São Paulo"""

        self.valor_total_confirmados = tracker.df['confirmados'].sum()

        """Total de casos confirmados no estado de São Paulo"""

        self.mortes = QLabel("Número total de mortes: " + str(self.valor_cidade), self)
        self.mortes_dia = QLabel("Novas mortes: " + str(self.valor_dia), self)
        self.mortes_sp = QLabel("Total de óbitos no estado de São Paulo: " + str(self.valor_mortes_sp), self)
        self.total_confirmados = QLabel(
            "Total de casos confirmados no estado de São Paulo: " + str(self.valor_total_confirmados), self)

        """Taxa de letalidade"""
        valor_letalidade = ((tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
                                 tracker.df['tipo'] == 'city'].loc[tracker.df['ano'] == int(self.ano)].sum()) * 100) / \
                           (tracker.df['confirmados'].loc[tracker.df['cidade'] == self.cidade].loc[tracker.df['tipo'] ==
                                                                                                   'city'].loc[
                                tracker.df['ano'] == int(self.ano)].sum())
        self.valor_taxa_letalidade = (f'{valor_letalidade:.2f}')
        self.letalidade = QLabel(f"Letalidade: {str(self.valor_taxa_letalidade)}%", self)

        """
        Botões com funções
        """
        self.lista.activated.connect(self.item_usuario)
        self.lista_ano.activated.connect(self.item_usuario)
        self.lista_meses.activated.connect(self.item_usuario)

        self.HelpButton = QPushButton(self)
        self.HelpButton.setText("Créditos")
        self.HelpButton.clicked.connect(self.extrawindow)

        outerLayout = QVBoxLayout()
        # Create a form layout for the label and line edit
        topLayout = QHBoxLayout()
        # Add a label and a line edit to the form layout
        # Create a layout for the checkboxes
        optionsLayout = QGridLayout()
        # Add some checkboxes to the layout
        optionsLayout.addWidget(self.texto)
        optionsLayout.addWidget(self.toolbar)
        optionsLayout.addWidget(self.canvas)
        optionsLayout.addWidget(self.button)
        optionsLayout.addWidget(self.atualizarButton)
        optionsLayout.addWidget(self.grafButton)
        optionsLayout.addWidget(self.lista_header, 0, 1)
        optionsLayout.addWidget(self.lista, 1, 1)
        optionsLayout.addWidget(self.lista_ano, 1, 2)
        optionsLayout.addWidget(self.mortes_dia, 3, 1)
        optionsLayout.addWidget(self.mortes, 4, 1)
        optionsLayout.addWidget(self.letalidade, 4, 2)
        optionsLayout.addWidget(self.mortes_sp, 5, 1)
        optionsLayout.addWidget(self.total_confirmados, 6, 1)
        optionsLayout.addWidget(self.HelpButton, 6, 2)
        # Nest the inner layouts into the outer layout
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(optionsLayout)
        # Set the window's main layout
        self.setLayout(outerLayout)

    def item_usuario(self):

        self.cidade_selected = self.lista.currentText()
        self.ano_selected = self.lista_ano.currentText()
        self.mes_selected = self.lista_meses.currentText()

        self.concat = self.cidade_selected + self.mes_selected + str(self.ano_selected)

        if self.mes_selected == 'Todos':

            self.valor_cidade_selected = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
                tracker.df['tipo'] == 'city'].loc[tracker.df['ano'] == int(self.ano_selected)].sum()

            valor_letalidade = ((tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
                                     tracker.df['tipo'] == 'city'].loc[
                                     tracker.df['ano'] == int(self.ano_selected)].sum()) * 100) / \
                               (tracker.df['confirmados'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
                                    tracker.df['tipo'] ==
                                    'city'].loc[tracker.df['ano'] == int(self.ano_selected)].sum())
            self.valor_taxa_letalidade = f'{valor_letalidade:.2f}'

            # Realiza a filtragem de acordo com a cidade selecionada.
            self.letalidade.setText(f"Letalidade: {str(self.valor_taxa_letalidade)}%")

            self.mortes.setText("Número total de Mortes: " + str(int(self.valor_cidade_selected)))
            """Altera o valor dos números de mortes que podemos ver."""
        else:

            self.valor_cidade_selected = tracker.df['mortes'].loc[tracker.df['chave'] == self.concat].sum()

            valor_letalidade = ((tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
                                     tracker.df['tipo'] == 'city'].loc[
                                     tracker.df['ano'] == int(self.ano_selected)].sum()) * 100) / \
                               (tracker.df['confirmados'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
                                    tracker.df['tipo'] ==
                                    'city'].loc[tracker.df['ano'] == int(self.ano_selected)].sum())
            self.valor_taxa_letalidade = f'{valor_letalidade:.2f}'

            # Realiza a filtragem de acordo com a cidade selecionada.
            self.letalidade.setText(f"Letalidade: {str(self.valor_taxa_letalidade)}%")
            self.mortes.setText("Número total de Mortes: " + str(int(self.valor_cidade_selected)))

        plt.clf()  # vai limpar o gráfico anterior para que não gere um em cima do outro.

        user_select_city = self.cidade_selected
        city_sel = user_select_city
        user_select_year = self.ano_selected
        ano_sel = user_select_year
        user_select_month = self.mes_selected
        mes_sel = user_select_month

        concat = city_sel + mes_sel + str(ano_sel)

        if mes_sel == "Todos":
            cidade_sel = tracker.df[tracker.df.cidade == str(city_sel)].loc[tracker.df.ano == int(ano_sel)]

            # Gráfico por mês da cidade selecionada
            sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
            ax = self.figure.add_subplot(111)
            sns.set_color_codes("pastel")
            sns.barplot(x="mes_nome", y="mortes", data=cidade_sel,
                        color="b", ci=None, estimator=sum)
            # Configurando título e rótulos dos eixos.
            plt.title('Evolução de morte por mês em ' + str(ano_sel), fontsize=9)
            plt.xlabel('Mês', fontsize=9)
            plt.ylabel('Mortes', fontsize=9)
            for container in ax.containers:
                ax.bar_label(container)
            ax.plot()
            self.canvas.draw()
        elif mes_sel != "Todos":

            if concat not in tracker.df.values:

                cidade_sel = tracker.df.loc[tracker.df.chave == 'São Paulonovembro2021']
                # Gráfico por mês da cidade selecionada
                sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
                ax = self.figure.add_subplot(111)
                sns.set_color_codes("pastel")
                sns.barplot(x="dia", y="mortes", data=cidade_sel,
                            color="b", ci=None, estimator=sum)
                # Configurando título e rótulos dos eixos.
                plt.title(
                    'Operação impossível, talvez os dados selecionados não exista no Dataset fornecido pela Brasil.io',
                    fontsize=9)
                plt.xlabel('Mês', fontsize=9)
                plt.ylabel('Mortes', fontsize=9)
                for container in ax.containers:
                    ax.bar_label(container)
                ax.plot()
                self.canvas.draw()
            else:
                cidade_sel = tracker.df.loc[tracker.df.chave == concat]
                # Gráfico por mês da cidade selecionada
                sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
                ax = self.figure.add_subplot(111)
                sns.set_color_codes("pastel")
                sns.barplot(x="dia", y="mortes", data=cidade_sel,
                            color="b", ci=None, estimator=sum)
                # Configurando título e rótulos dos eixos.
                plt.title('Mortes em ' + str(mes_sel) + " de " + str(ano_sel), fontsize=9)
                plt.xlabel('Mês', fontsize=9)
                plt.ylabel('Mortes', fontsize=9)
                for container in ax.containers:
                    ax.bar_label(container)
                ax.plot()
                self.canvas.draw()

    def atualizar_dados(self):
        formato = "%(asctime)s: %(message)s"
        logging.basicConfig(format=formato, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : Inicializando a thread para atualizar o arquivo.")
        x = threading.Thread(target=Updating.atualizar, args=(1,))
        x.start()

    def showGraf(self):

        plt.clf()

        sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
        sns.set(rc={'figure.figsize': (11.7, 8.27)})
        ax = self.figure.add_subplot(111)

        ax.clear()
        sns.set_color_codes("pastel")
        sns.barplot(x="mortes", y="cidade", data=tracker.df,
                    label="Total", color="b", estimator=sum, ci=None, order=tracker.total_mortes_cidade.index)

        # Configurando título e rótulos dos eixos.
        plt.title('Total de mortes', fontsize=19)
        plt.xlabel('Mortes', fontsize=9)
        plt.ylabel('Cidades', fontsize=9)
        for container in ax.containers:
            ax.bar_label(container)
        ax.plot()
        self.canvas.draw()

    def extrawindow(self):
        self.w = HelpWindow()
        self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.setWindowTitle('CovidTracker')
    main.show()
    app.setStyle('Fusion')

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(dark_palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    sys.exit(app.exec_())
