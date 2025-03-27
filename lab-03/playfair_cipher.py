import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow

class PlayFairCipher:
    def __init__(self):
        # Bạn có thể bỏ trống hoặc khởi tạo biến nếu cần
        pass

    def create_playfair_matrix(self, key):
        """
        Tạo ma trận 5x5 cho Playfair dựa trên key.
        """
        # Thay J bằng I (theo quy ước Playfair)
        key = key.replace("J", "I")
        key = key.upper()

        # Loại bỏ các ký tự trùng trong key
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Không có J

        # Lọc những ký tự chưa có trong key
        remaining_letters = [letter for letter in alphabet if letter not in key_set]

        # Ghép key + các ký tự còn lại thành danh sách 25 ký tự
        matrix = list(key)
        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break

        # Chia thành ma trận 5x5
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        """
        Tìm vị trí (row, col) của một ký tự trong ma trận.
        """
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        # Nếu không tìm thấy, trả về None
        return None, None

    def playfair_encrypt(self, plain_text, matrix):
        """
        Mã hóa Playfair: 
        - Cặp chữ giống nhau sẽ được chèn 'X' (nếu chưa xử lý cặp lặp trước).
        - Nếu cặp cuối lẻ 1 ký tự, thêm 'X'.
        - Áp dụng quy tắc cùng hàng, cùng cột hoặc hình chữ nhật.
        """
        # Chuẩn hoá plaintext
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()

        encrypted_text = ""
        # Xử lý từng cặp
        i = 0
        while i < len(plain_text):
            # Lấy 2 ký tự một lúc
            pair = plain_text[i:i+2]

            # Nếu cặp chỉ có 1 ký tự, thêm 'X' vào cuối
            if len(pair) == 1:
                pair += "X"
                i += 1
            else:
                i += 2

            # Tìm toạ độ trong ma trận
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Nếu ký tự không hợp lệ (None), bỏ qua
            if row1 is None or row2 is None:
                continue

            # Cùng hàng
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            # Cùng cột
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            # Khác hàng, khác cột
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        """
        Giải mã Playfair:
        - Áp dụng quy tắc ngược với khi mã hoá.
        - Có xử lý loại bỏ bớt 'X' nếu cần.
        """
        cipher_text = cipher_text.upper()
        decrypted_text = ""

        # Xử lý từng cặp
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            if len(pair) < 2:
                # Cặp thiếu ký tự
                continue

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 is None or row2 is None:
                continue

            # Cùng hàng
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            # Cùng cột
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            # Khác hàng, khác cột
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        # Tuỳ theo yêu cầu, bạn có thể xử lý bỏ 'X' cuối hoặc các ký tự đệm
        # Dưới đây là ví dụ xử lý gần giống code bạn cung cấp:
        banro = ""
        i = 0
        while i < len(decrypted_text):
            # Tránh lỗi index khi so sánh i+2
            if i < len(decrypted_text) - 2 and decrypted_text[i] == decrypted_text[i + 2]:
                banro += decrypted_text[i]
                i += 2
            else:
                banro += decrypted_text[i]
                if i + 1 < len(decrypted_text):
                    banro += decrypted_text[i + 1]
                i += 2

        # Nếu ký tự cuối là 'X' thì loại bỏ (theo logic code gốc)
        if len(banro) >= 1 and banro[-1] == 'X':
            banro = banro[:-1]

        return banro


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối nút Encrypt và Decrypt
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.ui.txt_key.toPlainText()

        # Khởi tạo PlayFairCipher và tạo matrix
        cipher = PlayFairCipher()
        matrix = cipher.create_playfair_matrix(key)
        encrypted_text = cipher.playfair_encrypt(plain_text, matrix)

        # Hiển thị kết quả
        self.ui.txt_cipher_text.setPlainText(encrypted_text)

        # Thông báo
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Encrypted Successfully")
        msg.exec_()

    def decrypt_text(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key = self.ui.txt_key.toPlainText()

        cipher = PlayFairCipher()
        matrix = cipher.create_playfair_matrix(key)
        decrypted_text = cipher.playfair_decrypt(cipher_text, matrix)

        self.ui.txt_plain_text.setPlainText(decrypted_text)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Decrypted Successfully")
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
