import sys
import PyQt6
import requests

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main.ui', self)
        self.press_delta = 0.00001

        self.map_zoom = 5
        self.map_ll = [39.55, 50.19]
        self.map_l = 'map'
        self.map_key = ''

        self.start()

    def start(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get('https://static-maps.yandex.ru/1.x/',
                               params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.maplabel.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())