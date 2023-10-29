import socket, mysql.connector, configparser

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.10', 7777))

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


while(1):
    full_msg = ""
    new_msg = True
    while(1):
        msg = s.recv(10)
        if new_msg:
            print(f"\nnew message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode('utf-8')

        if len(full_msg) - HEADERSIZE == msglen:
            print(full_msg[HEADERSIZE:])
            # cursor.execute("SELECT * FROM Blockchain ORDER BY number DESC LIMIT 1;")
            # result = cursor.fetchall()
            # print(result[0])
            print("full msg recvd\n")
            new_msg = True
            full_msg = ""
