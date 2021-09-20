import os

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


if __name__ == '__main__':
    # register('cur53','cur53')
    try:
        val = input("New Contract Instance : ")
        if val == "y":
            # output = sp.getoutput("../../deploy.sh")
            path=os.path.join(os.path.dirname(__file__), '../../deploy.sh')
            print(sp.getoutput("pwd"))
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