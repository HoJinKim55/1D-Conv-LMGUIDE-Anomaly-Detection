import torch
import torch.nn as nn


class GlobalPowerPooling(torch.nn.Module):
    def __init__(self):
        super(GlobalPowerPooling, self).__init__()
    
    def forward(self, x):
        return torch.mean(x ** 2, dim=2)
    
    

class FaultDiagnosisModel(nn.Module):
    def __init__(self, input_channel, num_classes):
        super(FaultDiagnosisModel, self).__init__()
        
        self.input_channel_ = input_channel
        self.num_classes_ = num_classes
        self.hidden_size = 0

        self.feature_extractor_ = nn.Sequential(
            #1층
            nn.Conv1d(in_channels = self.input_channel_, out_channels= 4,
                       kernel_size=7, dilation=2, bias=False),
            nn.Softsign(),

            #2층
            nn.Conv1d(in_channels = 4, out_channels = 4,
                       kernel_size=7,  dilation=2,  bias=False),
            nn.Softsign(),
            

            #3층
            nn.Conv1d(in_channels= 4, out_channels = 8,
                       kernel_size=7, dilation=2, bias=False),
            nn.Softsign(),
            

            #4층
            nn.Conv1d(in_channels=8, out_channels=8,
                       kernel_size=7, dilation=2, bias=False),
            nn.Softsign(),

            #5층
            nn.Conv1d(in_channels=8, out_channels=16,
                       kernel_size=7, dilation=2, bias=False),
            nn.Softsign(),
            

            #6층
            nn.Conv1d(in_channels=16, out_channels=16,
                       kernel_size=7, dilation=2, bias=False),
            nn.Softsign(),
        )
        self.sigmoid = nn.Sigmoid()

        # max pooling
        self.max_pool_ = nn.MaxPool1d(kernel_size=2, stride=2)

        # global average pooling
        self.gap_ = nn.AdaptiveAvgPool1d(1)

        # global power pooling
        self.gpp_ = GlobalPowerPooling()

        #fully connected
        
        self.fc_1 = nn.Linear(16, 8)
        self.fc_2 = nn.Linear(8, num_classes)



    def forward(self, x):
        x = self.feature_extractor_(x)
        x = self.gpp_(x)

        x = self.fc_1(x)
        x = self.fc_2(x)
        return x
    

if __name__ == '__main__':
    model = FaultDiagnosisModel(input_channel=3, num_classes=3)
    input_data = torch.randn(32, 3, 300)  
    output = model(input_data)
    print(output.shape) 
    total_params = sum(p.numel() for p in model.parameters())

    print(f'모델의 총 파라미터 개수: {total_params}')
        