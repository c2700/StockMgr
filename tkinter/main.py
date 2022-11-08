from stock_mgr_window import *

def main():
    MainWindow = Tk()
    MainWindow.protocol("WM_DELETE_WINDOW")
    StockManager(MainWindow)
    MainWindow.mainloop()
main()

