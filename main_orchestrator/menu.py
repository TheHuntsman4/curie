import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from llm_agent import LLMApp
from img_gen import ImageGenWidget
from discord import DiscordWidget

class ButtonWidget(QWidget):
    def __init__(self, stacked_widget):
        super(ButtonWidget, self).__init__()

        self.init_ui(stacked_widget)

    def init_ui(self, stacked_widget):
        button_layout = QVBoxLayout(self)

        curie_button = QPushButton('CURIE')
        curie_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        button_layout.addWidget(curie_button)

        img_gen_button = QPushButton('Image Gen')
        img_gen_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
        button_layout.addWidget(img_gen_button)

        discord_button = QPushButton('Discord')
        discord_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))
        button_layout.addWidget(discord_button)

class SinglePageApp(QWidget):
    def __init__(self):
        super(SinglePageApp, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Single Page App')
        self.setGeometry(100, 100, 400, 900)

        main_layout = QVBoxLayout(self)

        self.stacked_widget = QStackedWidget()

        # Create the button widget and add it to the stacked widget
        button_widget = ButtonWidget(self.stacked_widget)
        self.stacked_widget.addWidget(button_widget)

        curie_widget = LLMApp()
        img_gen_widget = ImageGenWidget()
        discord_widget = DiscordWidget()

        self.stacked_widget.addWidget(curie_widget)
        self.stacked_widget.addWidget(img_gen_widget)
        self.stacked_widget.addWidget(discord_widget)

        main_layout.addWidget(self.stacked_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    spa = SinglePageApp()
    spa.show()
    sys.exit(app.exec_())
