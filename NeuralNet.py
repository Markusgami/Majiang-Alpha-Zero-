import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion*planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10):
        super(ResNet, self).__init__()
        self.in_planes = 32

        self.conv1 = nn.Conv2d(1, self.in_planes, kernel_size=(7,3), stride=1, padding=(0, 1), bias=False)
        self.bn1 = nn.BatchNorm2d(self.in_planes)
        self.layer1 = self._make_layer(block, 32, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 64, num_blocks[1], stride=(2,1))
        self.layer3 = self._make_layer(block, 128, num_blocks[2], stride=(2,1))
        self.layer4 = self._make_layer(block, 256, num_blocks[3], stride=(2,1))        
        self.fc1 = nn.Linear(256*27, 256)
        self.fc2 = nn.Linear(256, 1)
        
        self.policy_head = nn.Conv2d(256, 1, kernel_size=1, stride=1, padding=0, bias=False)
        #self.card_predict_head = nn.Conv2d(256, 3, kernel_size=1, stride=1, padding=0, bias=False)
        
    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)

        policy = self.policy_head(out)
        policy = policy.view(policy.size(0), -1)
        #hide_cards = self.card_predict_head(out)
        value = out.view(out.size(0), -1)
        value = self.fc1(value)
        value = self.fc2(value)
        
        return F.softmax(policy), F.tanh(value)
    
    def predict(self, canonicalBoard):
        newcanonicalBoard = trans(canonicalBoard)
        y = np.expand_dims(newcanonicalBoard, axis=0)
        y = np.expand_dims(y, axis=0)

        # timing
        #start = time.time()

        # preparing input
        
        board = torch.FloatTensor(y.astype(np.float64))
        
        board = Variable(board, volatile=True)

        self.eval()
        pi, v = self.forward(board)
        

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

def ResNet18():
    return ResNet(BasicBlock, [2,2,2,2])

def ResNet34():
    return ResNet(BasicBlock, [3,4,6,3])

def ResNet50():
    return ResNet(Bottleneck, [3,4,6,3])

def ResNet101():
    return ResNet(Bottleneck, [3,4,23,3])

def ResNet152():
    return ResNet(Bottleneck, [3,8,36,3])

def test():
    net = ResNet18()
    y = net(Variable(torch.randn(1,1,14,27)))
    print(y.size())
    
def trans(CanonicalForm):
    new_canonicalBoard = np.zeros((14,27))
    new_canonicalBoard[2:11] = CanonicalForm
    new_canonicalBoard[0:2] = CanonicalForm[-2:]
    new_canonicalBoard[-3:] = CanonicalForm[:3]
    return new_canonicalBoard