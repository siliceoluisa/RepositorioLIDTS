import psycopg2

dbname = "repositoriolidts"
user = "postgres"       
password = "admin"       
host = "localhost"               
port = "5432"

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    cursor = conn.cursor()
    
    print("¡Conexión exitosa a la base de datos PostgreSQL!")

except Exception as e:
    print(f"No se pudo conectar a la base de datos. Error: {e}")
