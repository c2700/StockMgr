from stock_mgr_window import *

def main():
    try:
        if system() == "Linux":
            connect(user='blank',
                    host="localhost",
                    database="StockDB",
                    unix_socket="/home/blank/Projects/Hari_stock_mgmnt/StockMgr/tkinter/db/db_server.sock")
        if system() == "Windows":
            connect(user='blank',
                    host="localhost",
                    database="StockDB",
                    port=3306)

        print("FUCK YEA!!!!!!")
    except Error as e:
        messagebox.showerror(message=f"WTF????? BRUH, evr thot of doing sumthin calld \"**running d DB service**\"\n\n{e}")
        exit(1)

    MainWindow = Tk()
    stock_mngr_obj = StockManager(MainWindow)
    MainWindow.protocol(name="WM_DELETE_WINDOW", func=stock_mngr_obj.CloseApp)
    MainWindow.mainloop()
main()
