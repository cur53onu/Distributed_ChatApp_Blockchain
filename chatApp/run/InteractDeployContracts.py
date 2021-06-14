from SmartContractInteract import SmartContractInteract as SMC
import os
filepath=os.path.dirname(os.path.abspath(__file__))
class InteractDeployContracts(SMC):
    def __init__(self):
        global filepath
        SMC.__init__(self)
        try:
            with open(filepath + '../JSON_Files/userdata.txt') as data_file:
                pass
        except FileNotFoundError:
            print("Login!!!")