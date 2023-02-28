import re
from baseclasses import RandomCharGenerator
import mariadb


class DBops:
    def __init__(self, db_cursor):
        self.db_cursor = db_cursor
        self.fetched_db_data_list = []

    ### Fetch operations=s
    # def FetchProduct(self, getcount=False, getstockstate=False, **kwargs):
    def FetchProduct(self, select_cols=None, **kwargs):
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

        query = ""
        if "Name" in kwargs:
            kwargs['Name'] = f"{kwargs['Name']}"

        _conditional_query = kwargs["conditional_query"]
        _conditional_query = [f"{i} = {_conditional_query[i]}" for i in _conditional_query]
        _conditional_query = str.join(" AND ", _conditional_query)

        if select_cols is not None:
            _select_cols = [i for i in select_cols]
            _select_cols = str.join(",", _select_cols)

            query = f"SELECT {_select_cols} FROM ProductStock WHERE {_conditional_query}"
        else:
            query = f"SELECT Name FROM ProductStock WHERE {_conditional_query}"

        print(query)
        self.db_cursor.execute(query)
        _ret = self.db_cursor.fetchall()[0]
        print(_ret)
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



    # def FetchComponent(self, select_cols, getcount=False, getstockstate=False, **kwargs):
    def FetchComponent(self, select_cols, conditional_query, getstockstate=False, **kwargs):
        '''
        :param getcount: fetch count column of specified component table
        :param getstockstate: show stock-state of specified component
        :param kwargs: specify, 'Code' and/or 'Name' to fetch
        :return:
        '''

        select_cols = str.join(",", [i for i in select_cols])
        query = f"SELECT {select_cols} FROM ComponentStock "

        _ = []
        if isinstance(conditional_query, dict):
            for i in conditional_query:
                _col_name = i
                _col_val = conditional_query[i]
                _ += [f"{_col_name} = {_col_val}"]
            query += " WHERE "
            if ("query_conditional_operator" in kwargs):
                query += str.join(f" {kwargs['query_conditional_operator']} ", _)
            elif ("query_conditional_operator" not in kwargs):
                query += str.join(" AND ", _)
            # query += f"{conditional_query}"
        elif isinstance(conditional_query, str):
            query += f"WHERE {conditional_query}"

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

    def FetchComponentAllStocks(self, Code):
        query = f"SELECT `in-stock Count`,`Rejected Count`,`Lost Count`,`Defective Count` FROM ComponentStockStateCount WHERE `Code` = {Code}"
        self.db_cursor.execute(query)
        stock_state_list = self.db_cursor.fetchall()[0]
        InStock = stock_state_list[0]
        Rejected = stock_state_list[1]
        Lost = stock_state_list[2]
        Defective = stock_state_list[3]
        return InStock, Rejected, Lost, Defective


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
            select_cols = str.join(", ", kwargs["select_cols"])

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
        _ = self.FetchProduct(select_cols=["Name", "Code"], **kwargs)
        _ProductName = _[0][0]
        _ProductCode = _[0][1]

        _query = f"SELECT `Component Code`,`Component Code Count` FROM ComponentsPerProduct WHERE `Product Code` = {_ProductCode} AND `Component Code Count` > 0"
        self.db_cursor.execute(_query)
        _component_code_count_list = self.db_cursor.fetchall()

        _conditional_query = []
        for i in _component_code_count_list:
            _component_code = i[0]
            _component_count = i[1]
            _conditional_query += [f"Code = {_component_code}"]
        _conditional_query = str.join(" OR ", _conditional_query)
        for i in self.FetchComponent(select_cols=["Name", "Count"], conditional_query=_conditional_query):
            _component_name = i[0]
            _component_count = i[1]
            _components_per_product_dict.update({_component_name: _component_count})
        print(_components_per_product_dict)

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
        query = f"INSERT INTO TABLE {table_name}({_cols}) VALUES {_values}"
        print(query)
        # self.db_cursor.execute(query)
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
        # self.db_cursor.execute(query)
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list


    def UpdateValue(self, table_name, col_to_update, new_value, conditional_query, **kwargs):
        '''
        :param table_name: Table name to update value in
        :param current_data: current value ->
        :param new_data: value to replace current value
        :return:
        '''

        query = ""
        if isinstance(col_to_update, dict):
            col_to_update = [f"{i} = {col_to_update[i]}" for i in col_to_update]
        if conditional_query is not None:
            if isinstance(conditional_query, dict):
                conditional_query = [f"{i} = {conditional_query[i]}" for i in conditional_query]
                if "conditional_query_operator" in kwargs:
                    conditional_query = str.join(f" {kwargs['conditional_query_operator']} ", conditional_query)
                elif not "conditional_query_operator" in kwargs:
                    conditional_query = str.join(f" AND ", conditional_query)
            query = f"UPDATE {table_name} SET {col_to_update} = {new_value} WHERE {conditional_query}"
        elif conditional_query is None:
            query = f"UPDATE {table_name} SET {col_to_update} = {new_value}"

        print(query)
        self.db_cursor.execute(query)
        self.db_cursor.execute("COMMIT")
        print("funck it changed")
        # self.fetched_db_data_list = self.db_cursor.fetchall()
        # return self.fetched_db_data_list




    def AddComponent(self, component_name, component_code, component_count):
        self.AddRow(table_name="ComponentStock", row_data={"Name": component_name,
                                                           "Code": component_code,
                                                           "Count": component_count})

        self.AddRow(table_name="ComponentStockStateCount", row_data={"Code": component_code,
                                                                     "in-stock Count": component_count,
                                                                     "Rejected Count": 0,
                                                                     "Lost Count": 0,
                                                                     "Defective Count": 0})

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
            _component_count = component_list_dict[i]["count"]
            _component_code = "'" + RandomCharGenerator(char_len=6) + "'"
            self.AddComponent(_component_name, _component_code, _component_count)

        _product_code = "'" + RandomCharGenerator(char_len=6) + "'"

        self.AddRow(table_name="ProductStock",
                    row_data={"Name": product_name,
                              "Code": _product_code,
                              "Count": product_count})

        for i in component_list_dict:
            _component_name = i
            _component_count = component_list_dict[_component_name]
            _component_code = "'" + RandomCharGenerator(char_len=6) + "'"
            self.AddRow(table_name="ComponentsPerProduct",
                        row_data={
                            "`Product Code`": _product_code,
                            "`Component Code`": _component_count,
                            "`Component Code Count`": _component_count})

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

    def ChangeProductStockState(self, to_stock_num, conditional_query):
        current_stock_num = self.FetchProduct(select_cols=["Count", "Name"], conditional_query=conditional_query)
        print("rock on")
        conditional_query_dict = {"Count": current_stock_num[0], "Name": f'{current_stock_num[1]}'}
        conditional_query_dict = {"Count": current_stock_num[0], "Name": conditional_query["Name"]}
        print("FUCK YEA RYT")
        self.UpdateValue(table_name="ProductStock", col_to_update="Count", new_value=to_stock_num, conditional_query=conditional_query_dict)

    def ChangeComponentStockState(self, stock_type, to_stock_num, **kwargs):
        conditional_query = kwargs["conditional_query"]
        if ("Name" in conditional_query and "Code" not in conditional_query) or ("Name" in conditional_query and "Code" in conditional_query):
            ComponentCode = self.FetchComponent(select_cols=["Code"], conditional_query=conditional_query)[0][0]
            self.UpdateValue(table_name="ComponentStockStateCount", ComponentCode=ComponentCode, col_to_update=stock_type, new_value=to_stock_num, conditional_query={"`Code`": ComponentCode})
        if "Name" not in conditional_query and "Code" in conditional_query:
            self.UpdateValue(table_name="ComponentStockStateCount", ComponentCode=conditional_query["Code"], col_to_update=stock_type, new_value=to_stock_num, conditional_query={"`Code`": conditional_query["Code"]})
        print("funck")

