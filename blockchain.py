
import pickle
import time
from hashlib import sha256


class BlockChain:

    def __init__(self, genesis_hash="0000000000", difficulty=3):
        self.genesis_hash = genesis_hash
        self.blocks = []
        self.index = 0
        self.difficulty = difficulty


    def append(self,transactions):
        self.index += 1
        if len(self.blocks) > 0:
            previous_hash = self.blocks[-1].hash
        else:
            previous_hash = self.genesis_hash
        block = Block(self.index, transactions, time.time(), previous_hash, self.difficulty)
        self.blocks.append(block)

        with open("blockchain.pickle", "bw") as file:
            pickle.dump(self, file)
        
    def update_difficulty(self):
        if self.blocks[-1].nonce + self.blocks[-2].nonce >10_000:
            self.difficulty -=1
        else:
            self.difficulty +=1
        print("New difficulty",  self.difficulty)   

class Block:

    def __init__(self, index, transaction, timestamp, previous_hash, difficulty):
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty

        self.hash = self.compute_hash()

    def compute_hash(self):
        hash = ""
        while not hash.startswith("0" * self.difficulty):
            self.nonce += 1
            string_to_hash = "{0} {1} {2} {3} {4}".format(
                self.index,
                self.transaction,
                self.timestamp,
                self.previous_hash,
                self.nonce
            )
            hash = sha256(string_to_hash.encode("utf-8")).hexdigest()
        print("Nonce",self.nonce)
        print(string_to_hash)
        print(hash)
        return hash

class User:
    def __init__(self, name, kontostand):
        
        self.name=name
        self.kontostand = kontostand

class Transaktion:
    
    # Konstruktor
    def __init__(self, sender, receiver, amount):
        
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self) -> str:
        repr = self.sender.name + " to " +self.receiver.name + " amount" + str(self.amount)
        return repr 

try:
    with open("blockchain.pickle", "br") as file:
        print("Loading saved blockchain")
        current_blockchain = pickle.load(file)
except FileNotFoundError:
    print("Initializig new blockchain")
    current_blockchain = BlockChain()

class Main:

    def create_users(self):
        user1 = User("Peter",  10) 
        user2 = User("Susi",  16)
        user3 = User("Luli",  14)
        user4=  User("Mateo", 15)
        userliste = [user1,user2,user3,user4]
        
        return userliste
    
    def do_transactions(self,userliste):

        user1, user2, user3, user4 = userliste
      
        if user1.kontostand >= 2:
            
            transaction1 =Transaktion(user1,user2)
            blockchain = BlockChain()
            blockchain.append(transaction1)
            print("Aktueller Kontostand User 1 vor Transaktion:", user1.kontostand)
            print("Aktueller Kontostand User 2 vor Transaktion:", user2.kontostand)
            t1= 2
            user1.kontostand -=t1
            print(user1.name,"give to",user2.name,t1)
            user1.kontostand +=t1
            print("Aktueller Kontostand User 1 nach Transaktion:", user1.kontostand)
            print("Aktueller Kontostand User 2 nach Transaktion:", user2.kontostand)
        else:
            print("You should not give money")

        if user3.kontostand >= 2:
            
            transaction2 =Transaktion(user3,user4)
            blockchain.append(transaction2)
            print("Aktueller Kontostand User 3 vor Transaktion:", user3.kontostand)
            print("Aktueller Kontostand User 4 vor Transaktion:", user4.kontostand)
            t2= 5
            user3.kontostand -=t2
            print(user3.name,"give to",user4.name,t2)
            user4.kontostand +=t2
            print("Aktueller Kontostand User 1 nach Transaktion:", user3.kontostand)
            print("Aktueller Kontostand User 2 nach Transaktion:", user4.kontostand)  
            blockchain.update_difficulty()
            
        print("")
        print("Number of transactions: ", blockchain.index)
        print("Number of Blocks",len(blockchain.blocks))

#run only when I direct execute
if __name__ =="__main__":
    main = Main()
    users=main.create_users()
    main.do_transactions(users)