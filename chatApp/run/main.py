import os
from ExitHandler import exit_handler
from UserAuth import UserAuth as userAuth
from InteractDeployContracts import InteractDeployContracts
import subprocess as sp
filepath = os.path.dirname(os.path.abspath(__file__))
def logout():
    u = userAuth()
    u.Logout()


def register(username, password):
    u = userAuth()
    u.Register(username, password)


def interact(username, password):
    user = InteractDeployContracts(username, password)
    user.run()
    return user

def runApplication():
    try:
        val = input("New Contract Instance : ")
        if val == "y":
            print(sp.getoutput("../../deploy.sh"))
            path="../../deploy.sh"
            output = sp.getoutput(path)
            print(output)

        print("1)Register\n2)Login")
        choice = int(input("Enter Your Choice : "))
        if choice == 1:
            print("1)Don't have a public address \n2)Have a public address")
            if int(input("choice: ")) == 1:
                u=userAuth()
                u.PrepRegister()

            strRegister = ">>> Register <<<\nMake sure your account have ethers" + "\nEnter Username and Password"
            print(strRegister)
            username = input("username:")
            password = input("password:")
            register(username, password)
        strLogin = ">>> Login <<<" + "\nEnter Username and Password"
        print(strLogin)
        username = input("username:")
        password = input("password:")
        interact(username, password)
    except EOFError:
        pass

def main():
    try:
        runApplication()
    except:
        print()
    finally:
        exit_handler()

if __name__ == '__main__':
    main()