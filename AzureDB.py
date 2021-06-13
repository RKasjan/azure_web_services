import pypyodbc
import azurecred


class AzureDB:
    dsn = 'DRIVER=' + azurecred.AZDBDRIVER + ';Server=tcp:' + azurecred.AZDBSERVER + ',1433;Database=' + azurecred.AZDBNAME + ';UID=' + azurecred.AZDBUSER + ';PWD=' + azurecred.AZDBPW + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT id,name,text,date from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit(1)

    def azureAddData(self, name, text, date):
        sql = '''INSERT INTO data (name, text, date) VALUES (?, ?, ?)'''
        val = (name, text, date)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def azureDeleteData(self, id):
        self.cursor.execute("DELETE FROM data WHERE id = %s" % (id))
        self.conn.commit()
