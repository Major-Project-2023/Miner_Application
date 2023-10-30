import socket, mysql.connector, configparser, pickle

# Here connecting to the Database
config = configparser.ConfigParser()
config.read("config.ini")
db_config = {
    "host": config.get("database", "host"),
    "user": config.get("database", "user"),
    "password": config.get("database", "password"),
    "database": config.get("database", "database")
}
# Create a connection
connection = mysql.connector.connect(**db_config)
# Creating a cursor
cursor = connection.cursor()

# Here we are connecting to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('__IP_ADDRESS__', __port__))
s.connect((config.get("socket", "ip"), int(config.get("socket", "port"))))

while(1):
    received_data = s.recv(1024)
    data = pickle.loads(received_data)
    try:
        for i in range(len(data)):
            data_to_insert = [data[i][0], data[i][1], str(data[i][2])]
            insert_query ="INSERT INTO Pool (sender_country, receiver_country, amount) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, data_to_insert)
            print(f"Data i.e. {data_to_insert} was inserted")
        connection.commit()
    except Exception as e:
        pass