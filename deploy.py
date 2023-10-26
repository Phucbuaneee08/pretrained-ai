from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import random
import json
import torch
from model import NeuralNet
from nltk_untils import bag_of_words, tokenize

app = FastAPI()

# Load the pre-trained model and tokenizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json','r',encoding="utf-8") as f:
    intents = json.load(f,strict = False)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
categorys = data['categorys']
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()


class Item(BaseModel):
    text: str

@app.post("/predict/")
async def predict(item: Item):
    sentence = item.text
    sentence = tokenize(sentence)
    X = bag_of_words(sentence,all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _,predicted = torch.max(output,dim=1)
    category = categorys[predicted.item()]

    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]
    print(predicted.item())
    if prob.item() > 0.75:
        print(prob.item())
        for situation in intents:
            if situation["category"] == category:
                 return {"text": situation["answer"]}
    else:
        return {"text": "I dont understand ... "}
   

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
