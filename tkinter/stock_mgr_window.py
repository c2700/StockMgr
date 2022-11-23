from tkinter.ttk import *
import tksheet
from baseclasses import *
from tkinter import *
from sqlite3 import *


class StockManager:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow


        self.db_conn_obj = None
        try:

            self.db_conn_obj = connect("StockData.sqlite3")
            print("fuck yea")
        except:
            print("WTF IS RONG IS WID DIS MACHINE.....AAAGGGHHHH")


        self.MainWindow.title("Stock Manager")
        self.MainWindow.geometry("1200x700")

        # create table object with attributes
        self.MainWindowTable = tksheet.Sheet(self.MainWindow, headers=["Product", "count"], show_horizontal_grid=True,
                                             expand_sheet_if_paste_too_big=True, show_vertical_grid=True)
        self.MainWindowButtonsLayout = Frame(self.MainWindow)

        # placing frames & sheet object in window
        self.MainWindowTable.grid(row=0, column=0, padx=10, pady=10)
        self.MainWindowButtonsLayout.grid(row=0, column=1, pady=(0, 150))

        # creating buttons in table view frame
        self.AddRemComponentBtn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Component", command=lambda: AddRemoveComponentWindow(db_conn_obj=self.db_conn_obj))
        self.AddRemProductBTn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Product", command=lambda: AddRemoveProductWindow(db_conn_obj=self.db_conn_obj))
        self.ChangeComponentStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Component Stock State", command=lambda: ChangeComponentStockStateWindow(db_conn_obj=self.db_conn_obj))
        self.ChangeProductStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Product Stock State", command=lambda: ChangeProductStateWindow(db_conn_obj=self.db_conn_obj))
        self.ShowStockTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Component Stock Table", command=lambda: ShowComponentStockTableWindow(db_conn_obj=self.db_conn_obj))
        self.ShowProductTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Product Stock Table", command=lambda: ShowProductStockTableWindow(db_conn_obj=self.db_conn_obj))
        self.SearchComponentEntry = Entry(self.MainWindowButtonsLayout, width=30, name="search_component_stock_entry")
        self.SearchComponentBTn = Button(self.MainWindowButtonsLayout, width=12, text="Search", command=lambda: self.SearchWindow())

        # arraning ui elements
        self.AddRemComponentBtn.grid(row=0, column=0, padx=5, pady=5)
        self.AddRemProductBTn.grid(row=0, column=1, padx=5, pady=5)
        self.ChangeComponentStockStateBTn.grid(row=1, column=0, padx=5, pady=5)
        self.ChangeProductStockStateBTn.grid(row=1, column=1, padx=5, pady=5)
        self.ShowStockTableBTn.grid(row=2, column=0, padx=5, pady=5)
        self.ShowProductTableBTn.grid(row=2, column=1, padx=5, pady=5)
        self.SearchComponentEntry.grid(row=4, column=1, ipadx=10, ipady=5)
        self.SearchComponentBTn.grid(row=4, column=0, padx=35, pady=5, ipadx=10)

    def CloseApp(self):
        try:
            self.db_conn_obj.close()
            print("HOLY SHIT IT WORX")
        except:
            pass
        self.MainWindow.destroy()

    def SearchWindow(self):
        SearchPopupWindow = Toplevel()
        SearchPopupWindow.title = "Search Result"
        SearchPopupWindow.minsize(height=100, width=200)
        SearchString = Label(SearchPopupWindow, text="Found Component")
        SearchString.grid(row=0, column=0, pady=10, padx=10)


class AddRemoveComponentWindow(AddRemoveWindow):
    def __init__(self, db_conn_obj):
        super(AddRemoveComponentWindow, self).__init__(title_text="Component", db_conn_obj=db_conn_obj, table_name="ComponentStock")


class AddRemoveProductWindow(AddRemoveWindow):
    def __init__(self, db_conn_obj):
        super(AddRemoveProductWindow, self).__init__(title_text="Product", db_conn_obj=db_conn_obj, table_name="ProductStock")


class ChangeComponentStockStateWindow(ChangeStockStateWindow):
    def __init__(self, db_conn_obj):
        super(ChangeComponentStockStateWindow, self).__init__(stock_type_text="component", db_conn_obj=db_conn_obj, table_name="ComponentStock")


class ChangeProductStateWindow(ChangeStockStateWindow):
    def __init__(self, db_conn_obj):
        super(ChangeProductStateWindow, self).__init__(stock_type_text="component", db_conn_obj=db_conn_obj, table_name="ProductStock")


class ShowComponentStockTableWindow():
    def __init__(self, db_conn_obj):
        self.db_conn_obj = db_conn_obj
        self.ComponentStockTableWindow = Toplevel()
        self.ComponentStockTableWindow.title = "Component Stock Table"
        self.ComponentStockTableWindow.geometry("500x500")

        self.TopFrame = Frame(self.ComponentStockTableWindow)
        self.TopFrame.grid(column=0, row=0)
        self.BottomFrame = Frame(self.ComponentStockTableWindow)
        self.BottomFrame.grid(column=0, row=1)

        self.Label_Frame = Frame(self.TopFrame)
        self.Label_Frame.grid(column=0, row=0, pady=5)
        self.Button_Frame = Frame(self.TopFrame)
        self.Button_Frame.grid(column=0, row=1, pady=5)

        self.ChangeComponentStockStateWindowTitle = Label(self.Label_Frame, text="Component Stock Table")
        self.ChangeComponentStockStateWindowTitle.grid()

        self.AddRemoveButton = Button(self.Button_Frame, text="Add/Remove", command=lambda: AddRemoveComponentWindow())
        self.AddRemoveButton.grid(row=0, column=0, padx=10)

        self.ChangeStockStateBtn = Button(self.Button_Frame, text="Change Stock State", command=lambda: ChangeComponentStockStateWindow())
        self.ChangeStockStateBtn.grid(row=0, column=1, padx=10)

        self.ComponentStockTabbedPaneFrame = Frame(self.BottomFrame)
        self.ComponentStockTabbedPaneFrame.grid(column=0, row=0)

        self.ComponentStockTabbedPane = Notebook(self.ComponentStockTabbedPaneFrame)
        self.ComponentStockTabbedPane.grid(row=1, column=0)

        self.DefectiveTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"])
        self.RejectedTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"])
        self.LostTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"])
        self.OutOfStockTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"])
        self.AvailableTab = tksheet.Sheet(self.ComponentStockTabbedPane, headers=["Name", "Count"])

        self.DefectiveTab.pack(fill="both", expand=True)
        self.RejectedTab.pack(fill="both", expand=True)
        self.LostTab.pack(fill="both", expand=True)
        self.OutOfStockTab.pack(fill="both", expand=True)
        self.AvailableTab.pack(fill="both", expand=True)

        self.ComponentStockTabbedPane.add(self.DefectiveTab, text="Defective")
        self.ComponentStockTabbedPane.add(self.RejectedTab, text="Rejected")
        self.ComponentStockTabbedPane.add(self.LostTab, text="Lost")
        self.ComponentStockTabbedPane.add(self.OutOfStockTab, text="Out Of Stock")
        self.ComponentStockTabbedPane.add(self.AvailableTab, text="Available")

        self.ComponentStockTabbedPane.pack(expand=True, fill="both")


class ShowProductStockTableWindow():
    def __init__(self, db_conn_obj):
        self.db_conn_obj = db_conn_obj
        self.ProductStockTableWindow = Toplevel()
        self.ProductStockTableWindow.title = "Product Stock Table"
        self.ProductStockTableWindow.minsize(width=500, height=500)

        self.TitleFrame = Frame(self.ProductStockTableWindow)
        self.TitleFrame.grid(column=0, row=0)

        self.TableFrame = Frame(self.ProductStockTableWindow)
        self.TableFrame.grid(column=0, row=1)

        self.ButtonFrame = Frame(self.ProductStockTableWindow)
        self.ButtonFrame.grid(column=0, row=2)

        self.Title = Label(self.TitleFrame, text="Product Table")
        self.Title.grid()

        self.ProductTable = tksheet.Sheet(self.TableFrame, headers=["Name", "Count", "stock state"])
        self.ProductTable.grid(row=0, column=0, padx=10, pady=10)

        self.AddBtn = Button(self.ButtonFrame, text="Add-Product", command=lambda: self.AddProductWindow())
        self.RemBtn = Button(self.ButtonFrame, text="Remove-Product", command=lambda: self.RemoveProductWindow())
        self.ProductInfoBtn = Button(self.ButtonFrame, text="About-Product", command=lambda: self.ProductInfoPopup())
        self.AddBtn.grid(column=0, row=0)
        self.RemBtn.grid(column=1, row=0)
        self.ProductInfoBtn.grid(column=2, row=0)

    def ProductInfoPopup(self):

        ProductInfoWindow = Toplevel()
        ProductInfoWindow.title = "Product Info"

        WindowTitle = Label(ProductInfoWindow, text="About Product")
        ProductName = Label(ProductInfoWindow, text="Name: Name")
        ComponentList = Label(ProductInfoWindow, text="component_list: List - count")

        WindowTitle.grid(row=0, column=0, pady=5, padx=5)
        ProductName.grid(row=1, column=0, pady=5, padx=5)
        ComponentList.grid(row=2, column=0, pady=5, padx=5)

    def AddProductWindow(self):
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
        AddStockListbox = Listbox(LeftFrame)
        ProcutNameEntryBox = Entry(LeftFrame)

        LeftFrameLabel.grid(row=0, column=0, padx=5, pady=5)
        AddStockListbox.grid(row=1, column=0, padx=5, pady=5)
        ProcutNameEntryBox.grid(row=2, column=0, padx=5, pady=5)
        ##################################################################


        ################ MIDDLE FRAME ##################
        AddBtn = Button(MiddleFrame, text="->")
        RemoveBtn = Button(MiddleFrame, text="<-")
        ComponentCountSpinBox = Spinbox(MiddleFrame, width=6)

        AddBtn.grid(row=0, column=0, padx=5, pady=5)
        RemoveBtn.grid(row=1, column=0, padx=5, pady=5)
        ComponentCountSpinBox.grid(row=2, column=0, padx=5, pady=5)
        ##################################################################


        ################ RIGHT FRAME ##################
        RightFrameLabel = Label(RightFrame, text="Component Stock For Product")
        RemoveStockListbox = Listbox(RightFrame)
        DoneBtn = Button(RightFrame, text="Done", command=lambda: AddProductWindowObj.destroy())

        RightFrameLabel.grid(row=0, column=0, padx=5, pady=5)
        RemoveStockListbox.grid(row=1, column=0, padx=5, pady=5)
        DoneBtn.grid(row=2, column=0, padx=5, pady=5)
        ##################################################################

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

        ProductTable = tksheet.Sheet(BottomFrame, headers=["Product Name"])
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


