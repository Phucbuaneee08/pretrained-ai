import json
import nltk_untils
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
with open('intents.json','r',encoding="utf-8") as f:
    intents = json.load(f,strict = False)
categorys = []
all_words = []
xy = []
for situation in intents:
    cat = situation['category']
    categorys.append(cat)
    
    ques = situation['question']
    w = nltk_untils.tokenize(ques)
    all_words.extend(w)
    xy.append((w,cat))
ignore_words = ['?','!','.',',']
all_words= [nltk_untils.stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words),key=lambda x:all_words.index(x))
categorys = sorted(set(categorys))


X_train = []
Y_train = []
for(pattern_sentence, category) in xy:
    bag = nltk_untils.bag_of_words(pattern_sentence,all_words)
    X_train.append(bag)

    label = categorys.index(category)
    Y_train.append(label)
X_train = np.array(X_train)
Y_train = np.array(Y_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train
    def __getitem__(self,index):
        return self.x_data[index], self.y_data[index]
    def __len__(self):
        return self.n_samples
    


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,batch_size=8,shuffle=True, num_workers=0)

num_epochs = 1000
hidden_size = 8
input_size = len( X_train[0])
output_size = len(categorys)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size,hidden_size,output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)




for epoch in range(num_epochs):
    for(words,labels) in train_loader:
            words = words.to(device)
            labels = labels.to(torch.long)
            
            outputs = model(words)
            loss = criterion(outputs,labels)

            #backward and optimizer
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')
print(f'final Loss, loss={loss.item():.4f}')

data={
    "model_state":model.state_dict(),
    "input_size":input_size,
    "hidden_size":hidden_size,
    "output_size":output_size,
    "all_words":all_words,
    "categorys":categorys
}
FILE = "data.pth"
torch.save(data,FILE)

print(f'training compelte. file save to {FILE}')