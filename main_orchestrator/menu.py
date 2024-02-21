import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from llm_agent import LLMApp
from img_gen import ImageGenWidget
from discord import DiscordWidget

class MenuPage(QWidget):
    def __init__(self):
        super(MenuPage, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Menu Page')
        self.setGeometry(100, 100, 400, 400)  # Adjusted initial size

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # Set spacing between buttons

        self.stacked_widget = QStackedWidget()

        curie_button = QPushButton('CURIE')
        curie_button.clicked.connect(self.show_curie_widget)
        main_layout.addWidget(curie_button)

        img_gen_button = QPushButton('Image Gen')
        img_gen_button.clicked.connect(self.show_img_gen_widget)
        main_layout.addWidget(img_gen_button)

        discord_button = QPushButton('Discord')
        discord_button.clicked.connect(self.show_discord_widget)
        main_layout.addWidget(discord_button)

        self.setLayout(main_layout)

    def show_curie_widget(self):
        curie_widget = LLMApp()
        curie_widget.setFixedSize(400, 900)  # Set the fixed size
        self.stacked_widget.addWidget(curie_widget)
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.show()

    def show_img_gen_widget(self):
        img_gen_widget = ImageGenWidget()
        img_gen_widget.setFixedSize(400,900)  # Set the fixed size
        self.stacked_widget.addWidget(img_gen_widget)
        self.stacked_widget.setCurrentIndex(1)
        self.stacked_widget.show()

    def show_discord_widget(self):
        discord_widget = DiscordWidget()
        discord_widget.setFixedSize(400,900)  # Set the fixed size
        self.stacked_widget.addWidget(discord_widget)
        self.stacked_widget.setCurrentIndex(2)
        self.stacked_widget.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu_page = MenuPage()
    menu_page.show()
    sys.exit(app.exec_())
