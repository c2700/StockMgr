from tkinter import Frame, Button, Entry, Toplevel, Label, Spinbox
from tkinter.ttk import Combobox

class ChangeStockStateWindow():
    def __init__(self, stock_type_text, db_conn_obj, table_name):
        self.stock_type_text = stock_type_text
        self.db_conn_obj = db_conn_obj
        self.table_name = table_name

        self.title = "change " + self.stock_type_text + " stock state"
        self.stockstatewindow = Toplevel()
        self.stockstatewindow.title(self.title)
        self.stockstatewindow.minsize(width=480, height=160)

        self.Title = Label(self.stockstatewindow, text=self.title)
        self.StockNameCombobox = Combobox(self.stockstatewindow)
        self.FromStockStateCombobox = Combobox(self.stockstatewindow)
        self.ToStockStateCombobox = Combobox(self.stockstatewindow)
        self.StockQuantitySpinbox = Spinbox(self.stockstatewindow, width=8)
        self.ChangeBtn = Button(self.stockstatewindow, text="Change", command=self.ChangeBtn)

        self.Title.grid(row=0, column=1, pady=10)
        self.StockNameCombobox.grid(row=1, column=0, padx=15, pady=5)
        self.FromStockStateCombobox.grid(row=1, column=1, padx=5, pady=5)
        self.ToStockStateCombobox.grid(row=2, column=1, padx=5, pady=5)
        self.StockQuantitySpinbox.grid(row=2, column=2, padx=5, pady=5)
        self.ChangeBtn.grid(row=3, column=0, padx=5, pady=5)

    def ChangeBtn(self):
        pass



class AddRemoveWindow():
    def __init__(self, title_text, db_conn_obj, table_name):
        self.title_text = title_text
        self.db_conn_obj = db_conn_obj
        self.table_name = table_name

        self.title = "Add/Remove " + self.title_text + " from " + self.title_text + " stock"

        self.addremovewindow = Toplevel()
        self.addremovewindow.title()
        self.addremovewindow.minsize(width=320, height=130)

        # Handlers
        self.addremovewindow.protocol("WM_DELETE_WINDOW")

        # grid layout mngr
        self.TopFrame = Frame(self.addremovewindow)
        self.TopFrame.grid(row=0, column=0)

        self.BottomFrame = Frame(self.addremovewindow)
        self.BottomFrame.grid(row=1, column=0)

        self.label = Label(self.TopFrame, text=self.title)
        self.component_entry_name = Entry(self.TopFrame, width=30)
        self.component_quntity_spinbox = Spinbox(self.TopFrame, width=7, increment=True)
        self.add_btn = Button(self.BottomFrame, text="add", command=self.AddToDB)
        self.rem_btn = Button(self.BottomFrame, text="remove", command=self.RemoveFromDB)

        self.label.grid(row=0, column=0, ipadx=10, ipady=10)
        self.component_entry_name.grid(row=1, column=0, ipady=2, padx=2, pady=2)
        self.component_quntity_spinbox.grid(row=1, column=1, ipady=2, padx=10, pady=10)
        self.add_btn.grid(row=0, column=0, padx=2, pady=2)
        self.rem_btn.grid(row=0, column=1, padx=2, pady=2)

    # Add self.Name & self.count to self.table_name
    def AddToDB(self):
        pass

    # Remove self.Name & self.count from self.table_name
    def RemoveFromDB(self):
        pass
