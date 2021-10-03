import os
import ast
from termcolor import colored
from SmartContractInteract import SmartContractInteract as SMC
from print_output import printOutput
filepath=os.path.dirname(os.path.abspath(__file__))

class UserAuth(SMC):
    def __init__(self):
        SMC.__init__(self)
        self.register = ""
        self.account = None
        pass

    def PrepRegister(self):
        web3= SMC.getWeb3(self)
        print(web3)
        account = web3.eth.account.create()
        printOutput("Your Account is Ready For Registration!!!" +
                    "\n>>> Your Public Address is: " + str(account.address) +
                    "\n>>> Transfer some ether to this and come back for registration!!!" + "\n\n" + str(
            account.address) + "\n\n", "blue")
        privatekey_binary=account.privateKey
        with open(os.path.join(os.path.dirname(__file__), SMC.getTemporaryDataFileName(self)), "wb") as binary_file:
            binary_file.write(privatekey_binary)
        return account

    def Register(self, user_name, password):
        web3 = SMC.getWeb3(self)
        if not os.path.exists(os.path.join(os.path.dirname(__file__), SMC.getTemporaryDataFileName(self))):
            printOutput("Run Prepearation Register", 'red')
            return
        if SMC.userExist(self,user_name):
            print(colored(">>> Username exist choose different username", 'red'))
            return

        with open(SMC.getTemporaryDataFileName(self), "rb") as binary_file:
            data = binary_file.read()
            ax = (web3.eth.account.privateKeyToAccount(data))
            self.account = ax

        if (self.web3.eth.getBalance(self.account.address)) == 0:
            printOutput("Wallet empty add some ethers and come back"
                        + " Public Address : " + str(self.account.address), 'red')
            return

        encrypted = self.account.encrypt(password)
        instance = UserAuth()
        value, account_received = instance.customTransact(
            self.getContractInstance().functions.deployProfiles(user_name, str(encrypted)))
        self.account = account_received
        if value == True:
            printOutput("Registered successfully..." + "\n>>> Name " + user_name
                        + "\n>>> Public Address: " + str(self.account), "blue")

    def Login(self, username, password):
        web3 = SMC.getWeb3(self)
        profile_addr = SMC.userExist(self, username)
        if not profile_addr:
            printOutput("No user", 'red')
            return

        res = ast.literal_eval(SMC.callGetUserData(self, name=username))
        try:
            privatekey_binary = self.web3.eth.account.decrypt(res, password)
            restored = self.web3.eth.account.privateKeyToAccount(privatekey_binary)
            if os.path.exists(SMC.getUserDataFileName(self)):
                os.remove(SMC.getUserDataFileName(self))
            with open(os.path.join(os.path.dirname(__file__),SMC.getUserDataFileName(self)), "wb") as binary_file:
                # Write text or bytes to the file
                binary_file.write(privatekey_binary)
            with open(SMC.getUserDataFileName(self), "rb") as binary_file:
                data = binary_file.read()
                ax = (web3.eth.account.privateKeyToAccount(data))
                self.account = ax
            printOutput("Logged in..." + "\n>>> Name " + username
                        + "\n>>> Public Address: " + str(self.account.address)
                        + "\n>>> Balance : " + str(self.web3.eth.getBalance(self.account.address)), "blue")
            return True

        except ValueError:
            printOutput("Wrong Password", 'red')
        return False

    def Clear(self):
        if os.path.exists(SMC.getUserDataFileName(self)):
            os.remove(SMC.getUserDataFileName(self))

    def Logout(self):
        if os.path.exists(SMC.getUserDataFileName(self)):
            os.remove(SMC.getUserDataFileName(self))
        else:
            printOutput("Not Logged in", 'red')
            return
        self.account = None
        printOutput("Logged Out!!!", 'blue')
