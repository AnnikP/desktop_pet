import sys
import random
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMenu, QAction
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QMovie, QCursor


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        # === Window setup ===
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # === Pet sprite ===
        self.label = QLabel(self)
        self.movie = QMovie("pet_idle.gif")  # replace with your sprite
        self.label.setMovie(self.movie)
        self.movie.start()

        # === Position and size ===
        self.resize(128, 128)
        self.move(300, 800)  # near bottom of screen
        self.pet_name = "Mochi"

        # === Movement ===
        self.direction = random.choice([-1, 1])
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_pet)
        self.timer.start(50)  # update every 50ms

        # === States ===
        self.dialogue = QLabel(self)
        self.dialogue.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 8px;
                padding: 4px;
                font-family: Arial;
                font-size: 10pt;
            }
        """)
        self.dialogue.hide()

    # === Movement logic ===
    def move_pet(self):
        pos = self.pos()
        new_x = pos.x() + (2 * self.direction)
        screen_width = QApplication.primaryScreen().size().width()

        # bounce at edges
        if new_x <= 0 or new_x + self.width() >= screen_width:
            self.direction *= -1

        self.move(new_x, pos.y())

    # === Right-click menu ===
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        feed_action = QAction("Feed 🍪", self)
        talk_action = QAction("Talk 💬", self)
        exit_action = QAction("Exit ❌", self)

        feed_action.triggered.connect(self.feed_pet)
        talk_action.triggered.connect(self.talk_pet)
        exit_action.triggered.connect(QApplication.quit)

        menu.addAction(feed_action)
        menu.addAction(talk_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        menu.exec(QCursor.pos())

    # === Pet interactions ===
    def feed_pet(self):
        self.show_dialogue("Yum! Thanks for the treat!")

    def talk_pet(self):
        responses = [
            "Hi there!",
            "I’m just walking around 🐾",
            "Feeling happy today!",
            "Want to listen to music?",
            "Let’s set a timer soon!"
        ]
        self.show_dialogue(random.choice(responses))

    # === Dialogue display ===
    def show_dialogue(self, text):
        self.dialogue.setText(text)
        self.dialogue.adjustSize()
        self.dialogue.move(10, -30)
        self.dialogue.show()

        # Hide after 2 seconds
        QTimer.singleShot(2000, self.dialogue.hide)


# === App entry point ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())

