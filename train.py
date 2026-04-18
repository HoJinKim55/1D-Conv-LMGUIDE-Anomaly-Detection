import torch
from model import FaultDiagnosisModel
from challengedata import ChallengeData
import matplotlib.pyplot as plt
PATH = "data"

train_dataset = ChallengeData(path = PATH, flag = 'train')
test_dataset = ChallengeData(path = PATH, flag = 'test')

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=1, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=False)

device = torch.device('cuda')
model = FaultDiagnosisModel(input_channel= 3, num_classes= 3)
# summary(model, (torch.randn(3, 50001)))
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


# loss_func = torch.nn.BCELoss()
# loss_func = torch.nn.MSELoss()
# loss_func = torch.nn.L1Loss()
loss_func = torch.nn.CrossEntropyLoss()

def train_one_epoch(model, data_loader, optimizer):
    
    model.train()
    model.to(device)
    
    sum_loss = 0.0
    len_data = len(data_loader.dataset)
    
    for sound, label in data_loader:
        optimizer.zero_grad()

        sound = sound.to(device).float()
        label = label.to(device).long()
        pred = model(sound).float()

        # print(sound)target.squeeze(dim=-1)
        loss = loss_func(pred, label)

        
        loss.backward()
        optimizer.step()
        sum_loss += loss.item()
    
    return sum_loss/len_data

def test_one_epoch(model, data_loader):
    with torch.no_grad():
        model.eval()
        model.to(device)

        sum_loss = 0.0
        len_data = len(data_loader.dataset)
        
        for sound, label in data_loader:

            sound = sound.to(device).float()
            label = label.to(device).float()

            pred = model(sound).float()

            loss = loss_func(pred, label)
            
            sum_loss += loss.item()
        return sum_loss/len_data

epoch_arr = []
loss_arr = []

def main():
    initial_forloss = float("inf") 
    for epoch in range(1, 41):
        train_loss = train_one_epoch(model, train_loader, optimizer)
        test_loss = test_one_epoch(model, test_loader)

        if test_loss < initial_forloss:
            initial_forloss = test_loss
            torch.save(model, 'gpp.pth')
            print(f'      ---- epoch {epoch}에서 가중치 저장됨 -------    ')
        print(f'epoch : {epoch}, train loss : {train_loss}')

        epoch_arr.append(epoch)
        loss_arr.append(test_loss)

        plt.plot(epoch_arr, loss_arr)
    plt.show()


main()
