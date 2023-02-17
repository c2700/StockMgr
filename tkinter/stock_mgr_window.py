import re
import tkinter.messagebox
from tkinter.ttk import *

import mariadb
import tksheet
from tkinter import *
from mariadb import connect
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
                                           unix_socket="/home/blank/Projects/Hari_stock_mgmnt/StockMgr/tkinter/db/mysqld.sock")
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
        except mariadb.Error as e:
            print("WTF????? AAAAHHHHH IS D FUCKING SERVICE UP & RUNNING!!??????", e)
            exit(1)

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
        self.AddRemComponentBtn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Component", command=lambda: AddRemoveComponentWindow(db_cursor=self.db_cursor))
        self.AddRemProductBTn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Product", command=lambda: AddRemoveProductWindow(db_cursor=self.db_cursor))
        self.ChangeComponentStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Component Stock State", command=lambda: ChangeComponentStockStateWindow(db_cursor=self.db_cursor))
        self.ChangeProductStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Product Stock State", command=lambda: ChangeProductStateWindow(db_cursor=self.db_cursor))
        self.ShowStockTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Component Stock Table", command=lambda: ShowComponentStockTableWindow(db_cursor=self.db_cursor))
        self.ShowProductTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Product Stock Table", command=lambda: ShowProductStockTableWindow(db_cursor=self.db_cursor))
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

    def MainWindowTableData(self):
        try:
            db_data_set_list = [self.db_ops.FetchAllProducts(getcount=True, getstockstate=True)]
            data_list = []
            if db_data_set_list is None:
                print("SHIIIIITTTTT")
            if db_data_set_list is not None:
                for i in db_data_set_list[0]:
                    temp_data_list = list(i)
                    stock_state = 0 if temp_data_list[2] > 0 else 1
                    temp_data_list[2] = self.stock_state_dict[int(stock_state)]
                    data_list += [temp_data_list]
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

            name = None
            code = None
            count = None
            result = None

            if re.search('^[0-9]*$', SearchComponentEntryValue):
                result = self.db_ops.FetchComponent(getcount=True, getstockstate=True, component_code=SearchComponentEntryValue)
            if re.search('[a-zA-Z]+[0-9]+', SearchComponentEntryValue):
                result = self.db_ops.FetchComponent(getcount=True, getstockstate=True, component_name=SearchComponentEntryValue)

            if result == 2:
                tkinter.messagebox.showwarning(message=f"Component does not exist")
                return

            name = result[0][0][0]
            code = result[0][0][1]
            count = result[0][0][2]
            stock_state = result[1]

            ComponentInfoLabel = f"Component Name: {name}\nComponent Count: {count}\nStock State: {stock_state}"
            # tkinter.messagebox.showinfo(message=ComponentInfoLabel)
            SearchString = Label(SearchPopupWindow, text=ComponentInfoLabel)
            SearchString.grid(row=0, column=0, pady=10, padx=10)


class AddRemoveComponentWindow(AddRemoveWindow):
    def __init__(self, db_cursor):
        super(AddRemoveComponentWindow, self).__init__(title_text="Component", db_cursor=db_cursor, table_name="ComponentStock")



class AddRemoveProductWindow(AddRemoveWindow):
    def __init__(self, db_cursor):
        super(AddRemoveProductWindow, self).__init__(title_text="Product", db_cursor=db_cursor, table_name="ProductStock")


class ChangeComponentStockStateWindow(ChangeStockStateWindow):
    def __init__(self, db_cursor):
        super(ChangeComponentStockStateWindow, self).__init__(stock_type_text="Component", db_conn_obj=db_cursor, table_name="ComponentStock")


class ChangeProductStateWindow(ChangeStockStateWindow):
    def __init__(self, db_cursor):
        super(ChangeProductStateWindow, self).__init__(stock_type_text="Component", db_conn_obj=db_cursor, table_name="ProductStock")


class ShowComponentStockTableWindow(DefaultValues):
    def __init__(self, db_cursor):
        super(ShowComponentStockTableWindow, self).__init__()
        self.db_conn_obj = db_cursor

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

        self.AddRemoveButton = Button(self.Button_Frame, text="Add/Remove", command=lambda: AddRemoveComponentWindow(db_cursor=self.db_conn_obj))
        self.AddRemoveButton.grid(row=0, column=0, padx=10)

        self.ChangeStockStateBtn = Button(self.Button_Frame, text="Change Stock State", command=lambda: ChangeComponentStockStateWindow(db_cursor=self.db_conn_obj))
        self.ChangeStockStateBtn.grid(row=0, column=1, padx=10)

        self.RefreshInfoBtn = Button(self.Button_Frame, text="Refresh Info", command=lambda: ChangeComponentStockStateWindow(db_cursor=self.db_conn_obj))
        self.ChangeStockStateBtn.grid(row=0, column=2, padx=10)

        self.ComponentStockTabbedPaneFrame = Frame(self.BottomFrame)
        self.ComponentStockTabbedPaneFrame.grid(column=0, row=0)

        self.ComponentStockTabbedPane = Notebook(self.ComponentStockTabbedPaneFrame)
        self.ComponentStockTabbedPane.grid(row=1, column=0)
        available_component_list, defective_component_list, rejected_component_list, lost_component_list, out_of_stock_component_list = self.ComponentWindowTableData(db_cursor=self.db_conn_obj)

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
                    db_cursor.execute(f"SELECT cs.Name FROM ComponentStockStateCount cssc, ComponentStock cs WHERE cssc.`Component Code` = cs.Code AND cs.Code = {_ComponentStockStateCount_ComponentCode}")
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
    def __init__(self, db_cursor):
        super(ShowProductStockTableWindow, self).__init__()
        self.ProductStockTableWindow = Toplevel()
        self.ProductStockTableWindow.title = "Product Stock Table"
        self.ProductStockTableWindow.minsize(width=500, height=500)

        self.db_cursor = db_cursor
        self.db_ops = DBops(self.db_cursor)

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
        self.AddBtn.grid(column=0, row=0)
        self.RemBtn.grid(column=1, row=0)
        self.ProductInfoBtn.grid(column=2, row=0)

    def ProductStockData(self):
        try:
            db_data_set_list = self.db_ops.FetchAllProducts(getcount=True, getstockstate=True)
            self.data_list = []
            if db_data_set_list is None:
                print("SHIIIIITTTTT")
            if db_data_set_list is not None:
                for i in db_data_set_list:
                    temp_data_list = list(i)
                    stock_state = 0 if temp_data_list[2] > 0 else 1
                    temp_data_list[2] = self.stock_state_dict[int(stock_state)]
                    self.data_list += [temp_data_list]
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
        selected_product_info = self.db_ops.FetchComponentsPerProduct(selected_product)
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
        AddBtn = Button(MiddleFrame, text="->", command=lambda: MoveListItemsBtnCmd(AvailableStockListbox, AddStockListbox), textvariable=AddBtnIndexTuple)
        RemoveBtn = Button(MiddleFrame, text="<-", command=lambda: MoveListItemsBtnCmd(AddStockListbox, AvailableStockListbox), textvariable=RemBtnIndexTuple)
        ComponentCountSpinBox = Spinbox(MiddleFrame, width=6)

        AddBtn.grid(row=0, column=0, padx=5, pady=5)
        RemoveBtn.grid(row=1, column=0, padx=5, pady=5)
        ComponentCountSpinBox.grid(row=2, column=0, padx=5, pady=5)


        ################ RIGHT FRAME ##################
        RightFrameLabel = Label(RightFrame, text="Component Stock For Product")
        AddStockListbox = Listbox(RightFrame, selectmode="multiple", listvariable=AddStockListboxListVar)
        DoneBtn = Button(RightFrame, text="Done", command=lambda: DestroyWindow())
        CancelButton = Button(RightFrame, text="cancel", command=lambda: AddProductWindowObj.destroy())

        RightFrameLabel.grid(row=0, column=0, padx=5, pady=5)
        AddStockListbox.grid(row=1, column=0, padx=5, pady=5)
        DoneBtn.grid(row=2, column=0, padx=1, pady=1)
        CancelButton.grid(row=3, column=0, ipadx=5, pady=5)
        ##################################################################



        ##################################################################
        # Btn function to move items between lists in "Add Product Window"
        def MoveListItemsBtnCmd(from_list, to_list):
            from_list_item = from_list.selection_get().split("\n")
            from_list_item_index = from_list.curselection()
            for i, j in zip(from_list_item_index, range(1, len(from_list_item_index) + 1)):
                print(from_list.get(from_list.index(i)))
                to_list.insert(j, from_list.get(from_list.index(i)))

            from_list_item_index_rev = from_list_item_index[::-1]

            for i in from_list_item_index_rev:
                print(from_list.get(from_list.index(i)))
                from_list.delete(i)

            return from_list_item_index_rev

        def DestroyWindow():
            if AddStockListboxListVar.get() != () and ProcutNameEntryBox.get() != "":
                AddProductWindowObj.destroy()
            if AddStockListboxListVar.get() == () and ProcutNameEntryBox.get() == "":
                tkinter.messagebox.showwarning(message="Components not selected and product name not Entered")
            if AddStockListboxListVar.get() == () and ProcutNameEntryBox.get() != "":
                tkinter.messagebox.showwarning(message="Components not selected for product")
            if AddStockListboxListVar.get() != () and ProcutNameEntryBox.get() == "":
                tkinter.messagebox.showwarning(message="Product Name not Entered")

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


