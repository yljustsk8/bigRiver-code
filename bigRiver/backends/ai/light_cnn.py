import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import numpy as np
import os

class mfm(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, type=1):
        super(mfm, self).__init__()
        self.out_channels = out_channels
        if type == 1:
            self.filter = nn.Conv2d(in_channels, 2*out_channels, kernel_size=kernel_size, stride=stride, padding=padding)
        else:
            self.filter = nn.Linear(in_channels, 2*out_channels)

    def forward(self, x):
        x = self.filter(x)
        out = torch.split(x, self.out_channels, 1)
        return torch.max(out[0], out[1])

class group(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(group, self).__init__()
        self.conv_a = mfm(in_channels, in_channels, 1, 1, 0)
        self.conv   = mfm(in_channels, out_channels, kernel_size, stride, padding)

    def forward(self, x):
        x = self.conv_a(x)
        x = self.conv(x)
        return x

class resblock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(resblock, self).__init__()
        self.conv1 = mfm(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.conv2 = mfm(in_channels, out_channels, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        res = x
        out = self.conv1(x)
        out = self.conv2(out)
        out = out + res
        return out


class network_29layers(nn.Module):
    def __init__(self, block, layers, num_classes=79077):
        super(network_29layers, self).__init__()
        self.conv1 = mfm(1, 48, 5, 1, 2)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.block1 = self._make_layer(block, layers[0], 48, 48)
        self.group1 = group(48, 96, 3, 1, 1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.block2 = self._make_layer(block, layers[1], 96, 96)
        self.group2 = group(96, 192, 3, 1, 1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.block3 = self._make_layer(block, layers[2], 192, 192)
        self.group3 = group(192, 128, 3, 1, 1)
        self.block4 = self._make_layer(block, layers[3], 128, 128)
        self.group4 = group(128, 128, 3, 1, 1)
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.fc = mfm(8 * 8 * 128, 256, type=0)
        self.fc2 = nn.Linear(256, num_classes)

    def _make_layer(self, block, num_blocks, in_channels, out_channels):
        layers = []
        for i in range(0, num_blocks):
            layers.append(block(in_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool1(x)

        x = self.block1(x)
        x = self.group1(x)
        x = self.pool2(x)

        x = self.block2(x)
        x = self.group2(x)
        x = self.pool3(x)

        x = self.block3(x)
        x = self.group3(x)
        x = self.block4(x)
        x = self.group4(x)
        x = self.pool4(x)

        x = x.view(x.size(0), -1)
        fc = self.fc(x)
        fc = F.dropout(fc, training=self.training)
        out = self.fc2(fc)
        return out, fc


def LightCNN_29Layers(**kwargs):
    model = network_29layers(resblock, [1, 2, 3, 4], **kwargs)
    return model

def adjust_learning_rate(optimizer, epoch):
    scale = 0.457305051927326
    step  = 10
    if (epoch != 0) & (epoch % step == 0):
        for param_group in optimizer.param_groups:
            param_group['lr'] = param_group['lr'] * scale

def train_model(input_x,input_y,save_path,test_x=None,test_y=None):
    batch_size = 10
    momemtum = 0.9
    weight_decay = 1e-4
    learning_rate = 0.00001
    epoch=0
    batch_num = len(input_x) // batch_size

    model = LightCNN_29Layers(num_classes=11)
    if torch.cuda.is_available():
        model = nn.DataParallel(model).cuda()
    model.train()
    if os.path.exists(save_path):
        checkpoint=torch.load(save_path)
        model.load_state_dict(checkpoint['state_dict'])
        epoch=checkpoint['epoch']

    torch.save({'epoch':epoch,
                'state_dict':model.state_dict()},save_path)
    if not test_x is None and not test_y is None:
        acc = validate(model, test_x, test_y)
        print("accuracy", acc)

    params=[]
    for name, value in model.named_parameters():
        if 'bias' in name:
            if 'fc2' in name:
                params += [{'params':value, 'lr': 20 * learning_rate, 'weight_decay': 0}]
            else:
                params += [{'params':value, 'lr': 2 * learning_rate, 'weight_decay': 0}]
        else:
            if 'fc2' in name:
                params += [{'params':value, 'lr': 10 * learning_rate}]
            else:
                params += [{'params':value, 'lr': 1 *learning_rate}]

    optimizer = torch.optim.SGD(params, learning_rate,
                                momentum=momemtum,
                                weight_decay=weight_decay)
    cudnn.benchmark = True

    criterion = nn.CrossEntropyLoss()
    if torch.cuda.is_available():
        criterion.cuda()

    for i in range(3):
        for j in range(10):
            r=np.random.permutation(len(input_x))
            train_x=input_x[r]
            train_y=input_y[r]
            for batch in range(batch_num):
                batch_x = train_x[batch * batch_size:(batch + 1) * batch_size]
                batch_y = train_y[batch * batch_size:(batch + 1) * batch_size]
                batch_x=torch.from_numpy(batch_x)
                batch_y=torch.from_numpy(batch_y)
                if torch.cuda.is_available():
                    batch_x=batch_x.cuda()
                if torch.cuda.is_available():
                    batch_y=batch_y.cuda()
                batch_x_var=torch.autograd.Variable(batch_x)
                batch_y_var=torch.autograd.Variable(batch_y)

                output,_=model(batch_x_var)
                loss=criterion(output,batch_y_var)
                # acc=accuracy(output,batch_y_var)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                print(j*batch_size+batch,loss.data[0])
            adjust_learning_rate(optimizer, i*10+j+1+epoch)
            if not test_x is None and not test_y is None:
                acc = validate(model, test_x, test_y)
                print("accuracy", acc)
            print("save model to ",save_path)
            torch.save({'epoch':i*10+j+1+epoch,
                'state_dict':model.state_dict()},save_path)

def validate(model,test_x,test_y):
    model.eval()
    x=torch.autograd.Variable(torch.from_numpy(test_x),volatile=True)
    target=torch.autograd.Variable(torch.from_numpy(test_y),volatile=True)
    output,_=model(x)
    return accuracy(output,target)

def accuracy(output, target):
    """Computes the precision@k for the specified values of k"""
    F.softmax(output,1)
    pred=np.array(output.data)
    label=np.array(target.data)
    pred=np.argmax(pred,axis=1)
    print("predict",pred)
    print("label",label)
    equal=np.equal(label,pred)
    equal.astype(np.float32)
    acc=np.mean(equal)
    return acc

def loadModel(model_path):
    model=LightCNN_29Layers()
    if torch.cuda.is_available():
        model = nn.DataParallel(model).cuda()
    model.eval()
    if os.path.exists(model_path):
        ckpt=torch.load(model_path)
        model.load_state_dict(ckpt['state_dict'])
        return model
    else:
        return None

def CosSim(model,identify_img,person_img):
    model.eval()

    if identify_img.shape != (1, 1,128, 128):
        print("identify_img shape error")
        return None
    person_shape = person_img.shape
    if person_shape[1] != 1 or person_shape[2] != 128 or person_shape[3] != 128:
        print("person_img shape error")
        return None

    img1 = torch.autograd.Variable(torch.from_numpy(identify_img), volatile=True)
    img2 = torch.autograd.Variable(torch.from_numpy(person_img), volatile=True)

    _,identify_feature=model(img1)
    _,person_feature=model(img2)
    similarity=F.cosine_similarity(identify_feature,person_feature,1)
    return np.array(similarity.data)