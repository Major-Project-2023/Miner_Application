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
        # data_to_insert = f"'{str(data[0][0])}','{str(data[0][1])}','{str(data[0][2])}'"
        data_to_insert = [data[0][0], data[0][1], str(data[0][2])]
        insert_query = "INSERT INTO Pool (sender_country, receiver_country, amount) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, data_to_insert)
        connection.commit()
        print(f"Data i.e. {data_to_insert} was inserted")
    except Exception as e:
        pass
        # print("Exception",e)
        # print("Data", data)
    # full_msg = ""
    # new_msg = True
    # while(1):
    #     msg = s.recv(10)
    #     if new_msg:
    #         print(f"\nnew message length: {msg[:HEADERSIZE]}")
    #         msglen = int(msg[:HEADERSIZE])
    #         new_msg = False

    #     full_msg += msg.decode('utf-8')

    #     if len(full_msg) - HEADERSIZE == msglen:
    #         print(full_msg[HEADERSIZE:])
    #         # data_to_insert = ('4','000079a280ae6a52c9053e3dfc8fcaedceb9397f50ca6adda7be90a5b348cc7f','00002af91ce372d48bd05f794e833db5a41ff19f271f56b16bde4a4cce50cec7','bye','24066')
    #         data_to_insert = ()
    #         insert_query = "INSERT INTO Blockchain (sender_country, receiver_country, amount) VALUES (%s, %s, %s)"
    #         # cursor.execute(insert_query, data_to_insert)
    #         connection.commit()
    #         print("full msg recvd\n")
    #         new_msg = True
    #         full_msg = ""
# [[<User: sarthak>, <User: NGO2>, 'donor1@donor.com', 'donor1@donor.com', 2]]