from tkinter import Frame, Button, Entry, Toplevel, Label, Spinbox
from tkinter.ttk import Combobox

class ChangeStockStateWindow():
    def __init__(self, stock_type_text):
    # def __init__(self, MainWindow, stock_type_text):
        self.title = "change " + stock_type_text + " stock state"
        self.stockstatewindow = Toplevel()
        self.stockstatewindow.title(self.title)
        # self.stockstatewindow.geometry("480x150")
        self.stockstatewindow.minsize(width=480, height=160)
        # self.stockstatewindow.transient(MainWindow)

        self.Title = Label(self.stockstatewindow, text=self.title)
        self.StockNameCombobox = Combobox(self.stockstatewindow)
        self.FromStockStateCombobox = Combobox(self.stockstatewindow)
        self.ToStockStateCombobox = Combobox(self.stockstatewindow)
        self.StockQuantitySpinbox = Spinbox(self.stockstatewindow, width=8)
        self.ChangeBtn = Button(self.stockstatewindow, text="Change")

        self.Title.grid(row=0, column=1, pady=10)
        self.StockNameCombobox.grid(row=1, column=0, padx=15, pady=5)
        self.FromStockStateCombobox.grid(row=1, column=1, padx=5, pady=5)
        self.ToStockStateCombobox.grid(row=2, column=1, padx=5, pady=5)
        self.StockQuantitySpinbox.grid(row=2, column=2, padx=5, pady=5)
        self.ChangeBtn.grid(row=3, column=0, padx=5, pady=5)
        # self.stockstatewindow.wm_withdraw()

class AddRemoveWindow():
    # def __init__(self, MainWindow, title_text):
    def __init__(self, title_text):
        self.title = "Add/Remove " + title_text + " from stock"

        self.addremovewindow = Toplevel()
        self.addremovewindow.title()
        # self.addremovewindow.geometry("320x130")
        self.addremovewindow.minsize(width=320, height=130)

        # Handlers
        self.addremovewindow.protocol("WM_DELETE_WINDOW")
        # grid layout mngr
        self.TopFrame = Frame(self.addremovewindow)
        self.TopFrame.grid(row=0, column=0)

        self.BottomFrame = Frame(self.addremovewindow)
        self.BottomFrame.grid(row=1, column=0)

        self.label = Label(self.TopFrame, text=self.title).grid(row=0, column=0, ipadx=10, ipady=10)
        self.component_entry_name = Entry(self.TopFrame, width=30).grid(row=1, column=0, ipady=2, padx=2, pady=2)
        self.component_quntity_spinbox = Spinbox(self.TopFrame, width=7, increment=True).grid(row=1, column=1, ipady=2, padx=2, pady=2)
        self.add_btn = Button(self.BottomFrame, text="add").grid(row=0, column=0, padx=2, pady=2)
        self.rem_btn = Button(self.BottomFrame, text="remove").grid(row=0, column=1, padx=2, pady=2)

        # place layout mngr
        # self.label = Label(self.popupwindow, text="Add/Remove Components from stock").place(x=self.popupwindow.winfo_width()/3, y=self.popupwindow.winfo_height()/4)
        # self.component_entry_name = Entry(self.popupwindow, name="component_name").place(x=self.popupwindow.winfo_width()/2, y=self.popupwindow.winfo_height()/2)
        # self.component_quntity_spinbox = Spinbox(self.popupwindow).place(x=self.popupwindow.winfo_width()*(2/3), y=self.popupwindow.winfo_height()/2)
        # self.add_btn = Button(text="add").place(x=self.popupwindow.winfo_width()*(5/6), y=self.popupwindow.winfo_height()/2)
        # self.rem_btn = Button(text="add").place(x=self.popupwindow.winfo_width()*(5/6), y=self.popupwindow.winfo_height()*(3/4))

