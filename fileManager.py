from datetime import date
import json
import os
import validators

def write_json(data, path):
    #Ensure the path is valid json file path
    validators.is_file_path(path)

    # Write the updated data back to the file
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

"""
Create a file in a given path
"""
def new_file_json(path):
    #Ensure the path is valid json file path
    validators.is_file_path(path)

    # Check if the current.json file exists and if not, create it with an empty dict
    if not os.path.exists(path):
        with open(path, 'w') as file:
            pass

def delete_file(path):
    validators.is_file_path(path)

    if os.path.exists(path):
        os.remove(path)

#Read JSON into a dict
def read_json(path, is_list = False):
    validators.is_file_path(path)
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                data = json.load(file)
                print(f"JSON successfully decoded from {path}")
                return data
        else:
            print(f"File {path} does not exist, creating file")
            new_file_json(path)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {path}: {e}")

    if(is_list):
        print("Returning an empty list")
        return []
    else:
        print("Returning an empty dictionary")
        return {}
def first_file_from_shelf(path):
    try:
        first_file = os.listdir(path)[0]
        return first_file
    except IndexError:
        return ""

def dates_match(date_today, file_date):
    for i in range(2, -1, -1):
        if (date_today[i] != file_date[i]):
            return False
    return True

def store_in_shelf(dict, shelf_path):
    first_file_in_shelf = first_file_from_shelf(shelf_path)
    print(f"the first file: {first_file_in_shelf}")

    today = str(date.today())
    #If there are not any files in the shelf create the first one
    ending_number = "001"
    if (not first_file_in_shelf == ""):
        #Check if a file was already created into the shelf today
        today_components = today.split("-")
        name_no_ext = os.path.splitext(first_file_in_shelf)[0] #remove .json at the end
        file_date_comps = name_no_ext.split('-')
        print(f"today: {today}")
        #If the date at the moment is the same as first file's date in shelf,
        # grow the order number in the new file's name
        if(dates_match(today_components, file_date_comps)):
            file_ending_number = file_date_comps[-1]
            new_number = int(file_ending_number)+1
            ending_number = f"{new_number:03}" #3 digits padded with leading 0s

    shelf_file_name = today + '-' + ending_number + '.json'
    shelf_file_path = os.path.join(shelf_path, shelf_file_name)
    new_file_json(shelf_file_path)
    write_json(dict, shelf_file_path)
