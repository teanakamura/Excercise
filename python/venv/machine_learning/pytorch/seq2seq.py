import torch
from torchvision import transforms, datasets
import numpy as np

def load_data():
    en_classes = np.load('./data/en_classes.npy')
    ja_classes = np.load('./data/ja_classes.npy')
    en_

transform = transforms.Compose(
    [transforms.ToTensor(),
        transforms.Normalize((0.5, ), (0.5, ))
    ]
)
trainset = datasets.MNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)
trainloader = torch.utils.data.DataLoader(
    trainset,
    batch_size=100,  # minibatchのbatch size
    shuffle=True,
    num_workers=2
)
testset = datasets.MNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform
)
testloader = torch.utils.data.DataLoader(
    testset,
    batch_size=100,
    shuffle=False,
    num_workers=2
)



from torch import nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3) # 28x28x1 -(3x3x32)-> 26x26x32  # 2D convolution
        self.conv2 = nn.Conv2d(32, 64, 3) # 26x26x32 -(3x3x2)-> 24x24x64  # 2D convolution
        self.pool = nn.MaxPool2d(2, 2) # 24x24x64 -> 12x12x64
        self.fc1 = nn.Linear(12 * 12 * 64, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout05 = nn.Dropout2d() # default: p = 0.5
        self.dropout02 = nn.Dropout2d(p=0.2)

    def forward(self, x):
        self.dropout02(x) # 入力層はdropout ratio: 0.2
        x = nn.functional.relu(self.conv1(x))
        self.dropout02(x) # 全結合層以外はdropout ratio: 0.2
        x = nn.functional.relu(self.conv2(x))
        self.dropout05(x)
        x = self.pool(x)
        x = x.view(-1, 12 * 12 * 64)
        self.dropout05(x)
        x = nn.functional.relu(self.fc1(x))
        self.dropout05(x)
        x = self.fc2(x)
        return x



from torch import optim

if __name__ == '__main__':
    epochs = int(input())

    net = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        net.parameters(),
        lr=0.01,  # 学習係数
        momentum=0.8,  # 慣性係数
        nesterov=True
    )

    print('Start Training')

    net.train() # train modeに設定
    for epoch in range(1, epochs+1):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(trainloader, 1):
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs) # forwardメソッドが実行され、Tensorオブジェクトとして出力される。
            loss = criterion(outputs, labels) # outputsとlabelsからloss funcを計算してTensorオブジェクトとして返される。
            loss.backward()　#  loss.item()から各parameterの勾配を計算して、parameter.gradに記憶する。
                                         # lossはTensorオブジェクトでgrad_fnアトリビュートから全parameterを追跡できる。
                                         # このgrad_fnの値はoutputsに記憶されていたものでoutputsから渡される。
            optimizer.step() # parameter.gradを利用してparameterを更新

            # print statistics
            running_loss += loss.item()
            if i % 100 == 0:
                print(f'[{epoch: d}, {i: 5d}] loss: {running_loss/100: .3f}')
                running_loss = 0.0

    print('Finished Training')


    correct = 0
    total = 0

    net.eval() # eval modeに設定。dropoutがdeactivateされる
    with torch.no_grad():
        for (images, labels) in testloader:
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print('Accuracy: {:.2f} %'.format(100 * float(correct/total)))
