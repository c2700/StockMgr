class DBops:
    def __init__(self, conn_obj):
        self.conn_obj = conn_obj

    ### Fetch operations
    def FetchProduct(self, product_name, getcount=False, getstockstate=False):
        query = "SELECT Name FROM ProductStock WHERE Name = " + product_name
        if getcount == True and getstockstate == False:
            query = "SELECT Name,Count FROM ProductStock WHERE Name = " + product_name
        if getcount == True and getstockstate == True:
            query = "SELECT * FROM ProductStock WHERE Name = " + product_name
        self.conn_obj.execute(query)

    def FetchAllProducts(self, component_name, getcount=False, getstockstate=False):
        query = "SELECT Name FROM ProductStock"
        if getcount == True and getstockstate == False:
            query = "SELECT Name,Count FROM ProductStock"
        if getcount == True and getstockstate == True:
            query = "SELECT * FROM ProductStock"
        self.conn_obj.execute(query)

    def FetchComponentsPerProduct(self, product_name):
        query = ""
        self.conn_obj.execute(query)

    def FetchComponent(self, component_name, getcount=False, getstockstate=False):
        query = "SELECT Name FROM ComponentStock WHERE Name = " + component_name
        if getcount == True and getstockstate == False:
            query = "SELECT Name,Count FROM ComponentStock WHERE Name = " + component_name
        if getcount == True and getstockstate == True:
            query = "SELECT * FROM ComponentStock WHERE Name = " + component_name
        self.conn_obj.execute(query)

    def FetchAllComponents(self, getcount=False, getstockstate=False):
        query = "SELECT Name FROM ComponentStock"
        if getcount == True and getstockstate == False:
            query = "SELECT Name,Count FROM ComponentStock"
        if getcount == True and getstockstate == True:
            query = "SELECT * FROM ComponentStock"
        self.conn_obj.execute(query)



    ### db manip operations

    def AddTableColumn(self, table_name, column_name, count):
        query = ""
        self.conn_obj.execute(query)

    def RemoveTableColumn(self, table_name, column_name, count):
        query = ""
        self.conn_obj.execute(query)

    def AddTableRow(self, table_name, Name, NameCount):
        query = "INSERT INTO TABLE " + table_name + "VALUES(" + str(Name) + str(NameCount) + ")"
        self.conn_obj.execute(query)

    def RemoveTableRow(self, table_name, Name, NameCount):
        query = "DELETE FROM TABLE " + table_name + "WHERE "
        if str(NameCount) == "0" or str(NameCount) == "all" or str(NameCount) == "*" or str(NameCount) == "":
            query = query + "NAME = " + str(Name)
        if str(NameCount) > "0":
            query = query + "NAME = " + str(Name) + " AND Number = " + str(NameCount)
        self.conn_obj.execute(query)
