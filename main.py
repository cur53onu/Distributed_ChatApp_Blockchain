import os
import sys
from ChatApplication.Modules.ExitHandler.ExitHandler import exit_handler
from ChatApplication.Modules.SmartContract.UserAuth import UserAuth as userAuth
from ChatApplication.Modules.SmartContract.InteractDeployContracts import InteractDeployContracts
from Naked.toolshed.shell import execute_js
filepath = os.path.dirname(os.path.abspath(__file__))
def logout():
    u = userAuth()
    u.Logout()


def register():
    interactDeployedContractsRegister = InteractDeployContracts()
    interactDeployedContractsRegister.PrepRegister()
    strRegister = ">>> Register <<<\nMake sure your account have ethers" + "\nEnter Username and Password"
    print(strRegister)
    interactDeployedContractsRegister.Register()
    login()


def login():
    strLogin = ">>> Login <<<" + "\nEnter Username and Password"
    print(strLogin)
    username = input("username:")
    password = input("password:")
    user = InteractDeployContracts()
    user.setUserNameAndPassword(username,password)
    user.run()
    return user

def runApplication():
    try:
        # val = input("New Contract Instance : ")
        # if val == "y":
        #     deployjs_path="../../ethereum/deploy.js"
        #     success = execute_js(deployjs_path)
        #     if not success:
        #         sys.exit(0)
        print("1)Register\n2)Login")
        choice = int(input("Enter Your Choice : "))
        if choice == 1:
            register()
        else:
            login()
    except EOFError:
        pass

def main():
    try:
        runApplication()
    except:
        print()
    # finally:
    #     exit_handler()

if __name__ == '__main__':
    main()