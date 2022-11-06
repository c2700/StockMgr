from tkinter.ttk import *
import tksheet
from baseclasses import *
from tkinter import *

class StockManager():
    def __init__(self, MainWindow):
        MainWindow.title("Stock Manager")
        MainWindow.geometry("1200x700")

        # create table object with attributes
        self.MainWindowTable = tksheet.Sheet(MainWindow, headers=["Product", "count"], show_horizontal_grid=True,
                                             expand_sheet_if_paste_too_big=True, show_vertical_grid=True)

        # frame for buttons to control table view
        self.MainWindowButtonsLayout = Frame(MainWindow)

        # placing frames & sheet object in window
        self.MainWindowTable.grid(row=0, column=0, padx=10, pady=10)
        self.MainWindowButtonsLayout.grid(row=0, column=1, pady=(0, 150))

        # creating buttons in table view frame
        self.AddRemComponentBtn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Component", command=lambda: AddRemoveComponentWindow()).grid(row=0, column=0, padx=5, pady=5)
        self.AddRemProductBTn = Button(self.MainWindowButtonsLayout, width=30, text="Add/Remove Product", command=lambda: AddRemoveProductWindow()).grid(row=0, column=1, padx=5, pady=5)
        self.ChangeComponentStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Component Stock State", command=lambda: ChangeComponentStockStateWindow()).grid(row=1, column=0, padx=5, pady=5)
        self.ChangeProductStockStateBTn = Button(self.MainWindowButtonsLayout, width=30, text="Change Product Stock State", command=lambda: ChangeProductStateWindow()).grid(row=1, column=1, padx=5, pady=5)

        self.ShowStockTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Component Stock Table", command=lambda: ShowComponentStockTableWindow()).grid(row=2, column=0, padx=5, pady=5)
        self.ShowProductTableBTn = Button(self.MainWindowButtonsLayout, width=30, text="Show Product Stock Table", command=lambda: ShowProductStockTableWindow()).grid(row=2, column=1, padx=5, pady=5)
        self.SearchComponentEntry = Entry(self.MainWindowButtonsLayout, width=30, name="search_component_stock_entry").grid(row=4, column=1, ipadx=10, ipady=5)
        self.SearchComponentBTn = Button(self.MainWindowButtonsLayout, width=12, text="Search", command=lambda: SearchWindow()).grid(row=4, column=0, padx=35, pady=5, ipadx=10)

class AddRemoveComponentWindow(AddRemoveWindow):
    def __init__(self):
        super(AddRemoveComponentWindow, self).__init__("Component")

class AddRemoveProductWindow(AddRemoveWindow):
    def __init__(self):
        super(AddRemoveProductWindow, self).__init__("Product")

class ChangeComponentStockStateWindow(ChangeStockStateWindow):
    def __init__(self):
        super(ChangeComponentStockStateWindow, self).__init__("component")

class ChangeProductStateWindow(ChangeStockStateWindow):
    def __init__(self):
        super(ChangeProductStateWindow, self).__init__("component")

class ShowComponentStockTableWindow():
    def __init__(self):
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

        self.AddRemoveButton = Button(self.Button_Frame, text="Add/Remove")
        self.AddRemoveButton.grid(row=0, column=0, padx=10)

        self.ChangeStockStateBtn = Button(self.Button_Frame, text="Change Stock State")
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
    def __init__(self):
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

        self.AddBtn = Button(self.ButtonFrame, text="Add-Product")
        self.AddBtn.grid(column=0, row=0)
        self.RemBtn = Button(self.ButtonFrame, text="Remove-Product")
        self.RemBtn.grid(column=1, row=0)
        self.ProductInfoBtn = Button(self.ButtonFrame, text="About-Product")
        self.ProductInfoBtn.grid(column=2, row=0)

class SearchWindow():
    def __init__(self):
        self.SearchPopupWindow = Toplevel()
        self.SearchPopupWindow.title = "Search Result"

        self.SearchPopupWindow.minsize(height=100, width=200)

        self.SearchString = Label(self.SearchPopupWindow, text="Found Component")
        self.SearchString.grid(row=0, column=0, pady=10, padx=10)
