import PIL.Image
from PIL import ImageTk
import os

import fileManager

def show_image(word, img_folder, img_holder):
    image_name = word + ".png"
    image_path = os.path.join(img_folder, image_name)

    if os.path.isfile(image_path):
        img = PIL.Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        img_holder.config(image=photo)
        img_holder.image = photo
def gather_data(current_words_path, shelf_path, max_words):

    # Check if there is space for new data
    current_words = fileManager.read_json(current_words_path)
    word_count = len(current_words)

    while (word_count < max_words):
        # Search for oldest dir in the shelf
        first_file = fileManager.first_file_from_shelf(shelf_path)
        if(first_file == ""):
            break

        print(f"Getting data from the oldest file: {first_file}, in dir: {shelf_path}")
        # Get all the data from the oldest shelf file
        shelf_file_path = os.path.join(shelf_path, first_file)
        shelf_words = fileManager.read_json(shelf_file_path)
        shelf_count = len(shelf_words)

        #Merge all the words into the current words if they fit
        #otherwise take only part of them,
        # update/ delete the shelf file
        if(shelf_count + word_count <= max_words ):
            word_count += shelf_count
            current_words.update(shelf_words)

            # Delete the file
            print("deleting the file: " , shelf_file_path)
            fileManager.delete_file(shelf_file_path)
        else:
            needed_count = max_words - word_count
            data_cut = dict(list(shelf_words.items())[:needed_count])
            current_words.update(data_cut)
            word_count = max_words

            # Update the file in shelf
            print(f"updating with : {shelf_file_path}")
            fileManager.write_json(shelf_words, shelf_file_path)

    # After data gathering update the current.json file
    fileManager.write_json(current_words, current_words_path)
    return current_words
