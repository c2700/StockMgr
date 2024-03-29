from baseclasses import RandomCharGenerator
import re


class DBops:
    def __init__(self, db_cursor):
        self.db_cursor = db_cursor
        self.fetched_db_data_list = []

    ### Fetch operations
    def FetchProduct(self, select_cols=None, getstockstate=False, getcount=False, **kwargs):
    # def FetchProduct(self, select_cols=None, **kwargs):
        '''
        # :param product_name: name of product to fetch
        :param select_cols: list(columns_to_select)
        :param kwargs: {
                        Name="val",
                        Code="val",
                        Count="val",
                    }
        :param getcount: get count column
        :param getstockstate: get stock state
        :return:
        '''

        _query = ""
        if "Name" in kwargs:
            kwargs['Name'] = f"'{kwargs['Name']}'"

        _conditional_query = kwargs["conditional_query"]
        if isinstance(_conditional_query, dict):
            _conditional_query = [f"{i} = {_conditional_query[i]}" for i in _conditional_query]
            _conditional_query = str.join(" AND ", _conditional_query)

        if select_cols is not None:
            select_cols = [i for i in select_cols]
            select_cols = str.join(",", select_cols)
        elif select_cols is None:
            select_cols = "Name"

        _query = f"SELECT {select_cols} FROM ProductStock WHERE {_conditional_query}"

        print(_query)
        self.db_cursor.execute(_query)
        _ret = self.db_cursor.fetchall()
        # return self.db_cursor.fetchall()
        return _ret



    def FetchAllProducts(self, getcount=False, getstockstate=False):
        '''
        :param getcount: get count column
        :param getstockstate: get stock state
        :return:
        '''
        query = "SELECT "
        if (getcount is False) and (getstockstate is False):
            query += "Name"
        if ((getcount is True) and (getstockstate is False)) or ((getcount is False) and (getstockstate is True)):
            query += "Name,Count"
        if (getcount is True) and (getstockstate is True):
            query += "*"
        query += " FROM ProductStock"
        print(query)
        self.db_cursor.execute(query)
        fetched_db_data_list = []
        if getstockstate is True:
            for i in self.db_cursor.fetchall():
                if i[1] > 0:
                    fetched_db_data_list += [(i, "in-stock")]
                elif i[1] == 0:
                    fetched_db_data_list += [(i, "out-of-stock")]
            return fetched_db_data_list
        elif getstockstate is False:
            return self.db_cursor.fetchall()



    def FetchComponent(self, select_cols, conditional_query, getstockstate=False, **kwargs):
        '''
        :param getcount: fetch count column of specified component table
        :param getstockstate: show stock-state of specified component
        :param kwargs: specify, 'Code' and/or 'Name' to fetch
        :return:
        '''

        if getstockstate is True:
            if "Count" not in select_cols:
                select_cols += ["Count"]
        select_cols = str.join(",", [i for i in select_cols])
        query = f"SELECT {select_cols} FROM {kwargs['table_name']} " if "table_name" in kwargs else f"SELECT {select_cols} FROM ComponentStock "
        # query = f"SELECT {select_cols} FROM ComponentStock "

        _ = []
        if isinstance(conditional_query, dict):
            for i in conditional_query:
                _col_name = i
                _col_val = conditional_query[i]
                _ += [f"{_col_name} = {_col_val}"]
            query += "WHERE "
            if ("query_conditional_operator" in kwargs):
                query += str.join(f" {kwargs['query_conditional_operator']} ", _)
            elif ("query_conditional_operator" not in kwargs):
                query += str.join(" AND ", _)
            # query += f"{conditional_query}"
        elif isinstance(conditional_query, str):
            query += f"WHERE {conditional_query}"

        print(query)
        # print(dir(self.db_cursor))
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()

        if self.fetched_db_data_list == []:
            return None

        if self.fetched_db_data_list != []:
            if getstockstate is True:
                if self.fetched_db_data_list[0][2] > 0:
                    return self.fetched_db_data_list, "in-stock"
                if self.fetched_db_data_list[0][2] == 0:
                    return self.fetched_db_data_list, "out-of-stock"
            elif getstockstate is False:
                return self.fetched_db_data_list

    def FetchComponentAllStocks(self, Code):
        _query = f"SELECT `in-stock Count`,`Rejected Count`,`Lost Count`,`Defective Count` FROM ComponentStockStateCount WHERE `Code` = {Code}"
        self.db_cursor.execute(_query)
        _stock_state_list = self.db_cursor.fetchall()[0]
        _inStock = _stock_state_list[0]
        _rejected = _stock_state_list[1]
        _lost = _stock_state_list[2]
        _defective = _stock_state_list[3]
        return _inStock, _rejected, _lost, _defective


    def FetchAllComponents(self, **kwargs):
        '''
        Fetch all Names of all components from ComponentStock Table
        :param kwargs:{
            Bool "Code": Fetch Component Code
            Bool "Count": Fetch Component Count
        }
        :return:
        '''

        query = ""
        select_cols = "Name"
        if "select_cols" in kwargs:
            select_cols = [select_cols] + kwargs["select_cols"]
            select_cols = str.join(", ", select_cols)

        if "conditional_query" in kwargs:
            conditional_query = kwargs["conditional_query"]
            if (isinstance(conditional_query, dict)):
                _conditional_query = []
                for i in conditional_query:
                    _conditional_query += [f"{i} = {conditional_query[i]}"]

                if "query_conditional_operator" in kwargs:
                    _conditional_query = str.join(kwargs["query_conditional_operator"], _conditional_query)
                elif "query_conditional_operator" not in kwargs:
                    _conditional_query = str.join(" AND ", _conditional_query)

        if "conditional_query" not in kwargs:
            query = f"SELECT {select_cols} FROM ComponentStock"

        print(query)
        self.db_cursor.execute(query)
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list


    def FetchComponentsPerProduct(self, **kwargs):
        _components_per_product_dict = {}
        # _ = self.FetchProduct(select_cols=["Name", "Code"], **kwargs)
        # _ = self.FetchProduct(select_cols=["Name", "Code"], conditional_query=kwargs["conditional_query"]) if "conditional_query" in kwargs else self.FetchProduct(select_cols=["Name", "Code"], **kwargs)
        _conditional_query = kwargs["conditional_query"]
        # del _conditional_query["Count"]
        _ = self.FetchProduct(select_cols=["Name", "Code"], conditional_query=_conditional_query)
        '''
        _ = None
        if "conditional_query" in kwargs:
            _ = self.FetchProduct(select_cols=["Name", "Code"], conditional_query=kwargs["conditional_query"])
        elif "conditional_query" not in kwargs:
            _ = self.FetchProduct(select_cols=["Name", "Code"], **kwargs)
        '''
        _ProductName = _[0][0]
        _ProductCode = _[0][1]

        _query = f"SELECT `Component Code`,`CodeCount` FROM ComponentsPerProduct WHERE `Product Code` = {_ProductCode} AND `CodeCount` > 0"
        self.db_cursor.execute(_query)
        _component_code_count_list = self.db_cursor.fetchall()

        for i in _component_code_count_list:
            _component_code = i[0]
            _component_code_count = i[1]
            _components_per_product_dict.update({_component_code: _component_code_count})

        '''
        _conditional_query = []
        for i in _component_code_count_list:
            _component_code = i[0]
            _component_count = i[1]
            _conditional_query += [f"Code = {_component_code}"]
        _conditional_query = str.join(" OR ", _conditional_query)
        for i in self.FetchComponent(select_cols=["Name", "Count"], conditional_query=_conditional_query):
        # for i in self.FetchComponentsPerProduct(conditional_query=_conditional_query):
            _component_name = i[0]
            _component_count = i[1]
            _components_per_product_dict.update({_component_name: _component_count})
        '''
        print(_components_per_product_dict)
        return _components_per_product_dict

        # SET @var=(SELECT `Product Code` FROM ComponentsPerProduct WHERE `Product Code` = 653);
        # self.db_cursor.execute("SELECT Name FROM ")
        # SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='StockDB' AND `TABLE_NAME`='ComponentsPerProduct';
        # SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`='ComponentsPerProduct';
        # SET @var=(SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`='ComponentsPerProduct');



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
        self.db_cursor.execute(_query)
        self.db_cursor.execute("COMMIT")
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
        self.db_cursor.execute("COMMIT")
        self.fetched_db_data_list = self.db_cursor.fetchall()
        return self.fetched_db_data_list

    def AddRow(self, table_name, row_data):
        '''
        :param table_name: table to insert values to
        :param row_data: dictionary. {"column name": "row_value to insert"}
        :return:
        '''

        _cols = []
        _values = []

        for i in row_data:
            _cols += [i]
            if isinstance(row_data[i], dict) and ("count" in row_data[i]):
                _values += [str(row_data[i]["count"])]
            else:
                _values += [str(row_data[i])]

        # _cols = str.join(',', [i for i in row_data])
        # _values = "(" + str.join(',', [f"{(row_data[i])}" for i in row_data]) + ")"
        _cols = str.join(',', _cols)
        _values = "(" + str.join(',', _values) + ")"
        query = f"INSERT INTO {table_name}({_cols}) VALUES {_values}"
        print(query)
        self.db_cursor.execute(query)
        self.db_cursor.execute("COMMIT")
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
        print(query)
        self.db_cursor.execute(query)
        self.db_cursor.execute("COMMIT")
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list


    def UpdateValue(self, table_name, update_fields, conditional_query, **kwargs):
        '''
        :param table_name: Table name to update value in
        :param current_data: current value ->
        :param new_data: value to replace current value
        :return:
        '''

        query = ""
        if isinstance(update_fields, dict):
            update_fields = [f"{i} = {update_fields[i]}" for i in update_fields]
            update_fields = str.join(",", update_fields)
        if conditional_query is not None:
            if isinstance(conditional_query, dict):
                conditional_query = [f"{i} = {conditional_query[i]}" for i in conditional_query]
                if "conditional_query_operator" in kwargs:
                    conditional_query = str.join(f" {kwargs['conditional_query_operator']} ", conditional_query)
                elif not "conditional_query_operator" in kwargs:
                    conditional_query = str.join(f" AND ", conditional_query)
            query = f"UPDATE {table_name} SET {update_fields} WHERE {conditional_query}"
        elif conditional_query is None:
            query = f"UPDATE {table_name} SET {update_fields}"

        print(query)
        self.db_cursor.execute(query)
        self.db_cursor.execute("COMMIT")
        print("funck it changed")
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list




    # def AddComponent(self, component_name, component_code, component_count):
    def AddComponent(self, _added_component_name, component_count, return_code=False):
        self._added_component_code = RandomCharGenerator(char_len=6)
        self.AddRow(table_name="ComponentStock", row_data={"Name": _added_component_name,
                                                           "Code": self._added_component_code,
                                                           # "Code": component_code,
                                                           "Count": component_count})

        self.AddRow(table_name="ComponentStockStateCount", row_data={"Code": self._added_component_code,
                                                                     # "Code": component_code,
                                                                     "`in-stock Count`": component_count,
                                                                     "`Rejected Count`": 0,
                                                                     "`Lost Count`": 0,
                                                                     "`Defective Count`": 0})
    @property
    def get_added_component_code(self):
        return self._added_component_code


    def RemoveComponent(self, **kwargs):
        _kwargs = {
            "component_name": "Name",
            "component_code": "Code",
            "component_count": "Count"
        }

        _row_data = {}

        for i in kwargs:
            _row_data.update({_kwargs[i]: kwargs[i]})
        print(_row_data)

        self.RemoveRow(table_name="ComponentStock", row_data=_row_data)
        self.RemoveRow(table_name="ComponentStockStateCount", row_data=_row_data)


    def AddProduct(self, product_name, product_count, component_list_dict):
        '''
        # {"code": {"name": "", "count": ""}}
        for i in component_list_dict:
            _component_code = i
            _component_name = component_list_dict[_component_code]["name"]
            _component_count = component_list_dict[_component_code]["count"]
            self.AddComponent(_component_name, _component_code, _component_count)
        '''

        # "name": {"count": ""}
        for i in component_list_dict:
            _component_name = i
            _component_count = component_list_dict[_component_name]["count"]
            _component_code = component_list_dict[_component_name]["code"]
            # self.AddComponent(_component_name, _component_code, _component_count)
            # self.AddComponent(_component_name, _component_count)

        self._added_product_code = RandomCharGenerator(char_len=6)

        self.AddRow(table_name="ProductStock",
                    row_data={"Name": product_name,
                              "Code": self._added_product_code,
                              "Count": product_count})

        for i in component_list_dict:
            _component_name = i
            _component_count = component_list_dict[_component_name]["count"]
            _component_code = component_list_dict[_component_name]["code"]
            self.AddRow(table_name="ComponentsPerProduct",
                        row_data={
                            "`Product Code`": self._added_product_code,
                            "`Component Code`": _component_code,
                            "`CodeCount`": _component_count})
    @property
    def get_added_product_code(self):
        return self._added_product_code

    def RemoveProduct(self, **kwargs):
        '''
        :param kwargs: {
                            Code: "", # product code
                            Name: "", # product name
                        }
        :return:
        '''

        # self.RemoveComponent(component_name="", component_code="", component_count="")
        _row_data = {}
        if "Code" in kwargs:
            _row_data.update({"`Product Code`": kwargs["Code"]})
        if "Name" in kwargs:
            _row_data.update({"`Product Name`": kwargs["Name"]})

        self.RemoveRow("ProductStock", row_data=_row_data)
        self.RemoveRow("ComponentsPerProduct", row_data={"`Product Code`": kwargs["Code"]})

    def ChangeProductStockState(self, from_stock_state, to_stock_state, to_stock_num, conditional_query):
        current_stock_num = self.FetchProduct(select_cols=["Count", "Name"], conditional_query=conditional_query)
        print("rock on")
        # conditional_query_dict = {"Count": current_stock_num[0], "Name": f'{current_stock_num[1]}'}
        conditional_query_dict = {"Count": current_stock_num[0], "Name": conditional_query["Name"]}

        _from_stock_num = to_stock_num - current_stock_num[0]
        self.UpdateValue(table_name="ProductStock", update_fields={from_stock_state: _from_stock_num}, conditional_query=conditional_query_dict)
        print("FUCK YEA RYT")

    def ChangeComponentStockState(self, from_stock_state, to_stock_state, change_quantity, **kwargs):
        conditional_query = kwargs["conditional_query"]

        _table_name = ""
        _ComponentCode = None
        _ComponentCodeStockStateTuple = None

        if "table_name" not in conditional_query:
            _table_name = "ComponentStockStateCount"
        elif "table_name" in conditional_query:
            _table_name = conditional_query["table_name"]

        if ("Name" in conditional_query and "Code" not in conditional_query) or ("Name" in conditional_query and "Code" in conditional_query):
            _ComponentCode = self.FetchComponent(select_cols=["Code"], conditional_query=conditional_query)[0][0]

        if "Name" not in conditional_query and "Code" in conditional_query:
            _ComponentCode = conditional_query["Code"]

        _ComponentCodeStockStateTuple = self.FetchComponentAllStocks(Code=_ComponentCode)

        _temp_dict = {
            "in-stock": "`in-stock Count`",
            "rejected": "`Rejected Count`",
            "lost": "`Lost Count`",
            "defective": "`Defective Count`",
        }

        from_stock_state = _temp_dict[from_stock_state]
        to_stock_state = _temp_dict[to_stock_state]

        _temp_dict_0 = {
            "`in-stock Count`": _ComponentCodeStockStateTuple[0],
            "`Rejected Count`": _ComponentCodeStockStateTuple[1],
            "`Lost Count`": _ComponentCodeStockStateTuple[2],
            "`Defective Count`": _ComponentCodeStockStateTuple[3],
        }

        from_stock_state_quantity = _temp_dict_0[from_stock_state]
        to_stock_state_quantity = _temp_dict_0[to_stock_state]

        _changed_from_stock_state_quantity = from_stock_state_quantity - change_quantity
        _changed_to_stock_state_quantity = to_stock_state_quantity + change_quantity

        self.UpdateValue(table_name=_table_name,
                         ComponentCode=_ComponentCode,
                         update_fields={from_stock_state: _changed_from_stock_state_quantity, to_stock_state: _changed_to_stock_state_quantity},
                         conditional_query={"`Code`": _ComponentCode})
        print("funck")

