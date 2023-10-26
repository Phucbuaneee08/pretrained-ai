import json
import unidecode    

with open('intents.json','r',encoding="utf-8") as f:
    intents = json.load(f,strict = False)
for intent in intents:
    intent['category'] = unidecode.unidecode(intent['question']).lower().replace(" ","-")
    print(intent['category'])
with open('intents.json', 'w', encoding='utf-8') as f:
    json.dump(intents, f, ensure_ascii=False, indent=4)