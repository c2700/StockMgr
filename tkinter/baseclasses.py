import sqlite3
import tkinter
from tkinter import Frame, Button, Entry, Toplevel, Label, Spinbox
from tkinter.ttk import Combobox
from db_ops import *

class ChangeStockStateWindow:
    def __init__(self, stock_type_text, db_conn_obj, table_name):
        self.stock_type_text = stock_type_text
        self.table_name = table_name
        self.db_conn_obj = db_conn_obj

        self.title = "change " + self.stock_type_text + " stock state"
        self.stockstatewindow = Toplevel()
        self.stockstatewindow.title(self.title)
        self.stockstatewindow.minsize(width=480, height=160)

        # self.stockstatewindow.protocol(name="WM_DELETE_WINDOW", func=self.stockstatewindow.destroy())

        self.Title = Label(self.stockstatewindow, text=self.title)
        self.StockNameCombobox = Combobox(self.stockstatewindow)
        self.FromStockStateCombobox = Combobox(self.stockstatewindow)
        self.ToStockStateCombobox = Combobox(self.stockstatewindow)
        self.StockQuantitySpinbox = Spinbox(self.stockstatewindow, width=8)
        self.ChangeBtn = Button(self.stockstatewindow, text="Change ", command=self.ChangeBtn)

        self.Title.grid(row=0, column=1, pady=10)
        self.StockNameCombobox.grid(row=1, column=0, padx=15, pady=5)
        self.FromStockStateCombobox.grid(row=1, column=1, padx=5, pady=5)
        self.ToStockStateCombobox.grid(row=2, column=1, padx=5, pady=5)
        self.StockQuantitySpinbox.grid(row=2, column=2, padx=5, pady=5)
        self.ChangeBtn.grid(row=3, column=0, padx=5, pady=5)

    def ChangeBtn(self):
        pass


class AddRemoveWindow:
    def __init__(self, title_text, db_conn_obj, table_name):
        self.title_text = title_text
        self.table_name = table_name
        self.db_ops_obj = DBops(db_conn_obj)

        # print("self.title_text -", self.title_text)
        # print("self.table_name -", self.table_name)
        # print("title_text -", title_text)
        # print("table_name -", table_name)

        self.title = "Add/Remove " + self.title_text + " from/to " + self.title_text + " stock"

        self.NameVar = tkinter.StringVar()
        self.NameCountVar = tkinter.StringVar()
        self.VarArray = []
        self.VarArray += [self.NameVar]
        self.VarArray += [self.NameCountVar]

        self.addremovewindow = Toplevel()
        self.addremovewindow.title()
        self.addremovewindow.minsize(width=320, height=130)

        # grid layout mngr
        self.TopFrame = Frame(self.addremovewindow)
        self.TopFrame.grid(row=0, column=0)
        self.label = Label(self.TopFrame, text=self.title)

        self.component_entry_name = Entry(self.TopFrame, width=30)
        self.component_quantity_spinbox = Spinbox(self.TopFrame, width=7, increment=True)

        def AddTableRow():
            self.db_ops_obj.AddRow(table_name=self.table_name, Name=self.component_entry_name.get(),
                                   NameCount=self.component_quantity_spinbox.get())
            # try:
            #     self.db_ops_obj.AddTableRow(table_name=self.table_name, Name=self.component_entry_name.get(),
            #                                 NameCount=self.component_quantity_spinbox.get())
            #     print("haaaa. I'm promoted")
            # except:
            #     print("WTF???")

        def RemoveTableRow():
            self.db_ops_obj.RemoveRow(table_name=self.table_name, Name=self.component_entry_name.get())
            # try:
            #     self.db_ops_obj.RemoveTableRow(table_name=self.table_name, Name=self.component_entry_name.get(),
            #                                    NameCount=self.component_quantity_spinbox.get())
            #     print("heehee. I'm gona get fyerd")
            # except:
            #     print("I DELETED AN ENTYR COLUM TEEHEE :P")


        self.BottomFrame = Frame(self.addremovewindow)
        self.BottomFrame.grid(row=1, column=0)
        self.add_btn = Button(self.BottomFrame, text="Add " + title_text, command=lambda: AddTableRow())
        self.rem_btn = Button(self.BottomFrame, text="Remove " + title_text, command=lambda: RemoveTableRow())

        self.label.grid(row=0, column=0, ipadx=10, ipady=10)
        self.component_entry_name.grid(row=1, column=0, ipady=2, padx=2, pady=2)
        self.component_quantity_spinbox.grid(row=1, column=1, ipady=2, padx=10, pady=10)
        self.add_btn.grid(row=0, column=0, padx=2, pady=2)
        self.rem_btn.grid(row=0, column=1, padx=2, pady=2)

class DefaultValues():
    def __init__(self):
        self.stock_state_dict = {
            0: "in-stock",
            1: "out-of stock",
            2: "lost",
            3: "damaged",
            4: "defective",
            5: "rejected",
            6: "ordered",
        }
