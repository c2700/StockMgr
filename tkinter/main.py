from stock_mgr_window import *
from sqlite3 import *

def main():
    MainWindow = Tk()
    MainWindow.protocol("WM_DELETE_WINDOW")
    StockManager(MainWindow)
    MainWindow.mainloop()
main()

