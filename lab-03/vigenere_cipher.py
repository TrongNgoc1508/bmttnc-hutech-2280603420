import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.vigenere import Ui_MainWindow

class VigenereCipher:
    def __init__(self):
        pass

    def vigenere_encrypt(self, plain_text, key):
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        decrypted_text = ""
        key_index = 0
        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text

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
        key = self.ui.txt_key.toPlainText().strip()

        if not key:
            QMessageBox.critical(self, "Error", "Key cannot be empty")
            return

        cipher = VigenereCipher()
        cipher_text = cipher.vigenere_encrypt(plain_text, key)
        self.ui.txt_cipher_text.setPlainText(cipher_text)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Encrypted Successfully")
        msg.exec_()

    def decrypt_text(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key = self.ui.txt_key.toPlainText().strip()

        if not key:
            QMessageBox.critical(self, "Error", "Key cannot be empty")
            return

        cipher = VigenereCipher()
        plain_text = cipher.vigenere_decrypt(cipher_text, key)
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
