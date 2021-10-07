import json
import os
def exit_handler():
    print('Cleaning up!!!')
    json_default_file = 'JSON_Files/default.json'
    opened_default_file = open(json_default_file, "r")
    json_obj = json.load(opened_default_file)
    address = json_obj["contract_deploycontracts_address"]
    opened_default_file.close()
    json_data_file = 'JSON_Files/data.json'
    opened_json_data_file_read = open(json_data_file,"r")
    data = json.load(opened_json_data_file_read)
    if data["contract_deploycontracts_address"] != address:
        opened_json_data_file_write = open(json_data_file, "w")
        data["contract_deploycontracts_address"] = address
        json.dump(data, opened_json_data_file_write)
        opened_json_data_file_write.close()
    opened_json_data_file_read.close()
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