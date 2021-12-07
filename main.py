import json
import os
import sys
from ChatApplication.Modules.ExitHandler.ExitHandler import exit_handler
from ChatApplication.Modules.SmartContract.Core.SmartContractInteract import SmartContractInteract
from ChatApplication.Modules.SmartContract.UserAuth import UserAuth as userAuth
from ChatApplication.Modules.SmartContract.InteractDeployContracts import InteractDeployContracts
from ChatApplication.Modules.PrintOutput.print_output import printOutput
from Naked.toolshed.shell import execute_js
filepath = os.path.dirname(os.path.abspath(__file__))


def logout():
    u = userAuth()
    u.Logout()


class MainClass:

    def __init__(self):
        self.smc = SmartContractInteract()
        self.interactDeployedContracts = InteractDeployContracts()

    def register(self):
        self.interactDeployedContracts.register()
        self.login()

    def login(self):
        strLogin = ">>> Login <<<" + "\nEnter Username and Password"
        print(strLogin)
        self.interactDeployedContracts.run()

    def handleContractInstance(self):
        val = input(
            "1)New Contract Instance\n2)Join Contract Instance\nPress Enter to join default world\nchoice:")
        if val == "":
            return
        if int(val) == 1:
            deployjs_path = "ethereum/deploy.js"
            success = execute_js(deployjs_path)
            if not success:
                printOutput("Error deploying your new contract!!!", "red")
                sys.exit(0)
        if int(val) == 2:
            address = input("Enter contract address to join: ")
            json_file = 'JSON_Files/data.json'
            opened_file = open(json_file, "r")
            json_obj = json.load(opened_file)
            opened_file.close()
            json_obj["contract_deploycontracts_address"] = address
            opened_file = open(json_file, "w")
            json.dump(json_obj, opened_file)
            opened_file.close()

    def logout(self):
        self.interactDeployedContracts.Logout()


def runApplication(mainClassObj):
    try:
        mainClassObj.handleContractInstance()
        print("1)Register\n2)Login")
        choice = int(input("Enter Your Choice : "))
        if choice == 1:
            mainClassObj.register()
        else:
            mainClassObj.login()
        # mainClassObj.login()

    except EOFError:
        pass


def main():
    mainClassObj = MainClass()
    runApplication(mainClassObj)
    # try:
    #     runApplication(mainClassObj)
    # except:
    #     print('Error')
    # finally:
    #     pass
        #mainClassObj.logout()
        #exit_handler()


if __name__ == '__main__':
    main()
