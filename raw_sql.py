import mysql.connector
  
# Connecting to the Database
mydb = mysql.connector.connect(
  host ='localhost',
  database ='vhos',
  user ='root',
  password = ''
)
def update_services_price(id, s_name, price):
    cs = mydb.cursor()
    statement =f"""UPDATE services 
                SET price = '{price}' 
                WHERE 
                service_name ='{s_name}'
                AND
                asp_id = '{id}'
                """
    
    print(cs.execute(statement))
    mydb.commit()
    
    # Disconnecting from the database



