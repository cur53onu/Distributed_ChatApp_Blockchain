from UserAuth import UserAuth as userAuth
from InteractDeployContracts import InteractDeployContracts


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
    # register('cur53','cur53')
    login("cur53", "cur53")
    interact()
    logout()
