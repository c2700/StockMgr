from stock_mgr_window import *
from platform import system
import json

def main():
    creds_dict = {}
    try:
        with open("creds.txt", "r", encoding="ascii") as creds_file:
            _ = json.load(creds_file)
            if _ == {}:
                messagebox.showerror(message="no credentials have been issued. Please run the 'db_setup.ps1' script before running the app")
                exit(0)                
        creds_dict = {**_, "host": "localhost", "database": "StockDB"}
        del _
    except FileNotFoundError:
        messagebox.showerror(message="no credentials are stored. Please run the 'db_setup.ps1' script before running the app")
        exit(1)
    if creds_dict == {} or (("user" in creds_dict) and (creds_dict["user"] == "")):
        messagebox.showerror(message="no credentials have been issued. Please run the 'db_setup.ps1' script before running the app")
        exit(1)
    try:
        if system() == "Linux":
            creds_dict["unix_socket"] = "/home/blank/Projects/Hari_stock_mgmnt/StockMgr/tkinter/db/db_server.sock"
            # connect(user='blank',
            #         host="localhost",
            #         database="StockDB",
            #         unix_socket="/home/blank/Projects/Hari_stock_mgmnt/StockMgr/tkinter/db/db_server.sock")
        elif system() == "Windows":
            creds_dict["port"] = 3306
            # connect(user='blank',
            #         host="localhost",
            #         database="StockDB",
            #         port=3306)

        connect(**creds_dict)
        print("FUCK YEA!!!!!!")
    except Error as e:
        messagebox.showerror(message="Please run the The 'StockMgrDB_Service' service")
        exit(1)

    MainWindow = Tk()
    stock_mngr_obj = StockManager(MainWindow, creds_dict=creds_dict)
    MainWindow.protocol(name="WM_DELETE_WINDOW", func=stock_mngr_obj.CloseApp)
    MainWindow.mainloop()
main()
