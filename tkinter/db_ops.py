class DBops:
    def __init__(self, conn_obj):
        self.conn_obj = conn_obj

    ### Fetch operations
    def FetchProduct(self, product_name, getcount=False, getstockstate=False):
        query = f"SELECT Name FROM ProductStock WHERE Name = {product_name}"
        if (getcount is True) and (getstockstate is False):
            query = "SELECT Name,Count FROM ProductStock WHERE Name = " + product_name
        if (getcount is True) and (getstockstate is True):
            query = "SELECT * FROM ProductStock WHERE Name = " + product_name
        print(query)
        # self.conn_obj.execute(query)

    def FetchAllProducts(self, getcount=False, getstockstate=False):
        query = "SELECT Name FROM ProductStock"
        if (getcount is True) and (getstockstate is False):
            query += "Name,Count FROM ProductStock"
        if (getcount is True) and (getstockstate is True):
            query += "* FROM ProductStock"
        print(query)
        # self.conn_obj.execute(query)

    def FetchComponentsPerProduct(self, product_name):
        query = ""
        # self.conn_obj.execute(query)
        print(query)

    def FetchComponent(self, component_name, getcount=False, getstockstate=False):
        query = f"SELECT Name FROM ComponentStock WHERE Name = {component_name}"
        if (getcount is True) and (getstockstate is False):
            query = f"SELECT Name,Count FROM ComponentStock WHERE Name = {component_name}"
        if (getcount is True) and (getstockstate is True):
            query = f"SELECT * FROM ComponentStock WHERE Name = {component_name}"
        print(query)
        # self.conn_obj.execute(query)

    def FetchAllComponents(self, getcount=False, getstockstate=False):
        query = "SELECT Name FROM ComponentStock"
        if (getcount is True) and (getstockstate is False):
            query = "SELECT Name,Count FROM ComponentStock"
        if (getcount is True) and (getstockstate is True):
            query = "SELECT * FROM ComponentStock"
        print(query)
        # self.conn_obj.execute(query)


    ### db manip operations
    def AddColumn(self, table_name, column_name, **kwargs):
        query = f"ALTER TABLE {table_name} ADD {column_name} TEXT"
        print(query)
        # self.conn_obj.execute(query)

    def RemoveColumn(self, table_name, column_name, **kwargs):
        if ("count" in kwargs) and (int(str(kwargs["count"])) == 0 or str(kwargs["count"]) == ""):
            pass
        query = ""
        print(query)
        # self.conn_obj.execute(query)

    def AddRow(self, table_name, Name, **kwargs):
        Name = f"'{str(Name)}'"
        stock_state = "1"
        NameCount = "0"

        if ("NameCount" in kwargs) and (int(str(kwargs["NameCount"])) == 0 or str(kwargs["NameCount"]) == ""):
            NameCount = str(kwargs["NameCount"])
            stock_state = "0"

        query = f"INSERT INTO TABLE {table_name} VALUES({Name}, {NameCount}, {stock_state})"
        print(query)
        # self.conn_obj.execute(query)

    def RemoveRow(self, table_name, Name):
        query = f"DELETE FROM {table_name} WHERE Name = {Name}"
        print(query)
        # self.conn_obj.execute(query)

    def UpdateValue(self, table_name, **kwargs):
        query = f"UPDATE {table_name} SET "

        if ["CurrentName", "NewName"] in kwargs and "NewNameCount" not in kwargs:
            CurrentName = kwargs["CurrentName"]
            NewName = kwargs["NewName"]
            query += f"Name = {NewName} WHERE Name = {CurrentName}"

        if ["CurrentName", "NewName", "NewNameCount"] in kwargs:
            CurrentName = kwargs["CurrentName"]
            NewName = kwargs["NewName"]
            NewNameCount = kwargs["NewNameCount"]
            query += f"Name = {CurrentName}, NameCount = {NewNameCount} WHERE Name = {NewName}"

        if ["CurrentName", "NewName", "NewNameCount"] in kwargs and "NewNameCount" not in kwargs:
            CurrentName = kwargs["CurrentName"]
            CurrentNameCount = kwargs["NewNameCount"]
            NewName = kwargs["NewName"]
            NewNameCount = kwargs["NewNameCount"]
            query += f"Name = {CurrentName}, NameCount = {NewNameCount} WHERE Name = {NewName} AND NameCount = {CurrentNameCount}"  # NOQA: E501
        print(query)
        # self.conn_obj.execute(query)

