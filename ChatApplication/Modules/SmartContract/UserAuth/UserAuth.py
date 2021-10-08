import json
import os
import ast
import sys
import os.path
import time

from termcolor import colored
from ChatApplication.Modules.SmartContract.Core.SmartContractInteract import SmartContractInteract as SMC
from ChatApplication.Modules.PrintOutput.print_output import printOutput
filepath=os.path.dirname(os.path.abspath(__file__))

class UserAuth(SMC):
    def __init__(self):
        SMC.__init__(self)
        self.username = None
        self.password = None
        self.register = ""
        self.public_address = None

    def PrepRegister(self):
        if not os.path.isfile(self.getTemporaryDataFileName()):
            web3= SMC.getWeb3(self)
            print(web3)
            account = web3.eth.account.create()
            printOutput("Your Account is Ready For Registration!!!" +
                        "\n>>> Your Public Address is: " + str(account.address) +
                        "\n>>> Transfer some ether to this and come back for registration!!!" + "\n\n" + str(
                account.address) + "\n\n", "blue")
            privatekey_binary=account.privateKey
            with open(self.getTemporaryDataFileName(), "wb") as binary_file:
                binary_file.write(privatekey_binary)
            # self.account = account
            self.user_account = account
            # self.public_address = self.account.address
            self.public_address = self.user_account.address
            return account
        else:
            with open(self.getTemporaryDataFileName(), "rb") as binary_file:
                data = binary_file.read()
                account = (self.web3.eth.account.privateKeyToAccount(data))
                # self.account = account
                self.user_account = account
                self.public_address = account.address
                print('temp file present\nAccount address: ', account.address)

    def Register(self):
        self.PrepRegister()
        if self.callUserAddressExist(self.public_address):
            printOutput(
                "User account with " + self.public_address + " already exist!!!\nCannot create new account with same public address",
                "red")
            return

        if (self.web3.eth.getBalance(self.user_account.address)) == 0:
            printOutput("Wallet empty add some ethers and come back"
                        + " Public Address : " + str(self.user_account.address), 'red')
            printOutput("Waiting till u transfer ",'red')
            while (self.web3.eth.getBalance(self.user_account.address)) == 0:
                pass
            print('\nEthers received.')
            print('Current balance: ', (self.web3.eth.getBalance(self.user_account.address)))
        strRegister = ">>> Register <<<\nMake sure your account have ethers" + "\nEnter Username and Password"
        printOutput(strRegister, "blue")
        self.username = input("username:")
        self.password = input("password:")
        if not os.path.exists(self.getTemporaryDataFileName()):
            printOutput("Run Prepearation Register", 'red')
            return
        if self.userExist(self.username):
            print(colored(">>> Username exist choose different username", 'red'))
            return

        encrypted_password = self.user_account.encrypt(self.password)
        value, account_received = self.transactRegisterUser(self.username, str(encrypted_password))

        if value == True:
            printOutput("Registered successfully..." + "\n>>> Name " + self.username
                        + "\n>>> Public Address: " + str(self.user_account.address), "blue")
        cnt=0
        while not self.callUserAddressExist(self.public_address):
           cnt+=1

        # printOutput("Please wait for sometime until account gets added", "red")
        # time.sleep(15)

    def Login(self):
        self.username = input("username:")
        self.password = input("password:")
        profile_addr = self.userExist(self.username)
        if not profile_addr:
            printOutput("No user", 'red')
            return

        addr = input('Required public address: ')
        self.public_address = addr
        res = ast.literal_eval(self.callGetUserData(addr))
        try:
            privatekey_binary = self.web3.eth.account.decrypt(res, self.password)
            self.user_account = self.web3.eth.account.privateKeyToAccount(privatekey_binary)

            # if os.path.exists(SMC.getUserDataFileName(self)):
            #     os.remove(SMC.getUserDataFileName(self))
            # with open(self.getUserDataFileName(), "wb") as binary_file:
            #     # Write text or bytes to the file
            #     binary_file.write(privatekey_binary)
            # with open(self.getUserDataFileName(), "rb") as binary_file:
            #     data = binary_file.read()
            #     ax = (web3.eth.account.privateKeyToAccount(data))
            #     self.user_account = ax
            printOutput("Logged in..." + "\n>>> Name " + self.username
                        + "\n>>> Public Address: " + str(self.user_account.address)
                        + "\n>>> Balance : " + str(self.web3.eth.getBalance(self.user_account.address)), "blue")
            return True

        except ValueError:
            printOutput("Wrong Password", 'red')
        return False


    def Logout(self):
        if self.user_account:
            self.user_account = None
        else:
            printOutput("Not Logged in", 'red')
            return
        printOutput("Logged Out!!!", 'blue')
