import sys
import ssl
import itertools
import certifi
import urllib.request
from PyQt5.QtWidgets import *

class CurrencyConverter(QDialog):

    def __init__(self, parent=None):
        super(CurrencyConverter, self).__init__(parent)
        date = self.get_data()
        rates = sorted(self._rates.keys())

        date_label = QLabel(date)
        self.from_combo_box = QComboBox()
        self.from_combo_box.addItems(rates)

        self.from_spin_box = QDoubleSpinBox()
        self.from_spin_box.setRange(0.01, 10000000.00)
        self.from_spin_box.setValue(1.00)

        self.to_combo_box = QComboBox()
        self.to_combo_box.addItems(rates)
        self.to_label = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(date_label, 0, 0)
        grid.addWidget(self.from_combo_box, 1, 0)
        grid.addWidget(self.from_spin_box, 1, 1)
        grid.addWidget(self.to_combo_box, 2, 0)
        grid.addWidget(self.to_label, 2, 1)
        self.setLayout(grid)
        
    def get_data(self):
        self._rates = {}

        try:
            date = "2021-03-22"
            data = urllib.request.urlopen("https://www.bankofcanada.ca/"
"valet/observations/group/FX_RATES_DAILY/"
"csv?start_date=2021-03-20", context=ssl.create_default_context(
cafile=certifi.where())).read()
            data_lines = data.decode("utf-8").split("\n")


            data_dict = {}

            for line in itertools.islice(data_lines, 11, None):
                print(line[0])
                #if line[0] == "date":
                    #for i in range(len(line)):
                   #print(line[i])

##                        data_dict[i][0] = curr[3:5]
##                        print(data_dict[i][0])
##                if line[0] == date:
##                    data_dict[i][2] = line[i]
##                index += 1
##            self._rates = data_dict
##            return "Exchange Rates Date: " + date
        except Exception as e:
            return "Failed to download:\n{}".format(e)

app = QApplication(sys.argv)
currency_tool = CurrencyConverter()
currency_tool.show()
app.exec_()
