import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow

class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        """
        Mã hóa Rail Fence theo số hàng (num_rails).
        Nếu num_rails <= 1, trả về plain_text gốc.
        """
        if num_rails <= 1:
            return plain_text

        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        """
        Giải mã Rail Fence:
        - Tính số ký tự của từng rail.
        - Phân bổ các ký tự từ cipher_text cho đúng rail.
        - Duyệt đường zigzag để tái tạo plaintext.
        Nếu num_rails <= 1, trả về cipher_text gốc.
        """
        if num_rails <= 1:
            return cipher_text

        # Tính số ký tự trên mỗi rail theo cách duyệt zigzag
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Phân đoạn cipher_text thành từng rail
        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length

        # Duyệt lại đường zigzag để tái tạo plaintext
        plain_text = ""
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index].pop(0)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return plain_text

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện cho nút Encrypt và Decrypt
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key_text = self.ui.txt_key.toPlainText().strip()

        try:
            num_rails = int(key_text)
            if num_rails < 2:
                raise ValueError("Số rail phải >= 2")
        except ValueError:
            QMessageBox.critical(self, "Error", "Key phải là số nguyên >= 2")
            return

        cipher = RailFenceCipher()
        cipher_text = cipher.rail_fence_encrypt(plain_text, num_rails)
        self.ui.txt_cipher_text.setPlainText(cipher_text)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Encrypted Successfully")
        msg.exec_()

    def decrypt_text(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key_text = self.ui.txt_key.toPlainText().strip()

        try:
            num_rails = int(key_text)
            if num_rails < 2:
                raise ValueError("Số rail phải >= 2")
        except ValueError:
            QMessageBox.critical(self, "Error", "Key phải là số nguyên >= 2")
            return

        cipher = RailFenceCipher()
        plain_text = cipher.rail_fence_decrypt(cipher_text, num_rails)
        self.ui.txt_plain_text.setPlainText(plain_text)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Decrypted Successfully")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
