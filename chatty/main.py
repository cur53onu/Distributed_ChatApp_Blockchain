import sys
import os
from web3 import Web3
import time
from termcolor import colored
# from smart_contracts_interact.core import
from smart_contracts_interact import ChatRoom as Room
from smart_contracts_interact.authenticate_users import Profile as prof
from smart_contracts_interact.authenticate_users.Authenticate import Auth
act=''

def help():
    print("Queries:\n1)To get chat room name: /chatroomname? \n2)To get users:/getusers?")


def run():
    while True:
        # register()
        chatRooms = Room.ChatRoom
        profile=prof.Profile
        auth = Auth()
        user_input = input(colored("#", 'cyan'))
        if (user_input == "/?"):
            print(">>>", chatRooms.callGetName(self=chatRooms), end='\n')
        elif ('/add' in user_input):
            user_input = user_input.split(' ')
            print(user_input[1])
            # chatRooms.transactAddUser(user_input[1])
        elif ('/setchatroomname' in user_input):
            user_input = user_input.split(' ')
            print(user_input[1])
            start = time.time()
            chatRooms.transactSetName(chatRooms, user_input[1])
            end = time.time()
            print("time taken: ", end - start)
        elif ('/getusers?' in user_input):
            print(chatRooms.callGetUsers(self=chatRooms))
        elif ('/getprofile?' in user_input):
            user_input=user_input.split(" ")
            print(profile.callGetUsers(profile,user_input[1])[1])
        elif ('/adp' in user_input):

            user_input = user_input.split(' ')

            # auth.Register(user_input[1],user_input[2])
            web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/0a5866cdc4fb48d8808e336cd05a68ff"))
            # global act
            acct=web3.eth.account.create()
            # act=acct
            # print(act)
            # print(act.privateKey)
            encrypted=acct.encrypt(user_input[2])
            str_encrypted=str(encrypted)
            auth=Auth()
            auth.Register(user_input[1],user_input[2])
            # profile.transactAddUser(profile,user_input[1],str_encrypted)
            # # chatRooms.transactAddUser(chatRooms,user_input[1],str_encrypted)
            # chatRooms.callGetUsers(chatRooms)
            # profile.transactAddUser(profile,user_input[1],"x")
        elif ('/login' in user_input):
            user_input = user_input.split(" ")
            web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/0a5866cdc4fb48d8808e336cd05a68ff"))
            # res=ast.literal_eval(profile.callGetUsers(profile, user_input[1])[1])
            # restored = web3.eth.account.privateKeyToAccount(web3.eth.account.decrypt(res, user_input[2]))
            # print(restored)
            auth.Login(user_input[1],user_input[2])
        elif('/prepreg' in user_input):
            pr=prof.Profile()
            if os.path.exists(pr.getTemporaryDataFileName()):
                os.remove(pr.getTemporaryDataFileName())
            auth=Auth()
            account=auth.PrepRegister()
            with open(pr.getTemporaryDataFileName(), "wb") as binary_file:
                # Write text or bytes to the file
                print(account.address)
                binary_file.write(account.privateKey)
        else:
            print(user_input)


# def showMessages():
# chatRooms=ChatRoom()
# while True:
#     if str(chatRooms.callGetName()) == "cur53":
#         print("\n$$$",chatRooms.callGetName(),end='\n')
#         break

def login():
    print("Login\n")

    while True:
        user_input = input(colored("#", 'cyan'))
        auth = Auth()
        profile=prof.Profile()
        if ("/getprofile?" in user_input):
            user_input=user_input.split(' ')
            print(auth.callGetUsers(user_input[1]))
        elif("/prepreg"==user_input):
            pr = prof.Profile()
            if os.path.exists(pr.getTemporaryDataFileName()):
                os.remove(pr.getTemporaryDataFileName())
            account = auth.PrepRegister()
            with open(pr.getTemporaryDataFileName(), "wb") as binary_file:
                # Write text or bytes to the file
                binary_file.write(account.privateKey)
        elif("/register" in user_input):
            user_input=user_input.split(' ')
            auth.Register(user_input[1], user_input[2])
        elif("/login" in user_input):
            user_input=user_input.split(' ')
            auth.Login(user_input[1], user_input[2])

            # if auth.Login(user_input[1], user_input[2]):
            #     print('yuppy')
        elif("/logout"==user_input):
            auth.Logout()
        elif("/deploychat" in user_input):
            user_input = user_input.split(' ')
            r=Room.ChatRoom()
            r.deployChatRoom(user_input[1],user_input[2])
        elif("/getchatroom?" in user_input):
            user_input = user_input.split(' ')
            r = Room.ChatRoom()
            print(r.callGetChatRoomAddress(user_input[1]))


        else:
            print(user_input)

#
if __name__ == '__main__':
    try:
        # help()
        # chatRooms=ChatRooms()
        # print(colored(chatRooms.callGetName(), 'red', attrs=['bold', 'blink']))
        # t1 = threading.Thread(target=run)
        # t2=threading.Thread(target=showMessages())
        # t1.start()
        # t2.start()
        login()

        # run()


    except KeyboardInterrupt:
        print('\nExiting!!!\n')
        auth=Auth()
        auth.Clear()
        sys.exit(0)

# acct=web3.eth.account.privateKeyToAccount("0x5a38cd08daef780aef7fd4225bb190911250bb1d548f8baec83ac9b2feceff41")
# keystore=acct.encrypt("sumeet")
# data=chatRooms.callGetName()
# res=ast.literal_eval(data)
# restored=web3.eth.account.privateKeyToAccount(web3.eth.account.decrypt(res, "sumeet"))
# print(restored == acct)
# print(restored.privateKey==acct.privateKey)
