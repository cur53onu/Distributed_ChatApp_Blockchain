from UserAuth import UserAuth as userAuth
from InteractDeployContracts import InteractDeployContracts


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
    print("1)Register\n2)Login")
    choice = int(input("Enter Your Choice : "))
    if choice == 1:
        print("1)Don't have a public address \n2)Have a public address")
        if int(input("choice: ")) == 1:
            u=userAuth()
            u.PrepRegister()
            exit(0)
        strRegister = ">>> Register <<<" + "\nEnter Username and Password"
        print(strRegister)
        username = input("username:")
        password = input("password:")
        register(username, password)
    strLogin = ">>> Login <<<" + "\nEnter Username and Password"
    print(strLogin)
    username = input("username:")
    password = input("password:")
    interact(username, password)
