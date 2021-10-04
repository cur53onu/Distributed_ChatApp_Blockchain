import os
def exit_handler():
    print('Cleaning up!!!')
    login_file = "JSON_Files/userdata.txt"
    try:
        os.remove(login_file)
    except:
        pass
    temp_file = "JSON_Files/temp.txt"
    try:
        os.remove(temp_file)
    except:
        pass