# Connecting with MySQL
# Importing the connection variables
import mysql.connector, configparser, time

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

from hashlib import sha256

class Block:
    difficulty = 4
    
    def __init__(self, data):
        cursor.execute("SELECT * FROM Blockchain ORDER BY number DESC LIMIT 1;")
        result = cursor.fetchall()
        try:
            last_block = {
                "block_number":result[0][0],
                "current_hash":result[0][1],
            }
        except:
            last_block = {
                "block_number":"0",
                "current_hash":"0"*64,
            }
        self.block_data = data
        self.block_number = str(int(last_block["block_number"]) + 1)
        self.previous_hash = last_block["current_hash"]
        self.block_nonce = 0
        self.block_hash = self.hash()
    
    def __str__(self):
        return str(f"Block Number: {self.block_number} Previous Hash: {self.previous_hash} Block Data: {self.block_data} Block Nonce: {self.block_nonce} Block Hash: {self.block_hash}")
    
    def updatehash(self,*args):
        data = ""
        h = sha256()
        for arg in args:
            data += str(arg)
        h.update(data.encode('utf-8'))
        return h.hexdigest()
    
    def hash(self):
        return self.updatehash(
            self.previous_hash,
            self.block_number,
            self.block_data,
            self.block_nonce
        )
    
    def mine_block(self):
        while(1):
            print(self.block_nonce)
            print(self.block_hash)
            if(self.block_hash[:self.difficulty] == '0'*self.difficulty):
                break
            else:
                self.block_nonce += 1
                self.block_hash = self.hash()
    
    def add_block(self):
        self.mine_block()
        print(self)
        self.save_to_database()
    
    def save_to_database(self):
        data_to_insert = [str(self.block_number), str(self.block_hash), str(self.previous_hash), str(self.block_data), str(self.block_nonce)]
        insert_query ="INSERT INTO Blockchain (number, hash, previous, data, nonce) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, data_to_insert)
        cursor.execute('DELETE FROM Pool')
        connection.commit()
        # cursor.execute("INSERT INTO Blockchain VALUES('10','HASH', 'PREV', 'DATA', 'NONCE');")
        # cursor.execute("SELECT * FROM Blockchain ORDER BY number DESC LIMIT 1;")
        # result = cursor.fetchall()
        # print(result[0])
    
    def is_valid(self):
        pass

while(1):
    time.sleep(60)
    cursor.execute("SELECT * FROM Pool;")
    result = cursor.fetchall()
    block = Block(result)
    block.add_block()
    # print("\nRESULT",result)
