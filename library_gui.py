import sys
from PySide import QtGui, QtCore
data = {'Title':['1','2','3'], 'Artist':['4','5','6'], 'Album':['7','8','9']}
class Library(QTableWidget):

	def __init__(self, data, *args):
		QTableWidget.__init__(self, *args)
		self.data = data
		self.populate_library()
		self.resizeColumnsToContents()
		self.resizeRowsToContents()

	def populate_library(self):
		horHeaders = []
		for n, key in enumerate(sorted(self.data.keys())):
			horHeaders.append(key)
			for m, item in enumerate(self.data[key]):
				print m
				print item
				newitem = QTableWidgetItem(item)
				self.setItem(m, n, newitem)
		self.setHorizontalHeaderLabels(horHeaders)

def main(args):
	app = QApplication(args)
	library = Library(data, 5, 3)
	library.show()
	library.raise_()
	sys.exit(app.exec_())

if __name__=="__main__":
	main(sys.argv)