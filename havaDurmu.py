
import sys
from PyQt5.QtWidgets import QApplication
from ui_havaDurumu import *

import requests
from bs4 import BeautifulSoup
import re


class AnaPencere(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        
        super(AnaPencere, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.horizontalSliderSicaklik.setValue(0)
        self.ui.horizontalSliderNem.setValue(0)
        self.ui.radioButtonManuel.clicked.connect(self.manuel)
        self.ui.radioButtonOtomatik.clicked.connect(self.veriCekme)
              
        self.sicaklikStyle = """
        QFrame{
            border-radius: 150px;
            background-color: qconicalgradient(cx:0.51, cy:0.511364, angle:270.2, 
            stop: {STOP_0} rgba(255, 255, 255, 255), 
            stop: {STOP_1} rgba(255, 255, 0, 255), 
            stop: {STOP_2} rgba(255, 151, 0, 255), 
            stop:1 rgba(255, 0, 0, 255));
            }
            """
        # stop0 0
        # stop1 0.04
        # stop2 0.08

        self.nemStyle = """
        QFrame{
	        border-radius:130px;
	        background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:0.999818, 
            stop: {STOP_3} rgba(255, 255, 255, 255), 
            stop: {STOP_4} rgba(113, 144, 255, 255), 
            stop:1 rgba(69, 110, 255, 255));
	
            }
        """
        # stop3 0.15
        # stop4 0.3

        self.degerText = "SICAKLIK: {SICAKLIK}\nNEM: %{NEM}"

    def manuel(self):
        self.ui.horizontalSliderSicaklik.valueChanged.connect(self.manuelDeger)
        self.ui.horizontalSliderNem.valueChanged.connect(self.manuelDeger)

    def manuelDeger(self):
        if self.ui.radioButtonManuel.isChecked():
            value_0 = self.ui.horizontalSliderSicaklik.value()
            sicaklik =str(value_0)
            print("value0", value_0)

            progress = (100 - value_0) / 100.0
            stop_0 = str(progress - 0.08)
            stop_1 = str(progress - 0.04)
            stop_2 = str(progress)

            print("stop0 ", stop_0)
            print("stop1 ", stop_1)

            new_SicaklikStyle = self.sicaklikStyle.replace("{STOP_0}", stop_0).replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
            self.ui.frameSicaklik.setStyleSheet(new_SicaklikStyle)

            

            value_1 = self.ui.horizontalSliderNem.value()
            nem =str(value_1)
            print("value1", value_1)

            progress = (100 - value_1) / 100.0
            stop_3 = str(progress - 0.15)
            stop_4 = str(progress)

            print("stop3 ", stop_3)
            print("stop4 ", stop_4)

            new_NemStyle = self.nemStyle.replace("{STOP_3}", stop_3).replace("{STOP_4}", stop_4)
            self.ui.frameNem.setStyleSheet(new_NemStyle)

            newText = self.degerText.replace("{SICAKLIK}", str(value_0)).replace("{NEM}", str(value_1))
            self.ui.labelDeger.setText(newText)


    def veriCekme(self):
        if self.ui.radioButtonOtomatik.isChecked():
            self.ui.horizontalSliderNem.setValue(0)
            self.ui.horizontalSliderSicaklik.setValue(0)
            

            urlSicaklik = "https://havadurumu15gunluk.xyz/havadurumu/630/istanbul-hava-durumu-15-gunluk.html"
            response = requests.get(urlSicaklik)
            html_icerigi = response.content
            source = BeautifulSoup(html_icerigi, "html.parser")

            sicaklikDerecesi = source.find_all("span", {"class":"temperature type-1"})    
            nemYuzdesi = source.find_all("span",{"class": "bold"})

            sicaklikDerecesi = str(sicaklikDerecesi[0])
            sicaklikDerecesi = re.findall(r">\S+<",sicaklikDerecesi)
            sicaklikDerecesi = str(sicaklikDerecesi[0])
            sicaklikDerecesi = sicaklikDerecesi[1:3]
            

            value_0 = int(sicaklikDerecesi)
            sicaklik =str(value_0)
            print("value0", value_0)

            progress = (100 - value_0) / 100.0
            stop_0 = str(progress - 0.08)
            stop_1 = str(progress - 0.04)
            stop_2 = str(progress)

            print("stop0 ", stop_0)
            print("stop1 ", stop_1)

            new_SicaklikStyle = self.sicaklikStyle.replace("{STOP_0}", stop_0).replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
            self.ui.frameSicaklik.setStyleSheet(new_SicaklikStyle)


            nemYuzdesi = str(nemYuzdesi[3])
            nemYuzdesi = re.findall(r">\S+<",nemYuzdesi)
            nemYuzdesi = str(nemYuzdesi[0])
            value_1 = nemYuzdesi[2:4]
            
            value_1 = int(value_1)
            nem =str(value_1)
            print("value1", value_1)

            progress = (100 - value_1) / 100.0
            stop_3 = str(progress - 0.15)
            stop_4 = str(progress)

            print("stop3 ", stop_3)
            print("stop4 ", stop_4)

            new_NemStyle = self.nemStyle.replace("{STOP_3}", stop_3).replace("{STOP_4}", stop_4)
            self.ui.frameNem.setStyleSheet(new_NemStyle)

            newText = self.degerText.replace("{SICAKLIK}", str(value_0)).replace("{NEM}", str(value_1))
            self.ui.labelDeger.setText(newText)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow +icon
    mainWindow = AnaPencere()

    mainWindow.show()

    sys.exit(app.exec_())