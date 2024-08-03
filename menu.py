import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, 
    QLabel, QSlider, QComboBox, QPushButton, QStackedWidget, QColorDialog, 
    QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PyQt5.QtGui import QColor, QFont, QKeySequence

# tela de carregamento pra fakear
class TelaCarregamento(QWidget):
    def __init__(self, classe_principal):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(400, 500)

        self.classe_principal = classe_principal

        self.setStyleSheet("background-color: #1d1d1d;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.rotulo_carregamento = QLabel("Loading fortnite external 📗")
        self.rotulo_carregamento.setAlignment(Qt.AlignCenter)
        self.rotulo_carregamento.setStyleSheet("font: 22pt 'Segoe UI'; color: #ffffff;")
        layout.addWidget(self.rotulo_carregamento)
        
        self.setLayout(layout)
        
        self.animacao_fade_out()

    def animacao_fade_out(self):
        animacao = QPropertyAnimation(self, b"windowOpacity")
        animacao.setDuration(5000)
        animacao.setStartValue(1.0)
        animacao.setEndValue(0.0)
        animacao.setEasingCurve(QEasingCurve.InOutQuad)
        animacao.start()
        QTimer.singleShot(5000, self.exibir_janela_principal)

    def exibir_janela_principal(self):
        self.close()
        self.janela_principal = self.classe_principal()
        self.janela_principal.show()

class AplicativoAssistenteDeMira(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(500, 500)
        self.cor_destaque = "#393939"

        self.atualizar_estilo()

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.bar_titulo = QLabel("aqui ficaria o nick do aspecty la tlg")
        self.bar_titulo.setAlignment(Qt.AlignCenter)
        self.bar_titulo.setStyleSheet("font: 14pt 'Segoe UI'; color: #ffffff; padding: 10px;")
        layout_principal.addWidget(self.bar_titulo)
        self.animar_titulo()

        layout_navegacao = QHBoxLayout()
        layout_navegacao.setContentsMargins(10, 10, 10, 10)
        layout_navegacao.setSpacing(10)
        
        for texto in ["Aim", "Visuals", "Customize"]:
            botao = QPushButton(texto)
            botao.clicked.connect(self.mudar_pagina(texto))
            layout_navegacao.addWidget(botao)
        
        self.widget_navegacao = QWidget()
        self.widget_navegacao.setLayout(layout_navegacao)
        layout_principal.addWidget(self.widget_navegacao)

        self.widget_empilhado = QStackedWidget()
        layout_principal.addWidget(self.widget_empilhado)

        self.criar_paginas()

        self.aguardando_tecla = False

        self.esta_arrastando = False
        self.posicao_arraste = QPoint()

    def animar_titulo(self):
        pass

    def atualizar_estilo(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #1d1d1d;
            }}
            QLabel {{
                color: #ffffff;
                font: 12pt 'Calibri';
            }}
            QCheckBox {{
                color: #ffffff;
                font: 12pt 'Calibri';
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                background-color: #5c5c5c;
                border: 2px solid {self.cor_destaque};
                border-radius: 5px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.cor_destaque};
                border: 2px solid #ffffff;
                border-radius: 5px;
            }}
            QCheckBox::indicator:hover {{
                background-color: {self.cor_destaque};
            }}
            QSlider::groove:horizontal {{
                height: 10px;
                background: #5c5c5c;
                border-radius: 5px;
            }}
            QSlider::handle:horizontal {{
                background: {self.cor_destaque};
                width: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }}
            QSlider::sub-page:horizontal {{
                background: {self.cor_destaque};
                border-radius: 5px;
            }}
            QComboBox {{
                background-color: #5c5c5c;
                color: #ffffff;
                font: 12pt 'Calibri';
            }}
            QPushButton {{
                background-color: {self.cor_destaque};
                color: #ffffff;
                font: 12pt 'Calibri';
                border: 2px solid #5c5c5c;
                border-radius: 10px; /* Bordas arredondadas */
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #5c5c5c;
                border: 2px solid {self.cor_destaque};
            }}
            QRadioButton {{
                color: #ffffff;
                font: 12pt 'Calibri';
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:checked {{
                background-color: {self.cor_destaque};
                border: 2px solid #ffffff;
                border-radius: 10px;
            }}
            QRadioButton::indicator:unchecked {{
                background-color: #5c5c5c;
                border: 2px solid {self.cor_destaque};
                border-radius: 10px;
            }}
        """)

    def criar_paginas(self):
        # pagina Aim
        pagina_aim = QWidget()
        layout_aim = QVBoxLayout(pagina_aim)
        layout_aim.setContentsMargins(10, 10, 10, 10)
        layout_aim.setSpacing(10)

        self.criar_botao_toggle(layout_aim, "Enable Aim")
        self.criar_botao_toggle(layout_aim, "Visible Check")
        self.criar_botao_toggle(layout_aim, "Show FOV")

        self.criar_slider_com_rotulo(layout_aim, "FOV", 0, 100)
        self.criar_slider_com_rotulo(layout_aim, "Smooth", 0, 10)  

        # ops de Aim
        layout_opcoes_aim = QHBoxLayout()
        self.grupo_aim = QButtonGroup(self)
        for texto in ["Head", "Body", "Legs"]:
            botao = QRadioButton(texto)
            self.grupo_aim.addButton(botao)
            layout_opcoes_aim.addWidget(botao)
        
        layout_aim.addLayout(layout_opcoes_aim)

        layout_tecla_aim = QHBoxLayout()
        rotulo_tecla_aim = QLabel("Aim Key:")
        self.botao_tecla_aim = QPushButton("coded by xsxs000")
        self.botao_tecla_aim.clicked.connect(self.trocar_selecao_tecla_aim)
        layout_tecla_aim.addWidget(rotulo_tecla_aim)
        layout_tecla_aim.addWidget(self.botao_tecla_aim)
        layout_aim.addLayout(layout_tecla_aim)
        
        self.widget_empilhado.addWidget(pagina_aim)

        # pagina Visuals
        pagina_visuals = QWidget()
        layout_visuals = QVBoxLayout(pagina_visuals)
        layout_visuals.setContentsMargins(10, 10, 10, 10)
        layout_visuals.setSpacing(10)

        # bgl la de elemento visual
        self.criar_botao_toggle(layout_visuals, "Box ESP")
        self.criar_botao_toggle(layout_visuals, "Skeleton ESP")
        self.criar_botao_toggle(layout_visuals, "Distance ESP")
        self.criar_botao_toggle(layout_visuals, "Snaplines")
        self.criar_botao_toggle(layout_visuals, "View Angle")
        self.criar_botao_toggle(layout_visuals, "Name ESP")
        self.criar_botao_toggle(layout_visuals, "Weapon ESP")

        self.criar_slider_com_rotulo(layout_visuals, "Angle", 0, 360)

        self.widget_empilhado.addWidget(pagina_visuals)

        # Página Personalização
        pagina_personalizacao = QWidget()
        layout_personalizacao = QVBoxLayout(pagina_personalizacao)
        layout_personalizacao.setContentsMargins(10, 10, 10, 10)
        layout_personalizacao.setSpacing(10)

        self.botao_cor = QPushButton("Change Menu Color")
        self.botao_cor.clicked.connect(self.abrir_dialogo_cor)
        layout_personalizacao.addWidget(self.botao_cor)

        self.widget_empilhado.addWidget(pagina_personalizacao)

    def criar_botao_toggle(self, layout, texto):
        botao = QCheckBox(texto)
        layout.addWidget(botao)

    def criar_slider_com_rotulo(self, layout, texto_rotulo, valor_minimo, valor_maximo):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(valor_minimo)
        slider.setMaximum(valor_maximo)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setValue(valor_minimo)

        rotulo_slider = QLabel(f"{texto_rotulo}: {valor_minimo}")
        slider.valueChanged.connect(lambda valor: rotulo_slider.setText(f"{texto_rotulo}: {valor}"))

        layout.addWidget(rotulo_slider)
        layout.addWidget(slider)

    def mudar_pagina(self, nome_pagina):
        def _mudar_pagina():
            if nome_pagina == "Aim":
                self.widget_empilhado.setCurrentIndex(0)
            elif nome_pagina == "Visuals":
                self.widget_empilhado.setCurrentIndex(1)
            elif nome_pagina == "Customize":
                self.widget_empilhado.setCurrentIndex(2)
        return _mudar_pagina

    def abrir_dialogo_cor(self):
        cor = QColorDialog.getColor()
        if cor.isValid():
            self.cor_destaque = cor.name()
            self.atualizar_estilo()

    def trocar_selecao_tecla_aim(self):
        if not self.aguardando_tecla:
            self.aguardando_tecla = True
            self.botao_tecla_aim.setText("Press any key...")
            self.installEventFilter(self)
        else:
            self.aguardando_tecla = False
            self.botao_tecla_aim.setText("coded by xsxs000")
            self.removeEventFilter(self)

    def eventFilter(self, obj, evento):
        if self.aguardando_tecla and evento.type() == evento.KeyPress:
            tecla = evento.key()
            if tecla == Qt.Key_Left:
                self.botao_tecla_aim.setText("Left Arrow")
            elif tecla == Qt.Key_Right:
                self.botao_tecla_aim.setText("Right Arrow")
            elif tecla == Qt.Key_Up:
                self.botao_tecla_aim.setText("Up Arrow")
            elif tecla == Qt.Key_Down:
                self.botao_tecla_aim.setText("Down Arrow")
            elif tecla == Qt.Key_Space:
                self.botao_tecla_aim.setText("Space")
            else:
                sequencia_tecla = QKeySequence(tecla)
                self.botao_tecla_aim.setText(sequencia_tecla.toString())
            
            self.aguardando_tecla = False
            self.removeEventFilter(self)
            return True
        return super().eventFilter(obj, evento)

    def mousePressEvent(self, evento):
        if evento.button() == Qt.LeftButton:
            self.esta_arrastando = True
            self.posicao_arraste = evento.globalPos() - self.frameGeometry().topLeft()
            evento.accept()

    def mouseMoveEvent(self, evento):
        if self.esta_arrastando:
            self.move(evento.globalPos() - self.posicao_arraste)
            evento.accept()

    def mouseReleaseEvent(self, evento):
        if evento.button() == Qt.LeftButton:
            self.esta_arrastando = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_carregamento = TelaCarregamento(AplicativoAssistenteDeMira)
    tela_carregamento.show()
    sys.exit(app.exec_())
