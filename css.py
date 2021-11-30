"""Nesse arquivo se encontram todos os padrões de cores utilizados para botões, backgrounds e etcs."""
from PyQt5 import QtCore, QtWidgets, QtGui


class css:
    wallpaper = """
                    font: 75 10pt "Microsoft YaHei UI";
                    background-image: url(r'\assets\icons\back.png);
                    """
    default = """
                color: #FFFFFF;
                font: 75 10pt "Microsoft YaHei UI";
                """
    blueish = """
                background-color: #336B87;
                """
    blueish_main = """
                InterfacePrincipal {
                background-color: #336B87;
                background-image: url(Xaropinho.png);
                background-position: center;
                background-repeat: no-repeat;
                }
                """
    blueish_text = """
                color: #FFFFFF;
                font-family: Comic Sans MS;
                font-seize: 15px;
                """
    blueish_label = """
                color: #FFFFFF;
                font-family: Comic Sans MS;
                font: bold 15px;
                background-color: #90AFC5;
                border-width: 2px;
                border-radius: 10px;
                font-size: 15px;
                """


class animacao(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(60, 60)

        self.color1 = QtGui.QColor(240, 53, 218)
        self.color2 = QtGui.QColor(61, 217, 245)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:21px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)
