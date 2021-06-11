from userauth.UserAuth import UserAuth as userAuth

def main():
    u=userAuth()
    # u.PrepRegister()
    u.Register("k","sk")
    # u.Login("cur53","cur53")
if __name__ == '__main__':
    main()
