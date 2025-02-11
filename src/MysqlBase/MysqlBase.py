import mysql.connector

class MysqlService: 
     Instance = None

     @classmethod
     def __init__(self):
          try:
               if self.Instance is None:
                    self.Instance = mysql.connector.connect(
                         host="localhost",
                         user="root",
                         password="yourpassword",
                         database="yourdatabase"
                    )
                    self.cursor = self.Instance.cursor(dictionary=True)
          except Exception as err:
               raise Exception(f'Failed to initial mysql service: {err}')
          
     @classmethod
     def exec(cls, sp: str, data: any = None): 
          cls.checkMysqlInitial()

          query = f"CALL {sp}({', '.join(['%s'] * len(data))})" if data else f"CALL {sp}()"
          cls.cursor.execute(query, data or ())
          return cls.cursor.fetchall()
     
     


     @classmethod
     def checkMysqlInitial(cls):
          if cls.Instance is None:
               raise Exception(f'Mysql service is not initial')