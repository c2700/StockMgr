import re

import mariadb


class DBops:
    def __init__(self, db_cursor):
        self.db_cursor = db_cursor
        self.fetched_db_data_list = []

    ### Fetch operations=s
    def FetchProduct(self, product_name, getcount=False, getstockstate=False):
        query = f"SELECT Name FROM ProductStock WHERE Name = {product_name}"
        if (getcount is True) and (getstockstate is False):
            query = f"SELECT Name,Count FROM ProductStock WHERE Name = {product_name}"
        if (getcount is True) and (getstockstate is True):
            query = f"SELECT * FROM ProductStock WHERE Name = {product_name}"
        # print(query)
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()


    def FetchAllProducts(self, getcount=False, getstockstate=False):
        query = "SELECT "
        if (getcount is False) and (getstockstate is False):
            query += "Name"
        if (getcount is True) and (getstockstate is False):
            query += "Name,Count"
        if (getcount is True) and (getstockstate is True):
            query += "*"
        query += " FROM ProductStock"
        print(query)
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list


    def FetchComponentsPerProduct(self, ProductName):
        # SET @var=(SELECT `Product Code` FROM ComponentsPerProduct WHERE `Product Code` = 653);
        # self.db_cursor.execute("SELECT Name FROM ")
        _component_list = []
        for i in self.FetchAllComponents(Name=True):
            _ComponentName = [i[0]]
            _component_list += [_ComponentName]
        self.db_cursor.execute(f"SELECT Code FROM ProductStock WHERE Name = '{ProductName}'")
        _ProductCode = self.db_cursor.fetchall()
        _ProductCode = _ProductCode[0][0]

        # pull component_code from table column name. pulled as a list of tuples
        self.db_cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='ComponentsPerProduct'")
        _product_make_info_tuple = self.db_cursor.fetchall()

        # self.db_cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='ComponentsPerProduct' AND INFORMATION_SCHEMA.COLUMNS.COLUMN_NAME = '_7785'")
        # _product_make_info_tuple = self.db_cursor.fetchall()

        self._component_dict = {}
        self._product_components_code_list = []

        # loop through list of tuples
        for i in _product_make_info_tuple:
            i = i[0]
            if i == 'Product Code':
                continue

            # pull component count for the product
            query = f"SELECT {i} FROM ComponentsPerProduct WHERE `Product Code` = {_ProductCode} AND {i} > 0"
            self.db_cursor.execute(query)
            _component_count = self.db_cursor.fetchall()
            if _component_count == []:
                continue
            _component_count = _component_count[0][0]

            # pull name of product's component
            query = f"SELECT Name FROM ComponentStock WHERE Code = {re.sub('_', '', i)}"
            self.db_cursor.execute(query)
            _component_name = self.db_cursor.fetchall()[0][0]
            self._component_dict.update({_component_name: _component_count})
        return self._component_dict
        # SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='StockDB' AND `TABLE_NAME`='ComponentsPerProduct';
        # SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`='ComponentsPerProduct';
        # SET @var=(SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`='ComponentsPerProduct');


    def FetchComponent(self, getcount=False, getstockstate=False, **kwargs):
        kwargs_dict = {"component_code": "Code", "component_name": "Name"}
        query = "SELECT "
        if (getcount is False) and (getstockstate is False):
            query += f"Name,Code "
        if (getcount is True) or (getstockstate is True):
            query += f"* "
        query += "FROM ComponentStock WHERE "

        _ = []
        for i in kwargs:
            arg = i
            _col_name = kwargs_dict[i]
            _col_val = kwargs[i]
            if arg == "component_name":
                _ += [f"{_col_name} = '{_col_val}'"]
            elif arg != "component_name":
                _ += [f"{_col_name} = {_col_val}"]
        query += str.join(" AND ", _)
        print(query)
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()

        if self.fetched_db_data_list == []:
            return 2

        if self.fetched_db_data_list != []:
            if getstockstate is True:
                if self.fetched_db_data_list[0][2] > 0:
                    return self.fetched_db_data_list, "in-stock"
                if self.fetched_db_data_list[0][2] == 0:
                    return self.fetched_db_data_list, "out-of-stock"
            elif getstockstate is False:
                return self.fetched_db_data_list

    def FetchAllComponents(self, **kwargs):
        columns = []
        '''
        getcount=False, getstockstate=False, getstockcount=False
        '''
        if len(kwargs) >= 1 or len(kwargs) < 3 and any(i is False for i in kwargs):
            for i in kwargs:
                if kwargs[i] is True:
                    columns += [f"{i}"]
            columns = str.join(",", columns)
        elif not any(i is False for i in kwargs) and len(kwargs) == 3:
            columns = "*"
        query = f"SELECT {columns} FROM ComponentStock"
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list



    ### db manip operations
    def AddColumn(self, table_name, column_name, **col_constraints):
        _check_col_query = f"IF NOT EXISTS((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME='{column_name}' AND TABLE_NAME='{table_name}')) THEN "
        _add_col_query = f"ALTER TABLE {table_name} ADD {column_name} {col_constraints}"
        _query = f"{_add_col_query} {_check_col_query}"
        self.db_cursor.execute(_query)
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list

    def RemoveColumn(self, table_name, column_name, condtion_data_dict):
        query = f"DELETE {column_name} FROM {table_name}"
        if condtion_data_dict is not {}:
            _condtion_data_dict = str.join(" AND ", [f"{i} = {condtion_data_dict[i]}" for i in condtion_data_dict])
            query += f"WHERE {_condtion_data_dict}"
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list

    def AddRow(self, table_name, row_data):
        '''

        :param table_name: table to insert values to
        :param row_data: dictionary. {"column name": "row_value to insert"}
        :return:
        '''
        _cols = str.join(',', [i for i in row_data])
        _values = str.join(',', [f"{(row_data[i])}" for i in row_data])
        query = f"INSERT INTO TABLE {table_name}({_cols}) VALUES {_values}"
        self.db_cursor.execute(query)
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list

    def RemoveRow(self, table_name, row_data):
        '''
        :param table_name: table to remove values from
        :param row_data: dictionary. {"column name": "row_value to insert"}
        :return:
        '''
        _cond_query = str.join(' AND ', [f'{i} = {row_data[i]}' for i in row_data])
        query = f"DELETE FROM {table_name} WHERE {_cond_query}"
        self.db_cursor.execute(query)
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list

    def UpdateValue(self, table_name, old_data, new_data):

        _new_data = str.join(",", [f"{i} = {new_data[i]}" for i in new_data])
        _old_data = str.join(" AND ", [f"{i} = {old_data[i]}" for i in old_data])

        query = f"UPDATE {table_name} SET {_new_data} WHERE {_old_data}"
        self.db_cursor.execute(query)
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list

    def AddComponent(self, component_name, component_code, component_count):
        self.AddRow(table_name="ComponentStock", row_data={"Name": component_name,
                                                           "Code": component_code,
                                                           "Count": component_count})

        self.AddRow(table_name="ComponentStockStateCount", row_data={"Component Code": component_code,
                                                                     "in-stock Count": component_count,
                                                                     "Rejected Count": 0,
                                                                     "Lost Count": 0,
                                                                     "Defective Count": 0})

    def AddProduct(self):
        pass

    def RemoveProduct(self):
        pass

    def RemoveComponent(self):
        pass

