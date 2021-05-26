import sys
from web3 import Web3
import json
import threading
from termcolor import colored,cprint

def help():
    print("Queries:\n1)To get chat room name: /chatroomname? \n2)To get users:/getusers?")


class ChatRooms():
    def __init__(self):
        with open('./JSON_Files/data.json') as data_file:
            data = json.load(data_file)
            self.contract_address = data['contract_address']
            self.user_private_key = data['user_private_key']
            self.infura_node_url = data['infura_node_url']
            self.web3 = Web3(Web3.HTTPProvider(self.infura_node_url))

    def get_user_account(self):
        return self.web3.eth.account.privateKeyToAccount(self.user_private_key)

    def getContractInstance(self):
        with open('JSON_Files/ChatRoom.json') as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(self.contract_address)
            con = self.web3.eth.contract(address=address, abi=abi)
            return con

    def customTransact(self,function):
        builtTransaction = function.buildTransaction({
            'from': self.get_user_account().address,
            'nonce': self.web3.eth.getTransactionCount(self.get_user_account().address),
            'gas': 1728712,
            'gasPrice': self.web3.toWei('21', 'gwei')})
        signed = self.get_user_account().signTransaction(builtTransaction)
        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_hash)
        print(tx_receipt)

    def callGetName(self):
        return self.getContractInstance().functions.getName().call()

    def callGetUsers(self):
        print('>>>',self.getContractInstance().functions.getUsers().call(),end='\n')

    def transactAddUser(self,address_to_add):
        self.customTransact(self.getContractInstance().functions.addUser(address_to_add))

    def transactSetName(self,chatroom_name):
        self.customTransact(self.getContractInstance().functions.setName(chatroom_name))



def run():
    while True:
        chatRooms = ChatRooms()
        user_input = input(colored("#",'cyan',attrs=['bold', 'blink']))
        if (user_input == "/chatroomname?"):
            print(">>>",chatRooms.callGetName(),end='\n')
        elif ('/add' in user_input):
            user_input = user_input.split(' ')
            print(user_input[1])
            chatRooms.transactAddUser(user_input[1])
        elif ('/setchatroomname' in user_input):
            user_input=user_input.split(' ')
            print(user_input[1])
            chatRooms.transactSetName(user_input[1])
        elif ('/getusers?' in user_input):
            chatRooms.callGetUsers()
        else:
            print(user_input)
def showMessages():
    chatRooms=ChatRooms()
    while True:
        if str(chatRooms.callGetName()) == "cur53":
            print("\n$$$",chatRooms.callGetName(),end='\n')
            break

if __name__ == '__main__':
    try:
        # help()
        chatRooms=ChatRooms()
        print(colored(chatRooms.callGetName(), 'red', attrs=['bold', 'blink']))
        t1 = threading.Thread(target=run)
        t2=threading.Thread(target=showMessages())
        t1.start()
        t2.start()

    except KeyboardInterrupt:
        print('\nExiting!!!\n')
        sys.exit(0)
