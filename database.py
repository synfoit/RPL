import psycopg2

class Database:

    def __init__(self):
        self.db_handle = psycopg2.connect(
            database="RPL_DRYER",
            user='postgres',
            password='Servilink@123',
            host='localhost',
            port='5432'
        )

        self.mycursor = self.db_handle.cursor()



    def get_single_data(self, table, query_columns_dict):
        selection_list = " AND ".join([
            f"{column_name} {query_columns_dict[column_name][0]} %s"
            for column_name in sorted(query_columns_dict.keys())
        ])

        sql = f"SELECT * FROM {table} WHERE {selection_list}"

        val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))

        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchone()

        return result



    def get_multiple_data(self, table, query_columns_dict):
        if query_columns_dict == None:
            sql = f"SELECT * FROM {table}"
            self.mycursor.execute(sql)
        else:
            selection_list = " AND ".join([
                f"{column_name} {query_columns_dict[column_name][0]} %s"
                for column_name in sorted(query_columns_dict.keys())
            ])
            sql = f"SELECT * FROM {table} WHERE {selection_list}"

            val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))
            self.mycursor.execute(sql, val)

        result = self.mycursor.fetchall()

        return result

    def get_count_data(self, table, dashboard_id,start_date,process_name):
        start_Time=start_date+' 00:00:00'
        end_Time=start_date+' 24:00:00'
        sql = f"SELECT * FROM {table} WHERE dashboard_id={dashboard_id} and process_name='{process_name}' and start_time BETWEEN '{start_Time}' and '{end_Time}'"

        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()

        return result

    def get_batchname_heatingname(self, table,batch_name,DashboardId,processName):

        sql = f"SELECT * FROM {table} WHERE dashboard_id={DashboardId} and process_name='{processName}' and batch_name='{batch_name}'"

        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()

        return result
    def get_endtime_batchname(self, table,batchname,process_name):
        sql=f"SELECT end_time FROM {table} WHERE batch_name={batchname} and process_name={process_name}"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()

        return result
    def insert_single_data(self, table, query_columns_dict):
        column_names = ",".join([f"{column_name}" for column_name in sorted(query_columns_dict.keys())])
        column_holders = ",".join([f"%s" for column_name in sorted(query_columns_dict.keys())])
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_holders})"

        val = tuple(query_columns_dict[column_name] for column_name in sorted(query_columns_dict.keys()))

        self.mycursor.execute(sql, val)
        self.db_handle.commit()

        return self.mycursor.rowcount
    def get_batch_count(self,table, dashboard_id,batch_name,process_name):
        sql = f"SELECT * FROM {table} WHERE dashboard_id={dashboard_id} and process_name='{process_name}' and batch_name LIKE '{batch_name}%'"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()

        return result

    def insert_multiple_data(self, table, columns, multiple_data):
        column_names = ",".join(columns)
        column_holders = ",".join([f"%s" for column_name in columns])
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_holders})"

        self.mycursor.executemany(sql, multiple_data)
        self.db_handle.commit()

        return self.mycursor.rowcount


    def update_data(self,table,BatchName, dashboard_id,batchEndTime,processName):
        sql=f"UPDATE {table} SET end_time ='{batchEndTime}' Where batch_name='{BatchName}' and process_name ='{processName}' and dashboard_id={dashboard_id}"

        self.mycursor.execute(sql)
        self.db_handle.commit()

    def get_last_heatingprocess_batchname(self,table,dashboardId, ProcessName):
        sql = f"SELECT batch_name from {table} where dashboard_id={dashboardId} and process_name='{ProcessName}' ORDER BY id desc"
        print("sql",sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result
    def get_last_heatingprocess(self,table,dashboardId, ProcessName):
        sql = f"SELECT * from {table} where dashboard_id={dashboardId} and process_name='{ProcessName}' ORDER BY id desc"

        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result

    def get_batch_name_cooling(self,table,dashboardId,BatchName, ProcessName):
        sql = f"SELECT batch_name from {table} where dashboard_id={dashboardId} and process_name='{ProcessName}' and batch_name='{BatchName}'"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result
