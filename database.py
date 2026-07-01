import psycopg2

def connect_to_database():
    try:
        pass
        connection = psycopg2.connect(
            host="localhost",
            port = 2004,
            database="banksystemmanagement",
            user="postgres",
            password="Gargi@2004"
        )
        print("Connection to the database was successful.")
        return connection
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
    


    
if __name__ == "__main__":
    conn = connect_to_database()
    if conn :
        conn.close()
        print("Connection closed. ")