import pandas as pd
import torch
import glob
import numpy as np
from io import StringIO
PATH = ".archive/"

class ChallengeData(torch.utils.data.Dataset):
    def __init__(self, path, flag = 'train'):
        self.path_ = path
        self.flag = flag
        
        if self.flag == 'train':
            self.csv_path_ = np.array(glob.glob(self.path_+'/train/*.csv'))
            

        elif self.flag == 'test':
            self.csv_path_ = np.array(glob.glob(self.path_+'/eval/*.csv'))


    def __getitem__(self, idx):

        if "bearing" in self.csv_path_[idx]: 
            label = 1

        elif "normal" in self.csv_path_[idx]: 
            label = 0

        elif "rail" in self.csv_path_[idx]: 
            label = 2

        else:
            print('error')

        csv_data = np.transpose(pd.read_csv(self.csv_path_[idx], header=None).values)

        sounds = torch.tensor(csv_data)

        labels = torch.tensor(label)
        return sounds, labels
    
    def __len__(self, idx):
        return len(self.csv_path_[idx])
        