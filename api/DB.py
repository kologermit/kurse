import psycopg2, time, logging
from datetime import datetime
from psycopg2.sql import SQL, Identifier

logging.basicConfig(filename="log.txt")


def now_str():
    return datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")


class DB:
    def __init__(self, postgres, max_time_lost_connection=60):
        self.postgres = postgres
        self.max_time_lost_connection = max_time_lost_connection
        try:
            self.psql = psycopg2.connect(**self.postgres)
        except Exception as err:
            logging.error(f"{now_str()}:BDConnectError: {err}")
            time_lost_connection = 1
            flag_lost_connection = False
            while flag_lost_connection == False:
                try:
                    self.psql = psycopg2.connect(**self.postgres)
                    flag_lost_connection = True
                except Exception as err2:
                    time.sleep(time_lost_connection)
                    if time_lost_connection < self.max_time_lost_connection:
                        print(f"Wait {time_lost_connection} seconds...")
                        time_lost_connection += 3

    def query(self, Query, data=[], isResult=False):
        cursor = self.psql.cursor()
        cursor.execute(Query, data)
        self.psql.commit()
        result = None
        if isResult:
            result = cursor.fetchall()
        cursor.close()
        return result

    def select(self, table, columns=[], where=[], limit="", is_print_sql_query=False):
        """table = "table"
columns = ["col1", "col2", "col3"]
columns = None -> "*"
where = [{"column": "column", "cond_sign": ">", "data": 1},
{"column": "column2", "cond_sign": "<", "data": 100}]
limit = int
is_print_sql_query=False/True"""

        # columns and table
        sql_query = "SELECT "
        formatter = []
        if not columns:
            sql_query += "* FROM {} "
            formatter.append(Identifier(table))
        else:
            sql_query += "{} "
            formatter.append(Identifier(columns[0]))
            for i in columns[1:]:
                sql_query += ", {} "
                formatter.append(Identifier(i))
            sql_query += "FROM {} "
            formatter.append(Identifier(table))
        data = []

        # where
        if where:
            sql_query += "WHERE "
            for i in where:
                if i.get("column") and i.get("cond_sign"):
                    sql_query += f"{{}} {i['cond_sign']} %s AND "
                    formatter.append(Identifier(i['column']))
                    data.append(i["data"])
            if sql_query[-4:] == "AND ":
                sql_query = sql_query[:-4] + " "

        # limit
        if limit:
            sql_query += "LIMIT %s"
            data.append(limit)

        sql_query = SQL(sql_query).format(*formatter)

        # print sql query
        if is_print_sql_query:
            logging.info(sql_query)
            logging.info(data)

        result = self.query(sql_query, data, isResult=True)
        return result

    def insert(self, table, columns, values, lastval=False, is_print_sql_query=False):
        """table = "table"
columns = ["col1", "col2", "col3"]
values=[val1, val2, val3]
limit = int
is_print_sql_query=False/True"""

        # table and columns
        formatter = []
        sql_query = "INSERT INTO {} ({}"
        formatter.append(Identifier(table))
        formatter.append(Identifier(columns[0]))
        for i in columns[1:]:
            sql_query += ", {}"
            formatter.append(Identifier(i))

        # values
        sql_query += ") VALUES (%s"
        data = []
        data.append(values[0][0])
        for i in values[0][1:]:
            sql_query += ", %s"
            data.append(i)
        sql_query += ") "
        for i in values[1:]:
            sql_query += ", (%s"
            data.append(i[0])
            for j in i[1:]:
                sql_query += ", %s"
                data.append(j)
            sql_query += ") "
        sql_query += ";"

        if lastval:
            sql_query += "\nSELECT lastval();"

        sql_query = SQL(sql_query).format(*formatter)

        # print sql query
        if is_print_sql_query:
            logging.info(sql_query)
            logging.info(data)

        return self.query(sql_query, data, isResult=lastval)

    def update(self, table, where, values, is_print_sql_query=False, return_count=False):
        """table = "table"
where = [{"column": "column", "cond_sign": ">", "data": 1},
{"column": "column2", "cond_sign": "<", "data": 100}]
values={"column1": val1, "column2": val2}
return_count=False/True
is_print_sql_query=False/True"""

        # table
        formatter = []
        sql_query = "UPDATE {} \nSET "
        formatter.append(Identifier(table))

        # values
        data = []
        for i in values:
            sql_query += "{} = %s,\n"
            formatter.append(Identifier(i))
            data.append(values[i])

        # where
        sql_query += "WHERE "
        sql_query = sql_query.replace(",\nWHERE", "\nWHERE")
        for i in where:
            if i.get("column") and i.get("cond_sign"):
                sql_query += f"{{}} {i['cond_sign']} %s AND "
                formatter.append(Identifier(i['column']))
                data.append(i["data"])
        if sql_query[-4:] == "AND ":
            sql_query = sql_query[:-4]

        if return_count:
            sql_query = f"WITH updated AS ({sql_query} IS TRUE RETURNING *) SELECT count(*) FROM updated;"

        logging.info(sql_query)
        sql_query = SQL(sql_query).format(*formatter)

        # print sql query
        if is_print_sql_query:
            logging.info(sql_query)
            logging.info(data)

        return self.query(sql_query, data, isResult=return_count)

    def delete(self, table, where, return_count=False, is_print_sql_query=False):
        """table = "table"
where = [{"column": "column", "cond_sign": ">", "data": 1},
{"column": "column2", "cond_sign": "<", "data": 100}]
return_count=False/True
is_print_sql_query=False/True"""
        # table
        formatter = []
        sql_query = "DELETE FROM {} \n "
        formatter.append(Identifier(table))

        # where
        sql_query += "WHERE "
        data = []
        for i in where:
            if i.get("column") and i.get("cond_sign"):
                sql_query += f"{{}} {i['cond_sign']} %s AND "
                formatter.append(Identifier(i['column']))
                data.append(i["data"])
        if sql_query[-4:] == "AND ":
            sql_query = sql_query[:-4]

        if return_count:
            sql_query = f"WITH deleted AS ({sql_query} IS TRUE RETURNING *) SELECT count(*) FROM deleted;"

        sql_query = SQL(sql_query).format(*formatter)

        # print sql query
        if is_print_sql_query:
            logging.info(sql_query)
            logging.info(data)

        return self.query(sql_query, data, isResult=return_count)

    def __del__(self):
        self.psql.close()
