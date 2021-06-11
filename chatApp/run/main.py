from userauth.UserAuth import UserAuth as userAuth
from core.InteractDeployContracts import InteractDeployContracts


def login(username, password):
    u = userAuth()
    u.Login(username, password)


def logout():
    u = userAuth()
    u.Logout()


def register(username, password):
    u = userAuth()
    u.Register(username, password)


def interact():
    user = InteractDeployContracts()
    return user


if __name__ == '__main__':
    login("cur53", "cur53")
    print(interact())
    logout()
