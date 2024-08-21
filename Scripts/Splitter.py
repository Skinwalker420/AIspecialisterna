import os
import json
import math

def _init():
    print("File location? ")
    file_location = input()
    file_location = str(file_location)
    print("File max size? (Mb)")
    max_size = input()
    print("output location? ")
    output_location = input()
    print("File name? ")
    name = input()
    max_size = int(max_size)* 1000000

    print(file_location)
    try:
        with open(file_location, 'r') as json_file:
            file_size = os.path.getsize(file_location)
            print(file_size)
            files_amount = int(math.ceil(file_size/max_size))
            print(files_amount)
            text = json_file.readlines()
            max_text = int(math.ceil(len(text)/files_amount))
            time = 1
            line = 0
            while(time <= files_amount):
                location = output_location +"/"+ name + "%d.json" %time
                #os.mkdir(location)
                print(location)
                with open(location, 'w') as file:
                    print("wawaw")
                    full_text = []
                    for i in range(max_text):
                        full_text.append(text[line])
                        line = line + 1
                    json.dump(full_text, file, indent = 4)  
                print("häng mig")      
                time = time + 1
                print(time)


    except Exception as e:
        print(e)

_init()