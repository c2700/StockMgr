from stock_mgr_window import *
from sqlite3 import *


def main():
    MainWindow = Tk()
    stock_mngr_obj = StockManager(MainWindow)
    MainWindow.protocol(name="WM_DELETE_WINDOW", func=stock_mngr_obj.CloseApp)
    MainWindow.mainloop()


main()
