import re
import tkinter.messagebox
from tkinter.ttk import *
import tksheet
from tkinter import *
from mariadb import connect, Error
from baseclasses import *
from db_ops import *
from platform import system

class StockManager(DefaultValues):
    def __init__(self, MainWindow):
        super(StockManager, self).__init__()
        self.MainWindow = MainWindow
        self.db_conn_obj = None
        self.db_cursor = None
        self.db_ops = None
        try:
            if system() == "Linux":
                self.db_conn_obj = connect(user='blank',
                                           host="localhost",
                                           database="StockDB",
                                           unix_socket="/home/blank/Projects/Hari_stock_mgmnt/StockMgr/tkinter/db/db_server.sock")
            if system() == "Windows":
                self.db_conn_obj = connect(user='blank',
                                  host="localhost",
                                  database="StockDB",
                                  port=3306)

            self.db_cursor = self.db_conn_obj.cursor()
            print("FUCK YEA!!!!!!")
            self.db_ops = DBops(db_cursor=self.db_cursor)

        # except Exception as e:
        #     print("WTF????? AAAAHHHHH IS D FUCKING SERVICE UP & RUNNING!!??????", e)
        except Error as e:
            print("WTF????? AAAAHHHHH IS D FUCKING SERVICE UP & RUNNING!!??????", e)
            # exit(1)

        self.MainWindow.title("Stock Manager")
        self.MainWindow.geometry("1200x700")

        # def ShiftSelection():
        #     pass

        self.MainWindowTable = tksheet.Sheet(self.MainWindow, headers=["Product", "count", "stock_state"], data=self.MainWindowTableData(), show_horizontal_grid=True, expand_sheet_if_paste_too_big=True, show_vertical_grid=True)
        self.MainWindowTable.set_all_cell_sizes_to_text()
        self.MainWindowTable.enable_bindings("all")
        self.MainWindowTable.edit_bindings(True)
        self.MainWindowTable.basic_bindings(enable=True)
        self.MainWindowTable.tk_focusFollowsMouse()
        # self.MainWindowTable.extra_bindings(bindings="bind_all", func=lambda event: ShiftSelection)

        self.MainWindowButtonsLayout = Frame(self.MainWindow)

        # placing frames & sheet object in window
        self.MainWindowTable.grid(row=0, column=0, padx=10, pady=10)
        self.MainWindowButtonsLayout.grid(row=0, column=1, pady=(0, 150))

        # creating buttons in table view frame
        self.AddRemComponentBtn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Component", command=lambda: AddRemoveComponentWindow(db_ops_obj=self.db_ops))
        # self.AddRemProductBTn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Product", command=lambda: ShowProductStockTableWindow(db_cursor=self.db_cursor, db_ops_obj=self.db_ops).AddProductWindow())
        # self.AddRemProductBTn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Product", command=lambda: None)
        self.AddRemProductBTn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Product", command=lambda: AddRemoveProductWindow(db_ops_obj=self.db_ops))
        self.ChangeComponentStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Component Stock State", command=lambda: ChangeComponentStockStateWindow(db_ops_obj=self.db_ops))
        self.ChangeProductStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Product Stock State", command=lambda: ChangeProductStateWindow(db_ops_obj=self.db_ops))
        self.ShowStockTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Component Stock Table", command=lambda: ShowComponentStockTableWindow(db_cursor=self.db_cursor, db_ops_obj=self.db_ops))
        self.ShowProductTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Product Stock Table", command=lambda: ShowProductStockTableWindow(db_cursor=self.db_cursor, db_ops_obj=self.db_ops))
        self.SearchComponentEntry = Entry(self.MainWindowButtonsLayout, width=30, name="search_component_stock_entry")
        self.SearchComponentBTn = Button(self.MainWindowButtonsLayout, width=12, text="Search Component", command=lambda: self.SearchWindow())

        # arranging ui elements
        self.AddRemComponentBtn.grid(row=0, column=0, padx=5, pady=5)
        self.AddRemProductBTn.grid(row=0, column=1, padx=5, pady=5)
        self.ChangeComponentStockStateBTn.grid(row=1, column=0, padx=5, pady=5)
        self.ChangeProductStockStateBTn.grid(row=1, column=1, padx=5, pady=5)
        self.ShowStockTableBTn.grid(row=2, column=0, padx=5, pady=5)
        self.ShowProductTableBTn.grid(row=2, column=1, padx=5, pady=5)
        self.SearchComponentEntry.grid(row=4, column=1, ipadx=10, ipady=5)
        self.SearchComponentBTn.grid(row=4, column=0, padx=35, pady=5, ipadx=10)

        # component keybindings
        self.SearchComponentEntry.bind("<Return>", lambda event: self.SearchWindow())

    def MainWindowTableData(self):
        try:
            db_data_set_list = [self.db_ops.FetchAllProducts(getcount=True, getstockstate=True)]
            data_list = []
            if db_data_set_list is None:
                print("SHIIIIITTTTT")
            if db_data_set_list is not None:
                for i in db_data_set_list[0]:
                    _temp_data = list(i[0][:-1])
                    _stock_state = [i[1]]
                    data_list += [_temp_data + _stock_state]
                return data_list
        except Exception as e:
            print("WTF IS RONG WID DIS DB???? ", e)

    def CloseApp(self):
        try:
            if self.db_cursor.close():
                print("MOMENT of TRUTH")
            if self.db_conn_obj.close():
                print("HOLY SHIT IT WORX")
        except Exception as e:
            print("NOOOOOOOOO....THE DB IS A ZOMBEEEEEE", e)
        self.MainWindow.destroy()

    def SearchWindow(self):
        if self.SearchComponentEntry.get() == "":
            tkinter.messagebox.showinfo(title="INFO", message="Please Enter a component name")
        elif self.SearchComponentEntry.get() != "":
            SearchPopupWindow = Toplevel()
            SearchPopupWindow.title = "Search Result"
            SearchPopupWindow.minsize(height=100, width=200)
            SearchComponentEntryValue = self.SearchComponentEntry.get()

            result = None
            if re.search('^\d+$', SearchComponentEntryValue):
                result = self.db_ops.FetchComponent(select_cols=["Name", "Code"], conditional_query={"Code":f"'{SearchComponentEntryValue}"}, getstockstate=True)
                # result = self.db_ops.FetchComponent(select_cols=["Name", "Code"], conditional_query={"Code":f"'{SearchComponentEntryValue}"}, getstockstate=True)
            if re.search('([0-9]+)?[a-zA-Z]+([0-9]+)?', SearchComponentEntryValue):
                result = self.db_ops.FetchComponent(select_cols=["Name", "Code"], conditional_query={"Name":f"'{SearchComponentEntryValue}'"}, getstockstate=True)
                # result = self.db_ops.FetchComponent(select_cols=["Name", "Code"], conditional_query={"Name":f"'{SearchComponentEntryValue}'"}, getstockstate=True)
            if result == None:
                tkinter.messagebox.showwarning(message=f"Component does not exist")
                return

            stock_state = result[1]
            count = result[0][0][2]
            name = result[0][0][0]
            code = result[0][0][1]

            ComponentInfoLabel = f"Component Name: {name}\nComponent Code: {code}\nComponent Count: {count}\nStock State: {stock_state}"
            SearchString = Label(SearchPopupWindow, text=ComponentInfoLabel)
            SearchString.grid(row=0, column=0, pady=10, padx=10)


class AddRemoveComponentWindow(AddRemoveWindow):
    def __init__(self, db_ops_obj):
        self.db_ops_obj = db_ops_obj
        super(AddRemoveComponentWindow, self).__init__(title_text="Component", db_ops_obj=self.db_ops_obj, table_name="ComponentStock")
        self.add_btn.configure(command=lambda: self.AddComponentValue())
        self.rem_btn.configure(command=lambda: self.RemoveComponentValue())

    def AddComponentValue(self):
        if self.AddValueCheck() == 0:
            _component_name = f"'{self.entry_name.get()}'"
            _component_quantity = self.quantity_spinbox.get()
            # _component_code = RandomCharGenerator(char_len=6)
            # self.db_ops_obj.AddComponent(_component_name, _component_code, _component_quantity)
            self.db_ops_obj.AddComponent(_component_name, _component_quantity)

    def RemoveComponentValue(self):
        if self.RemoveValueCheck() == 0:
            _component_name = f"'{self.entry_name.get()}'"
            _component_code = self.db_ops_obj.FetchComponent(select_cols=["Code"], conditional_query={"Name": _component_name})
            self.db_ops_obj.RemoveComponent(component_name=_component_name, component_code=_component_code)



class AddRemoveProductWindow(AddRemoveWindow):
    def __init__(self, db_ops_obj):
        self.db_ops_obj = db_ops_obj
        super(AddRemoveProductWindow, self).__init__(title_text="Product", db_ops_obj=self.db_ops_obj, table_name="ProductStock")
        self.add_btn.configure(command=lambda: self.AddProductValue())
        self.rem_btn.configure(command=lambda: self.RemoveProductValue())
    def AddProductValue(self):
        if self.AddValueCheck() == 0:
            _product_name = f"'{self.entry_name.get()}'"
            _product_count = self.quantity_spinbox.get()
            # _product_code = RandomCharGenerator(char_len=8)
            _component_list_dict = {}
            self.db_ops_obj.AddProduct(_product_name, _product_count, component_list_dict=_component_list_dict)
            # self.db_ops_obj.AddProduct(_component_name, _component_code, _component_quantity)

    def RemoveProductValue(self):
        if self.RemoveValueCheck() == 0:
            _product_name = self.entry_name.get()
            _product_code = self.db_ops_obj.FetchProduct(select_cols=["Code"], conditional_query={"Name": f"'{_product_name}"})
            self.db_ops_obj.RemoveProduct(component_name=_product_name, component_code=_product_code)


class ChangeComponentStockStateWindow(ChangeStockStateWindow):
    def __init__(self, db_ops_obj):
        self.db_ops_obj = db_ops_obj

        self._inStock = 0
        self._rejected = 0
        self._lost = 0
        self._defective = 0

        super(ChangeComponentStockStateWindow, self).__init__(stock_type_text="Component", db_ops_obj=self.db_ops_obj, table_name="ComponentStock")
        self.ComponentName = None
        self._component_list = db_ops_obj.FetchAllComponents()
        self.ComponentNameComboBox = self.StockNameCombobox

        _ = []
        for i in self._component_list:
            _ += [i[0]]
        self.ComponentNameComboBox["values"] = _

        self.ChangeBtn.configure(command=lambda: self.ChangeBtnFunc())
        self.ComponentNameComboBox.bind("<<ComboboxSelected>>", lambda event: self.AutoFill_FromStockStateComboBox())
    def AutoFill_FromStockStateComboBox(self):
        self.ComponentName = self.ComponentNameComboBox.get()
        if self.ComponentName == "" or self.ComponentName is None:
            self.FromStockStateCombobox["values"] = [""]
        elif self.ComponentName == "" or self.ComponentName is not None:
            self.Component_code = self.db_ops_obj.FetchComponent(select_cols=["Code"], conditional_query={"Name": f"'{self.ComponentName}'"})[0][0]

            self._inStock, self._rejected, self._lost, self._defective = self.db_ops_obj.FetchComponentAllStocks(Code=self.Component_code)

            self._from_stock_states_list = []
            if self._inStock > 0:
                self._from_stock_states_list += [self.stock_state_dict[1]]
            if self._lost > 0:
                self._from_stock_states_list += [self.stock_state_dict[2]]
            if self._defective > 0:
                self._from_stock_states_list += [self.stock_state_dict[4]]
            if self._rejected > 0:
                self._from_stock_states_list += [self.stock_state_dict[5]]

            self.FromStockStateCombobox["values"] = self._from_stock_states_list

        self.FromStockStateCombobox.bind("<<ComboboxSelected>>", lambda event: self.AutoFill_ToStockStateComboBox())

    def AutoFill_ToStockStateComboBox(self):
        print("IS IT NOR WORKING")
        if self.ComponentName is None:
            self.ToStockStateCombobox["values"] = [""]

        elif self.ComponentName is not None:
            self.ToStockStateCombobox.grab_current()
            # self.db_ops_obj.FetchComponentAllStocks(Code=self.Component_code)[0]
            # sleep(1)

            _ = {
                    "1": self._inStock,
                    "2": self._lost,
                    "4": self._defective,
                    "5": self._rejected
            }

            self._to_stock_states_list = []
            for i in _:
                if self.FromStockStateCombobox.get() == self.stock_state_dict[int(i)]:
                    continue
                else:
                    self._to_stock_states_list += [self.stock_state_dict[int(i)]]

            self.ToStockStateCombobox["values"] = self._to_stock_states_list

            # self.StockQuantitySpinbox.configure(command=lambda event: self.SpinBoxFunc())
            # self.StockQuantitySpinbox.bind("<Key>", lambda event: self.SpinBoxFunc())
            self.StockQuantitySpinbox.bind("<Return>", lambda event: self.SpinBoxFunc())
            # self.StockQuantitySpinbox.bind("<Button-1>", lambda event: self.SpinBoxFunc())
            # self.StockQuantitySpinbox.bind("<Up>", lambda event: self.SpinBoxFunc())
            # self.StockQuantitySpinbox.bind("<Down>", lambda event: self.SpinBoxFunc())
            # self.StockQuantitySpinbox.bind("<>", lambda event: self.SpinBoxFunc())
            # self.StockQuantitySpinbox.bind("<>", lambda event: self.SpinBoxFunc())

    def SpinBoxFunc(self):
        _ = {
            "in-stock": self._inStock,
            "lost": self._lost,
            "defective": self._defective,
            "rejected": self._rejected
        }
        if self.StockQuantitySpinbox.get() == "":
            pass
        if int(self.StockQuantitySpinbox.get()) > _[self.FromStockStateCombobox.get()]:
            messagebox.showerror(message="The quantity to change to is greater than what is available")
            print("it's too much")



    def ChangeBtnFunc(self):
        self.SpinBoxFunc()
        if self.ComponentNameComboBox.get() == "":
            messagebox.showerror(message="Please Select a Component Name to transfer the component to")
            return 1
        if self.ToStockStateCombobox == "":
            messagebox.showerror(message="Please Select a Stock State to transfer the component to")
            return 2
        if self.FromStockStateCombobox == "":
            messagebox.showerror(message="Please Select a Stock State to transfer the component from")
            return 3
        if self.StockQuantitySpinbox.get() == "":
            messagebox.showerror(message="Please Select the quantity of components to transfer")
            return 4
        if not isinstance(eval(self.StockQuantitySpinbox.get()), int) or isinstance(eval(self.StockQuantitySpinbox.get()), float):
            messagebox.showerror(message="Please enter number in quantity")
            return 5
        if all(i != "" for i in [self.StockQuantitySpinbox.get(), self.FromStockStateCombobox.get(), self.ToStockStateCombobox.get(), self.ComponentNameComboBox.get()]):
            _change_quantity = self.StockQuantitySpinbox.get()
            _from_state = self.FromStockStateCombobox.get()
            _to_state = self.ToStockStateCombobox.get()
            if (_change_quantity > _to_state) and (_to_state != "in-stock"):
                messagebox.showinfo(message="done")
        else:
            messagebox.showerror(message="Please enter the necessary values")
            return 6





class ChangeProductStateWindow(ChangeStockStateWindow):
    def __init__(self, db_ops_obj):
        self.db_ops_obj = db_ops_obj
        super(ChangeProductStateWindow, self).__init__(stock_type_text="Component", db_ops_obj=db_ops_obj, table_name="ProductStock")
        _product_list = db_ops_obj.FetchAllProducts()
        _ = []
        for i in _product_list:
            _ += [i]
        self.FromStockStateCombobox["values"] = _



class ShowComponentStockTableWindow(DefaultValues):
    def __init__(self, db_cursor, db_ops_obj):
        super(ShowComponentStockTableWindow, self).__init__()
        self.db_cursor = db_cursor
        self.db_ops_obj = db_ops_obj

        self.ComponentStockTableWindow = Toplevel()
        self.ComponentStockTableWindow.title = "Component Stock Table"
        self.ComponentStockTableWindow.geometry("500x500")

        self.TopFrame = Frame(self.ComponentStockTableWindow)
        self.TopFrame.grid(column=0, row=0)
        self.BottomFrame = Frame(self.ComponentStockTableWindow)
        self.BottomFrame.grid(column=0, row=1)

        self.LabelFrame = Frame(self.TopFrame)
        self.LabelFrame.grid(column=0, row=0, pady=5)
        self.Button_Frame = Frame(self.TopFrame)
        self.Button_Frame.grid(column=0, row=1, pady=5)

        self.ChangeComponentStockStateWindowTitle = Label(self.LabelFrame, text="Component Stock Table")
        self.ChangeComponentStockStateWindowTitle.grid()

        self.AddRemoveButton = Button(self.Button_Frame, text="Add/Remove", command=lambda: AddRemoveComponentWindow(db_ops_obj=self.db_ops_obj))
        self.AddRemoveButton.grid(row=0, column=0, padx=10)

        self.ChangeStockStateBtn = Button(self.Button_Frame, text="Change Stock State", command=lambda: ChangeComponentStockStateWindow(
            db_ops_obj=self.db_cursor))
        self.ChangeStockStateBtn.grid(row=0, column=1, padx=10)

        self.RefreshInfoBtn = Button(self.Button_Frame, text="Refresh Info", command=lambda: ChangeComponentStockStateWindow(
            db_ops_obj=self.db_cursor))
        self.ChangeStockStateBtn.grid(row=0, column=2, padx=10)

        self.ComponentStockTabbedPaneFrame = Frame(self.BottomFrame)
        self.ComponentStockTabbedPaneFrame.grid(column=0, row=0)

        self.ComponentStockTabbedPane = Notebook(self.ComponentStockTabbedPaneFrame)
        self.ComponentStockTabbedPane.grid(row=1, column=0)
        available_component_list, defective_component_list, rejected_component_list, lost_component_list, out_of_stock_component_list = self.ComponentWindowTableData(db_cursor=self.db_cursor)

        self.AvailableTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"], data=available_component_list, align="center")
        self.DefectiveTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"], data=defective_component_list, align="center")
        self.RejectedTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"], data=rejected_component_list, align="center")
        self.LostTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"], data=lost_component_list, align="center")
        self.OutOfStockTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name"], data=out_of_stock_component_list, align="center")


        for object in [self.DefectiveTab, self.RejectedTab, self.LostTab, self.OutOfStockTab, self.AvailableTab]:
            object.set_options(expand_sheet_if_paste_too_big=True,
                               page_up_down_select_row=True,
                               show_horizontal_grid=True,
                               show_vertical_grid=True)

            object.set_all_cell_sizes_to_text()
            object.enable_bindings("all")


        self.DefectiveTab.pack(fill="both", expand=True)
        self.RejectedTab.pack(fill="both", expand=True)
        self.LostTab.pack(fill="both", expand=True)
        self.OutOfStockTab.pack(fill="both", expand=True)
        self.AvailableTab.pack(fill="both", expand=True)

        self.ComponentStockTabbedPane.add(self.AvailableTab, text="Available")
        self.ComponentStockTabbedPane.add(self.DefectiveTab, text="Defective")
        self.ComponentStockTabbedPane.add(self.RejectedTab, text="Rejected")
        self.ComponentStockTabbedPane.add(self.LostTab, text="Lost")
        self.ComponentStockTabbedPane.add(self.OutOfStockTab, text="Out Of Stock")
        self.ComponentStockTabbedPane.pack(expand=True, fill="both")

    def ComponentWindowTableData(self, db_cursor):
        try:
            db_cursor.execute("SELECT * FROM ComponentStock")
            cs_data_set_list = db_cursor.fetchall()

            db_cursor.execute("SELECT * FROM ComponentStockStateCount")
            cssc_data_set_list = db_cursor.fetchall()

            available_component_list = []
            rejected_component_list = []
            lost_component_list = []
            defective_component_list = []
            out_of_stock_component_list = []

            if cs_data_set_list is None or cssc_data_set_list is None:
                print("SHIIIIITTTTT NOOOOO")
            if (cs_data_set_list is not None) and (cssc_data_set_list is not None):
                print("NAAAAYEEEESSSS")
                '''
                    loop to display components in "in-stock", "defective", etc states in table
                '''
                for a in cssc_data_set_list:
                    _ComponentStockStateCount_ComponentCode = a[0]
                    db_cursor.execute(f"SELECT cs.Name FROM ComponentStockStateCount cssc, ComponentStock cs WHERE cssc.`Code` = cs.Code AND cs.Code = {_ComponentStockStateCount_ComponentCode}")
                    _ComponentStockStateCount_ComponentName = db_cursor.fetchall()[0][0]

                    _ComponentStockStateCount_in_stock_count = a[1]
                    _ComponentStockStateCount_rejected_count = a[2]
                    _ComponentStockStateCount_lost_count = a[3]
                    _ComponentStockStateCount_defective_count = a[4]

                    if _ComponentStockStateCount_in_stock_count > 0:
                        available_component_list += [(_ComponentStockStateCount_ComponentName, _ComponentStockStateCount_in_stock_count)]
                    if _ComponentStockStateCount_rejected_count > 0:
                        rejected_component_list += [(_ComponentStockStateCount_ComponentName, _ComponentStockStateCount_rejected_count)]
                    if _ComponentStockStateCount_lost_count > 0:
                        lost_component_list += [(_ComponentStockStateCount_ComponentName, _ComponentStockStateCount_lost_count)]
                    if _ComponentStockStateCount_defective_count > 0:
                        defective_component_list += [(_ComponentStockStateCount_ComponentName, _ComponentStockStateCount_defective_count)]

                    if (len(available_component_list) == 0) and (len(rejected_component_list) == 0) and (len(lost_component_list) == 0) and (len(defective_component_list) == 0):
                        out_of_stock_component_list += [_ComponentStockStateCount_ComponentName]
                    elif (len(available_component_list) != 0) and (len(rejected_component_list) != 0) and (len(lost_component_list) != 0) and (len(defective_component_list) != 0):
                        out_of_stock_component_list = [["all components in-stock"], []]

                return available_component_list, rejected_component_list, lost_component_list, defective_component_list, out_of_stock_component_list
        except Exception as e:
            print("WTF IS RONG WID DIS DB???? ", e)




class ShowProductStockTableWindow(DefaultValues):
    def __init__(self, db_cursor, db_ops_obj):
        super(ShowProductStockTableWindow, self).__init__()
        self.ProductStockTableWindow = Toplevel()
        self.ProductStockTableWindow.title = "Product Stock Table"
        self.ProductStockTableWindow.minsize(width=500, height=500)

        self.db_cursor = db_cursor
        self.db_ops_obj = db_ops_obj

        self.TitleFrame = Frame(self.ProductStockTableWindow)
        self.TitleFrame.grid(column=0, row=0)

        self.TableFrame = Frame(self.ProductStockTableWindow)
        self.TableFrame.grid(column=0, row=1)

        self.ButtonFrame = Frame(self.ProductStockTableWindow)
        self.ButtonFrame.grid(column=0, row=2)

        self.Title = Label(self.TitleFrame, text="Product Table")
        self.Title.grid()

        self.ProductTable = tksheet.Sheet(self.TableFrame, headers=["Name", "Count", "stock state"], data=self.ProductStockData(), show_horizontal_grid=True, expand_sheet_if_paste_too_big=True, show_vertical_grid=True)
        self.ProductTable.enable_bindings("all")
        self.ProductTable.edit_bindings(True)
        self.ProductTable.basic_bindings(enable=True)
        self.ProductTable.tk_focusFollowsMouse()

        self.ProductTable.grid(row=0, column=0, padx=10, pady=10)

        self.AddBtn = Button(self.ButtonFrame, text="Add-Product", command=lambda: self.AddProductWindow())
        self.RemBtn = Button(self.ButtonFrame, text="Remove-Product", command=lambda: self.RemoveProductWindow())
        self.ProductInfoBtn = Button(self.ButtonFrame, text="About-Product", command=lambda: self.ProductInfoPopup())
        self.DoneBtn = Button(self.ButtonFrame, text="Done", command=lambda: self.ProductStockTableWindow.destroy())
        self.AddBtn.grid(column=0, row=0)
        self.RemBtn.grid(column=1, row=0)
        self.ProductInfoBtn.grid(column=2, row=0)
        self.DoneBtn.grid(column=3, row=0)

    def ProductStockData(self):
        try:
            db_data_set_list = self.db_ops_obj.FetchAllProducts(getcount=True, getstockstate=True)
            self.data_list = []
            if db_data_set_list is None:
                print("SHIIIIITTTTT")
            if db_data_set_list is not None:
                for i in db_data_set_list:
                    _temp_data = list(i[0][:-1])
                    _stock_state = [i[1]]
                    self.data_list += [_temp_data + _stock_state]
                return self.data_list
        except Exception as e:
            print("WTF IS RONG WID DIS DB NOOOO 222222 BLAH BLAH???? ", e)

    def ProductInfoPopup(self):

        # scl - selected_cell_location
        scl = self.ProductTable.get_currently_selected()

        if scl == ():
            tkinter.messagebox.showwarning(message="Please select a product from the table")
            return

        scl = list(scl)
        scl[1] = 0  # used to select 1st column of arbitrarily selected cell

        selected_product = self.ProductTable.get_cell_data(r=scl[0], c=scl[1])
        # selected_product_info = self.db_ops.FetchComponentsPerProduct(select_cols=["selected_product"])
        selected_product_info = self.db_ops_obj.FetchComponentsPerProduct(conditional_query={"Name": f"'{selected_product}'"}, query_conditional_operator="AND")
        component_list = "component: component_count\n"

        ProductInfoWindow = Toplevel()
        ProductInfoWindow.title = "Product Info"

        for i in selected_product_info:
            component_list += f"{i}: {selected_product_info[i]}\n"

        WindowTitle = Label(ProductInfoWindow, text=f"About Product")
        ProductName = Label(ProductInfoWindow, text=f"Name: {selected_product}")
        ComponentList = Label(ProductInfoWindow, text=component_list)


        WindowTitle.grid(row=0, column=0, pady=5, padx=5)
        ProductName.grid(row=1, column=0, pady=5, padx=5)
        ComponentList.grid(row=2, column=0, pady=5, padx=5)


    def AddProductWindow(self):
        try:
            self.db_cursor.execute("SELECT Name FROM ComponentStock")
            self.component_name_list_for_product = self.db_cursor.fetchall()
            self._data_list = []
            for i in self.component_name_list_for_product:
                _ComponentName = i[0]
                self._data_list += [_ComponentName]
        except Exception as e:
            print(e)

        AddProductWindowObj = Toplevel()
        AddProductWindowObj.title = "Add Product"

        LeftFrame = Frame(AddProductWindowObj)
        MiddleFrame = Frame(AddProductWindowObj)
        RightFrame = Frame(AddProductWindowObj)

        LeftFrame.grid(row=0, column=0, padx=5, pady=5)
        MiddleFrame.grid(row=0, column=1, padx=5, pady=5)
        RightFrame.grid(row=0, column=2, padx=5, pady=5)


        ################ LEFT FRAME ######################
        LeftFrameLabel = Label(LeftFrame, text="Available Component Stock")
        AddStockListboxListVar = Variable(value=[])
        AvailableStockListbox = Listbox(LeftFrame, selectmode="multiple")
        ProcutNameEntryBox = Entry(LeftFrame)

        LeftFrameLabel.grid(row=0, column=0, padx=5, pady=5)
        AvailableStockListbox.grid(row=1, column=0, padx=5, pady=5)
        ProcutNameEntryBox.grid(row=2, column=0, padx=5, pady=5)
        for i in range(len(self._data_list)):
            AvailableStockListbox.insert(i, self._data_list[i])
        ##################################################################


        ################ MIDDLE FRAME ##################

        AddBtnIndexTuple = (Variable())
        RemBtnIndexTuple = (Variable())
        AddBtn = Button(MiddleFrame, text="->", command=lambda: MoveListItemsBtnCmd(AvailableStockListbox, AddStockListbox), textvariable=RemBtnIndexTuple)
        RemoveBtn = Button(MiddleFrame, text="<-", command=lambda: MoveListItemsBtnCmd(AddStockListbox, AvailableStockListbox), textvariable=AddBtnIndexTuple)
        ComponentCountSpinBox = Spinbox(MiddleFrame, width=6)

        AddBtn.grid(row=0, column=0, padx=5, pady=5)
        RemoveBtn.grid(row=1, column=0, padx=5, pady=5)
        ComponentCountSpinBox.grid(row=2, column=0, padx=5, pady=5)


        ################ RIGHT FRAME ##################
        RightFrameLabel = Label(RightFrame, text="Component Stock For Product")
        AddStockListbox = Listbox(RightFrame, selectmode="multiple", listvariable=AddStockListboxListVar)
        RightFrame_BtnFrame = Frame(RightFrame)
        AddButton = Button(RightFrame_BtnFrame, text="Add", command=lambda: AddProduct())
        DoneBtn = Button(RightFrame_BtnFrame, text="Done", command=lambda: AddProductWindowObj.destroy())

        RightFrameLabel.grid(row=0, column=0, padx=5, pady=5)
        AddStockListbox.grid(row=1, column=0, padx=5, pady=5)
        RightFrame_BtnFrame.grid(row=2, column=0, padx=1, pady=1)

        AddButton.grid(row=0, column=0, padx=5, pady=5)
        DoneBtn.grid(row=0, column=1, padx=5, pady=5)
        ##################################################################



        ##################################################################
        # Btn function to move items between lists in "Add Product Window"
        def MoveListItemsBtnCmd(from_list, to_list):
            if ComponentCountSpinBox.get() == 0 or ComponentCountSpinBox.get() == "":
                tkinter.messagebox.showwarning(message="Please enter a number greater than 0")
                return
            from_list_item = from_list.selection_get().split("\n")
            from_list_item_index = from_list.curselection()
            for i, j in zip(from_list_item_index, range(1, len(from_list_item_index) + 1)):
                to_list.insert(j, from_list.get(from_list.index(i)))
                # print(from_list.get(from_list.index(i)))

            from_list_item_index_rev = from_list_item_index[::-1]

            for i in from_list_item_index_rev:
                from_list.delete(i)
                # print(from_list.get(from_list.index(i)))

            return from_list_item_index_rev

        def AddProduct():
            AddStockListboxComponentList = AddStockListboxListVar.get()
            ProcutName = ProcutNameEntryBox.get()

            if (AddStockListboxComponentList == () or AddStockListboxComponentList == "") and ProcutName == "":
                tkinter.messagebox.showwarning(message="Components not selected and product name not Entered")
                return
            if (AddStockListboxComponentList == () or AddStockListboxComponentList == "") and ProcutName != "":
                tkinter.messagebox.showwarning(message="Components not selected for product")
                return
            if (AddStockListboxComponentList != () or AddStockListboxComponentList != "") and ProcutName == "":
                tkinter.messagebox.showwarning(message="Product Name not Entered")
                return
            if (AddStockListboxComponentList != () or AddStockListboxComponentList != "") and ProcutName != "":
                print(AddStockListboxComponentList)  # tuple
                print(ProcutName)  # string
            _ComponentCount = ComponentCountSpinBox.get()
            _components_dict = {}
            for i in AddStockListboxComponentList:
                _ = self.db_ops_obj.FetchComponent(component_name=i)
                _name = _[0][0]
                _code = f"_{_[0][1]}"
                _components_dict.update({ _code: _ComponentCount})

            self.db_ops_obj.AddColumn()



    def RemoveProductWindow(self):
        RemoveProductWindow = Toplevel()
        RemoveProductWindow.title = "Remove Product"
        RemoveProductWindow.minsize(width=800, height=600)

        TopFrame = Frame(RemoveProductWindow)
        TopFrame.grid(row=0, column=0, padx=5, pady=5)
        BottomFrame = Frame(RemoveProductWindow)
        BottomFrame.grid(row=1, column=0, padx=5, pady=5)

        Title = Label(BottomFrame, text="Remove Product")
        Title.grid(row=0, column=0, padx=5, pady=5)

        ProductTable = tksheet.Sheet(BottomFrame, headers=["Product Name"], data=self.ProductStockData(), show_horizontal_grid=True, expand_sheet_if_paste_too_big=True, show_vertical_grid=True)
        BtnsFrame = Frame(BottomFrame)
        ProductTable.grid(row=0, column=0, padx=5, pady=5)
        BtnsFrame.grid(row=0, column=1, padx=5, pady=5)


        RemoveSelectedBtn = Button(BtnsFrame, text="Remove Selected", width=16)
        RemoveUnselectedBtn = Button(BtnsFrame, text="Remove Unselected", width=16)
        SelectAllBtn = Button(BtnsFrame, text="Select All", width=16)
        UnselectAllBtn = Button(BtnsFrame, text="Unselect All", width=16)
        InvertSelectionBtn = Button(BtnsFrame, text="Invert Selection", width=16)
        DoneBtn = Button(BtnsFrame, text="Done", width=16, command=lambda: RemoveProductWindow.destroy())
        RemoveSelectedBtn.grid(row=0, column=0, padx=5, pady=5)
        RemoveUnselectedBtn.grid(row=0, column=1, padx=5, pady=5)
        SelectAllBtn.grid(row=1, column=0, padx=5, pady=5)
        UnselectAllBtn.grid(row=1, column=1, padx=5, pady=5)
        InvertSelectionBtn.grid(row=2, column=0, padx=5, pady=5)
        DoneBtn.grid(row=2, column=1, padx=5, pady=5)


