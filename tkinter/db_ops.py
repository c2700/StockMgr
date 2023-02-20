import re

import mariadb


class DBops:
    def __init__(self, db_cursor):
        self.db_cursor = db_cursor
        self.fetched_db_data_list = []

    ### Fetch operations=s
    def FetchProduct(self, product_name, getcount=False, getstockstate=False):
        '''
        :param product_name: name of product to fetch
        :param getcount: get count column
        :param getstockstate: get stock state
        :return:
        '''
        query = f"SELECT Name FROM ProductStock WHERE Name = {product_name}"
        if (getcount is True) and (getstockstate is False):
            query = f"SELECT Name,Count FROM ProductStock WHERE Name = {product_name}"
        if (getcount is True) and (getstockstate is True):
            query = f"SELECT * FROM ProductStock WHERE Name = {product_name}"
        # print(query)
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()


    def FetchAllProducts(self, getcount=False, getstockstate=False):
        '''
        :param getcount: get count column
        :param getstockstate: get stock state
        :return:
        '''
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
        '''
        fetch info of all required components required for said product from DB
        :param ProductName: name of product to fetch
        :return:
        '''
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
        '''
        :param getcount: fetch count column of specified component table
        :param getstockstate: show stock-state of specified component
        :param kwargs: specify, 'component code' and/or 'component name' to fetch
        :return:
        '''
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
        '''
        Fetch all Names of all components from ComponentStock Table
        :param kwargs:{
            Bool "Code": Fetch Component Code
            Bool "Count": Fetch Component Count
        }
        :return:
        '''

        columns = ["Name"] + [i for i in kwargs if kwargs[i] is not True]
        columns = str.join(",", columns)
        query = f"SELECT {columns} FROM ComponentStock"
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list



    ### db manip operations
    def AddColumn(self, table_name, column_name, col_data_props, foreign_key_constraints, foreign_key=False, index=False):
        '''

        :param table_name: table name to add the column to
        :param column_name: column name to be added
        :param foreign_key_constraints: {
                                        "reference_table": string,
                                        "reference_column": string
                                        }

        :param col_data_props: column data entry properties/constraints
                                {
                                no_null: bool,
                                data_type: string,
                                }

        :param index_constraints: => set index constraints
                {
                index_name: string (column_name_idx),
                index_mode: ASC
                index_reference_col: foreign_key_constraints["reference_table"]
                }

        :return:
        '''

        # _check_col_query = f"IF NOT EXISTS((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME='{column_name}' AND TABLE_NAME='{table_name}')) THEN "
        # _add_col_query = f"ALTER TABLE {table_name} ADD {column_name} {col_constraints}"
        # _query = f"{_check_col_query} {_add_col_query}"
        _check_add_col_query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS `{column_name}`"

        col_data_props["data_type"] = str.upper(col_data_props["data_type"])
        if col_data_props["no_null"] is True:
            _check_add_col_query = f"{_check_add_col_query} NOT NULL"

        _query = ""
        if foreign_key == False:
            _query = f"{_check_add_col_query}"
        elif foreign_key == True:
            _reference_table = foreign_key_constraints["reference_table"]
            _reference_column = foreign_key_constraints["reference_column"]
            _foreign_key_query = f"CONSTRAINT `{column_name}` FOREIGN KEY (`{column_name}`) REFERENCES {_reference_table}(`{_reference_column}`) ON DELETE CASCADE ON UPDATE CASCADE"
            # CONSTRAINT `Component Code` FOREIGN KEY (`Component Code`) REFERENCES ComponentStock(`Code`) ON DELETE CASCADE ON UPDATE CASCADE
            _query = f"{_check_add_col_query} {_foreign_key_query}"

            if index == True:
                _index_name = f"{_reference_column}"
                _index_mode = "ASC"
                _index_reference = f"{_reference_table}"
                _index_query = f"INDEX ({_index_reference} {_index_mode}) VISIBLE"
                # INDEX `Product Code_idx` (`Product Code` ASC) VISIBLE
                _query += f", {_index_query}"

        print(_query)
        # self.db_cursor.execute(_query)
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list

    def RemoveColumn(self, table_name, column_name, condtion_data_dict):
        '''
        :param table_name: table name to remove column from
        :param column_name: column to remove
        :param condtion_data_dict: constraints/conditions/values to check for
        :return:
        '''
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


    def UpdateValue(self, table_name, curent_data, new_data):
        '''
        :param table_name: Table name to update value in
        :param curent_data: current value
        :param new_data: value to replace current value
        :return:
        '''

        _new_data = str.join(",", [f"{i} = {new_data[i]}" for i in new_data])
        _old_data = str.join(" AND ", [f"{i} = {curent_data[i]}" for i in curent_data])

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

    def RemoveComponent(self, **kwargs):
        _kwargs = {
            "component_name": "Code",
            "component_code": "Name"
        }

        _row_data = {}

        for i in kwargs:
            _row_data.update({i: _kwargs[i]})

        self.RemoveRow(table_name="ComponentStock", row_data=_row_data)
        self.RemoveRow(table_name="ComponentStockStateCount", row_data=_row_data)


    def AddProduct(self):
        pass

    def RemoveProduct(self):
        pass

