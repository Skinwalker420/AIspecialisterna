file_path = "/home/vinkemnt/test.txt"

def find_name(text):
    name = ""
    lines = [line for line in text.splitlines() if line.strip()]
    for i in lines[0]:
        if(i == "|"):
            break
        name += i
    print(name)
    return name

def clean(text = 0):
    if(text == 0):
        print("type text here: ")
        text = input()
    englishFound = False
    kontaktFound = False
    name = find_name(text)
    lines = [line for line in text.splitlines() if line.strip()]

    textlength = len(lines)

    for i in range(textlength):
        if(lines[i] == "Engelska (English)"):
            lines[i] = ""
            englishFound = True
        if(lines[i] == "Kontakta oss" and englishFound):
            kontaktFound = True
        if(not englishFound or kontaktFound):
            lines[i] = ""
    lines = [line for line in lines if line.strip()]
    print(lines)
    # with open("haho.txt", 'w', encoding='utf-8') as file:
    #     for i in lines:
    #         file.write(i)
    #         file.newlines
    
clean()