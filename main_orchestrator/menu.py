import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from llm_agent import LLMApp
from img_gen import ImageGenWidget
from discord import DiscordWidget

class SinglePageApp(QWidget):
    def __init__(self):
        super(SinglePageApp, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Single Page App')
        self.setGeometry(100, 100, 400, 900)

        main_layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        curie_widget = LLMApp()
        img_gen_widget = ImageGenWidget()
        discord_widget = DiscordWidget()

        self.stacked_widget.addWidget(curie_widget)
        self.stacked_widget.addWidget(img_gen_widget)
        self.stacked_widget.addWidget(discord_widget)

        curie_button = QPushButton('CURIE')
        curie_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        main_layout.addWidget(curie_button)

        img_gen_button = QPushButton('Image Gen')
        img_gen_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        main_layout.addWidget(img_gen_button)

        discord_button = QPushButton('Discord')
        discord_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        main_layout.addWidget(discord_button)

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    spa = SinglePageApp()
    spa.show()
    sys.exit(app.exec_())
