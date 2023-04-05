import tkinter
from idlelib.sidebar import temp_enable_text_widget
from tkinter import Frame, Button, Entry, Toplevel, Label, Spinbox, messagebox
from tkinter.ttk import Combobox
# from db_ops import *
import random



def Widget_TempText(temp_text, widget_object):
    widget_object.insert(0, temp_text)
    '''
    widget_object.bind("<FocusIn>", lambda event: widget_object.delete(0, "end"))
    widget_object.bind("<FocusOut>", lambda event: ReEnter_Text())
    # widget_object.bind("<Button-1>", lambda event: widget_object.insert(0, temp_text))

    def ReEnter_Text():
        if (widget_object.get() == temp_text) or (widget_object.get() == ""):
            widget_object.delete(0, "end")
            widget_object.insert(0, temp_text)
        else:
            widget_object.insert(0, widget_object.get())
    '''


def RandomCharGenerator(char_len):
    chr_list = [chr(i) for i in range(48, 58)]
    # chr_list += [chr(i) for i in range(65, 91)]

    print(chr_list)

    random_val = ""

    rand = random.Random()
    for i in range(0, char_len):
        random_val += rand.choice(chr_list)
    return int(random_val)


def MultiCellSelect(TableObj, event, return_cell_coord=False):
    _column = TableObj.identify_column(event)
    _row = TableObj.identify_row(event)
    # TableObj.toggle_select_cell(row=_row, column=_column)
    TableObj.add_cell_selection(row=_row, column=_column)
    if return_cell_coord is True:
        return _row, _column




class DefaultValues:
    def __init__(self):
        self.stock_state_dict = {
            0: "in-stock",
            1: "out-of stock",
            2: "lost",
            3: "damaged",
            4: "defective",
            5: "rejected",
            6: "ordered"
        }


class ChangeStockStateWindow(DefaultValues):
    # def __init__(self, stock_type_text, db_conn_obj, table_name):
    def __init__(self, stock_type_text, db_ops_obj, table_name):
        super(ChangeStockStateWindow, self).__init__()
        self.stock_type_text = stock_type_text
        self.table_name = table_name
        # self.db_conn_obj = db_conn_obj
        self.db_ops_obj = db_ops_obj

        self.title = "change " + self.stock_type_text + " stock state"
        self.stockstatewindow = Toplevel()
        self.stockstatewindow.title(self.title)
        self.stockstatewindow.minsize(width=480, height=160)

        # self.stockstatewindow.protocol(name="WM_DELETE_WINDOW", func=self.stockstatewindow.destroy())

        self.Title = Label(self.stockstatewindow, text=self.title)
        self.StockNameCombobox = Combobox(self.stockstatewindow)
        self.FromStockStateCombobox = Combobox(self.stockstatewindow)
        self.FromStockStateQntytLabel = Label(self.stockstatewindow)
        self.ToStockStateCombobox = Combobox(self.stockstatewindow)
        self.StockQuantitySpinbox = Spinbox(self.stockstatewindow, width=8)
        self.ChangeBtn = Button(self.stockstatewindow, text="Change ", command=self.ChangeBtn)

        self.Title.grid(row=0, column=1, pady=10)
        self.StockNameCombobox.grid(row=1, column=0, padx=15, pady=5)
        self.FromStockStateCombobox.grid(row=1, column=1, padx=5, pady=5)  # top
        self.FromStockStateQntytLabel.grid(row=1, column=2, padx=5, pady=5)  # top
        self.ToStockStateCombobox.grid(row=2, column=1, padx=5, pady=5)  # bottom
        self.StockQuantitySpinbox.grid(row=2, column=2, padx=5, pady=5)
        self.ChangeBtn.grid(row=3, column=0, padx=5, pady=5)

        Widget_TempText(temp_text=f"{self.stock_type_text} Name", widget_object=self.StockNameCombobox)
        Widget_TempText(temp_text=f"From Stock State", widget_object=self.FromStockStateCombobox)
        Widget_TempText(temp_text=f"To Stock State", widget_object=self.ToStockStateCombobox)
        Widget_TempText(temp_text=f"Quantity", widget_object=self.StockQuantitySpinbox)


    def ChangeBtn(self):
        pass

    def MoveItemsBtn(self, from_list, to_list):
        pass

class AddRemoveWindow:
    # def __init__(self, title_text, db_conn_obj, db_ops_obj, table_name):
    def __init__(self, title_text, db_ops_obj, table_name):
        self.title_text = title_text
        self.table_name = table_name
        self.db_ops_obj = db_ops_obj
        # self.db_conn_obj = db_conn_obj
        # self.db_ops_obj = DBops(db_conn_obj)

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

        self.entry_name = Entry(self.TopFrame, width=30)
        self.quantity_spinbox = Spinbox(self.TopFrame, width=10, increment=True)

        self.BottomFrame = Frame(self.addremovewindow)
        self.BottomFrame.grid(row=1, column=0)
        self.add_btn = Button(self.BottomFrame, text="Add " + title_text)
        self.rem_btn = Button(self.BottomFrame, text="Remove " + title_text)

        self.label.grid(row=0, column=0, ipadx=10, ipady=10)
        self.entry_name.grid(row=1, column=0, ipady=2, padx=2, pady=2)
        self.quantity_spinbox.grid(row=1, column=1, ipady=2, padx=10, pady=10)
        self.add_btn.grid(row=0, column=0, padx=2, pady=2)
        self.rem_btn.grid(row=0, column=1, padx=2, pady=2)

        Widget_TempText(temp_text=f"{title_text} Name", widget_object=self.entry_name)
        Widget_TempText(temp_text="Quantity", widget_object=self.quantity_spinbox)

    def AddValueCheck(self):
        if self.quantity_spinbox.get() == "" and self.entry_name.get() == "":
            messagebox.showerror(message=f"Please enter a Name and Quantity")
            return 3
        if self.quantity_spinbox.get() == "" and self.entry_name.get() != "":
            messagebox.showerror(message=f"Please enter a Quantity")
            return 2
        if self.quantity_spinbox.get() != "" and self.entry_name.get() == "":
            messagebox.showerror(message=f"Please enter a Name")
            return 1
        return 0

    def RemoveValueCheck(self):
        if self.entry_name.get() == "":
            messagebox.showerror(message=f"Please enter a Name")
            return 3
        return 0
