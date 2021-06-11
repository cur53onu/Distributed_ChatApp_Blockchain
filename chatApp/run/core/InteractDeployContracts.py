from .SmartContractInteract import SmartContractInteract as SMC

class InteractDeployContracts(SMC):
    def __init__(self):
        SMC.__init__(self)
        try:
            with open('JSON_Files/userdata.txt') as data_file:
                pass
        except FileNotFoundError:
            print("Login!!!")