import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QDrag
from PyQt6.QtCore import Qt, QMimeData, QByteArray

class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Bắt đầu quá trình kéo thả
            drag = QDrag(self)
            mime_data = QMimeData()

            # Chuyển tên file hình ảnh thành dữ liệu
            mime_data.setData('application/x-pixmap', QByteArray(self.toolTip().encode()))
            drag.setMimeData(mime_data)

            # Hiển thị ảnh đại diện khi kéo thả
            drag.setPixmap(self.pixmap())
            drag.exec(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-pixmap'):
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Xử lý khi một lá bài được thả
        data = event.mimeData().data('application/x-pixmap').data().decode()

        # Cập nhật ảnh cho QLabel này khi thả vào
        pixmap = QPixmap(f'path_to_folder/{data}')
        self.setPixmap(pixmap.scaled(100, 150))

        # Gắn lại tooltip với đường dẫn file ảnh
        self.setToolTip(data)

        event.acceptProposedAction()


class PokerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mậu Binh - Kéo và Thả")
        self.setGeometry(100, 100, 800, 600)

        # Layout chính để chứa các hàng bài
        self.main_layout = QVBoxLayout()

        # Nút xáo bài
        self.shuffle_button = QPushButton("Xáo Bài")
        self.shuffle_button.clicked.connect(self.deal_cards)
        self.main_layout.addWidget(self.shuffle_button)

        # Layout cho 3 hàng bài (hàng 1: 3 lá, hàng 2 & 3: 5 lá)
        self.row_layouts = [QHBoxLayout() for _ in range(3)]
        for row_layout in self.row_layouts:
            self.main_layout.addLayout(row_layout)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Căn lề trái cho mỗi hàng

        # Tạo danh sách label để chứa các lá bài có thể kéo thả
        self.card_labels = [DraggableLabel(self) for _ in range(13)]
        
        # Thêm các label vào từng hàng theo quy tắc mậu binh
        for i in range(3):
            self.row_layouts[0].addWidget(self.card_labels[i])  # Hàng đầu (3 lá)
        for i in range(3, 8):
            self.row_layouts[1].addWidget(self.card_labels[i])  # Hàng thứ hai (5 lá)
        for i in range(8, 13):
            self.row_layouts[2].addWidget(self.card_labels[i])  # Hàng thứ ba (5 lá)

        self.setLayout(self.main_layout)

        # Danh sách tên các quân bài
        self.cards = [
            '2_bich.jpg', '2_co.jpg', '2_ro.jpg', '2_tep.jpg',
            '3_bich.jpg', '3_co.jpg', '3_ro.jpg', '3_tep.jpg',
            '4_bich.jpg', '4_co.jpg', '4_ro.jpg', '4_tep.jpg',
            '5_bich.jpg', '5_co.jpg', '5_ro.jpg', '5_tep.jpg',
            '6_bich.jpg', '6_co.jpg', '6_ro.jpg', '6_tep.jpg',
            '7_bich.jpg', '7_co.jpg', '7_ro.jpg', '7_tep.jpg',
            '8_bich.jpg', '8_co.jpg', '8_ro.jpg', '8_tep.jpg',
            '9_bich.jpg', '9_co.jpg', '9_ro.jpg', '9_tep.jpg',
            '10_bich.jpg', '10_co.jpg', '10_ro.jpg', '10_tep.jpg',
            'J_bich.jpg', 'J_co.jpg', 'J_ro.jpg', 'J_tep.jpg',
            'Q_bich.jpg', 'Q_co.jpg', 'Q_ro.jpg', 'Q_tep.jpg',
            'K_bich.jpg', 'K_co.jpg', 'K_ro.jpg', 'K_tep.jpg',
            'A_bich.jpg', 'A_co.jpg', 'A_ro.jpg', 'A_tep.jpg'
        ]

        # Xáo bài và hiển thị lần đầu
        self.deal_cards()

    def deal_cards(self):
        # Random 13 lá bài
        chosen_cards = random.sample(self.cards, 13)

        # Hiển thị ảnh của các quân bài theo quy tắc mậu binh
        for i, card_name in enumerate(chosen_cards):
            pixmap = QPixmap(f'poker/{card_name}')
            self.card_labels[i].setPixmap(pixmap.scaled(100, 150))

            # Gắn tooltip để biết tên file khi kéo thả
            self.card_labels[i].setToolTip(card_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PokerApp()
    window.show()
    sys.exit(app.exec())
