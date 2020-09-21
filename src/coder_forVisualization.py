import os
import argparse
import numpy as np
from net import AlexNetPlusLatent
import torch
from torchvision import datasets, transforms
from torch.autograd import Variable
import torch.optim.lr_scheduler
from PIL import Image
import matplotlib.pyplot as plt


def load_data():
    transform = transforms.Compose(
         [transforms.Resize(227), transforms.ToTensor(),
         transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))])
    dataset = datasets.CIFAR10(root='../data', train=True, download=True,
                               transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=100,
                                         shuffle=False, num_workers=2)
    return loader


def binary_output(dataloader, args):
    net = AlexNetPlusLatent(args.bits)
    net.load_state_dict(torch.load('./model/90.42'))
    full_batch_output = torch.FloatTensor()
    net.eval()
    imgrecord = []
    if not os.path.isdir('images'):
        os.mkdir('images')
        print("Generating...")
    for batch_idx, (inputs, targets) in enumerate(dataloader):
        for i in range(0, 100):
            img_np = inputs[i].numpy().transpose([1, 2, 0])
            img_np = (img_np - np.min(img_np)) / (np.max(img_np) - np.min(img_np)) * 255.0  # 转为0-255
            img = Image.fromarray(img_np.astype('uint8')).convert('RGB')
            img = img.resize((32, 32), Image.ANTIALIAS)
            path = str(100*batch_idx+(i+1))
            img.save(path)
            imgrecord.append(path)
        with torch.no_grad():
            inputs, targets = Variable(inputs), Variable(targets)
        outputs, _ = net(inputs)
        full_batch_output = torch.cat((full_batch_output, outputs.data), 0)
    return imgrecord, torch.round(full_batch_output)


def hammingDis(B, b, num):
    # hammingDists
    hamming = []
    for bitemp in B:
        smstr = np.nonzero(b - bitemp)
        sm = np.shape(smstr[0])[0]
        hamming.append(sm)
    # minNum
    minNum = []
    for i in range(num):
        minind = hamming.index(min(hamming))
        minNum.append(minind)
        hamming[minind] = max(hamming)
    return minNum


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deep Hashing evaluate mAP')
    parser.add_argument('--pretrained', type=int, default=0, metavar='pretrained_model',
                        help='loading pretrained model(default = None)')
    parser.add_argument('--bits', type=int, default=48, metavar='bts',
                        help='binary bits')
    args = parser.parse_args()
    args.pretrained = 90.42

    if os.path.exists("./code/bits.npy") and os.path.exists("./code/imgrecord.txt"):
        bits = np.load("./code/bits.npy")
        imgrecord = []
        with open('./code/imgrecord.txt', 'r') as f:
            for line in f:
                imgrecord.append(list(line.strip('\n').split(',')))
    else:
        loader = load_data()
        imgrecord, binary = binary_output(loader,args)
        if not os.path.isdir('code'):
            os.mkdir('code')
        m = binary.numpy()
        np.save('./code/bits.npy', binary.numpy())
        with open('./code/imgrecord.txt', 'w') as f:
            f.write('\n'.join(imgrecord))

    testindex = np.random.randint(0, high=len(args.bits))
    bitest = bits[testindex]
    minHamming = hammingDis(bits, bitest, 10)

    plt.figure()
    imgtest = Image.open(imgrecord[testindex][0])
    plt.subplot(3, 5, 3)
    plt.imshow(imgtest)
    plt.xticks([])
    plt.yticks([])
    count = 5
    for ind in minHamming:
        count += 1
        img = Image.open(imgrecord[ind][0])
        plt.subplot(3, 5, count)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
    plt.show()