from nltk.tokenize import sent_tokenize
import nltk.data
import json

filePath = "/home/tempvm/Dumps/Sentence.json"
text = ("Äktenskap Här hittar du information om vad som gäller när ni ska gifta er i Sverige "
        "eller utomlands, eller omvandla ett tidigare partnerskap till ett äktenskap. Ansök om "
        "hindersprövning Innan ni kan gifta er i Sverige måste ni ansöka om hindersprövning. "
        "Ansök genom att fylla i en blankett som ni skickar till Skatteverket. Det är viktigt att ni "
        "lämnar in er ansökan i god tid före vigseln.Före vigseln – hindersprövning Vigsel i Sverige "
        "eller i utlandet Läs om vilka regler som gäller då ni gifter er i Sverige eller i utlandet, och hur "
        "det går till.Att gifta sig i Sverige eller i utlandet Skilsmässa Läs om vilka regler som gäller då ni "
        "vill skilja er eller upplösa ett partnerskap och hur det går till. Läs även vad ni behöver göra om ni "
        "skilt er utomlands.Skilsmässa Äktenskapsregistret I äktenskapsregistret registreras bland annat "
        "äktenskapsförord, gåvor mellan makar och bodelningshandlingar.Äktenskapsregistret")

tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
sentences = sent_tokenize(text)
print(sentences)
# Output the sentences
with open(filePath, 'w') as json_file:
     json.dump(sentences, json_file, indent=4)
print(f"Data successfully saved to {filePath}")
