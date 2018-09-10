import tensorflow as tf
import numpy as np
import cv2
from backends.ai import CNN_Net
import os
import re
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from basic_info.models import personal_info
def train(model):
    #调用模型函数
    model_path="./models/model_%d"%model

    train_x=[]
    train_y=[]
    classnum=0
    for name in os.listdir(model_path):

        pattern=re.compile("person_([\\curr_month_obj])")
        ret=re.findall(pattern,name)
        person_path=os.path.join(model_path,name)
        print(ret)
        if ret==None:
            continue
        else:
            classnum+=1
            for img in os.listdir(person_path):
                if img.endswith(".jpg"):
                    img=cv2.imread(os.path.join(person_path,img))

                    train_x.append(img)
                    train_y.append(int(ret[0]))
    train_y=one_hot(train_y,classnum)

    #转化为numpy矩阵
    train_x=np.array(train_x)
    train_y=np.array(train_y)

    #重新训练该模型
    model_save_path=os.path.join(model_path,"model/model.ckpt")
    CNN_Net.train(train_x,train_y,model_save_path)
    # 返回训练结果
    return True

def identify(matrix):
    if matrix.shape[1] == matrix.shape[2]== 64:

        #循环获取所有模型
        model_list=os.listdir("./models")
        model=-1
        person=-1
        max_possi=0.1

        #计算每个模型下的预测可能，取最大可能结果
        for _model in model_list:
            model_path=os.path.join("./models",_model)
            classnum=len(os.listdir(model_path))-1
            model_save_path=os.path.join(model_path,"model/model.ckpt")
            print("matrix:",matrix.shape)

            index,possibility=CNN_Net.predict(matrix,classnum,model_save_path)
            index,possibility=index[0],possibility[0]
            if possibility > max_possi:
                model=model_path.split('_')[1]
                person=index
                max_possi = possibility
        # 返回识别结果
        if model==-1 or person==-1:
            return None
        model_location="{0}_{1}".format(model,person)
        print("model_location:",model_location)
        user=personal_info.objects.get(modelLocation=model_location)
        return user.userID
    else:
        return None

def face_enter(userID,imgs):
    # 调用face_identify.imgs2faces(imgs)把图片变为矩阵
    matrices=imgs2faces(imgs)

    #获取数据库中userID对应的模型
    entire_model=personal_info.objects.all()
    count=len(entire_model)-1
    #将matrices存到相应的模型源文件下
    file_name="./models/model_{0}/person_{1}".format(count//10,count%10)
    if os.path.exists(file_name) == False:
        os.makedirs(file_name)
    save_faces(file_name,matrices)

    model,person=count//10,count%10

    #将模型位置存入数据库
    model_location="{0}_{1}".format(model,person)
    user=personal_info.objects.get(userID=userID)
    user.modelLocation=model_location
    user.save()

    #训练模型
    success=train(model)

    # 根据返回的标识符，写入数据库
    if model < 0 or person <0 or person>9:
        return False
    else:
        return success

def face_identify(img):
    # 将img变成增加一个维度，符合输入要求
    img_list=[]
    img_list.append(img)
    img_list=np.array(img_list)
    # 调用face_identify.img2face(img)
    matrix=imgs2faces(img_list)
    # 调用face_identify.identify(matrix)
    userID=identify(matrix)
    return userID

def one_hot(train_y,classnum):
    labels=np.zeros([len(train_y),classnum])
    for i in range(len(train_y)):
        if train_y[i] >= classnum or train_y[i]<0:
            continue
        labels[i,train_y[i]]=1

    return labels

####Constants####

IMGSIZE = 64

#################

def img2face(img):
    haar = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    gray_sample = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pin = haar.detectMultiScale(gray_sample, 1.3, 5)
    face = pin
    for f_x, f_y, f_w, f_h in pin:
        # print(f_x, f_y, f_w, f_h)
        face = img[f_y:f_y + f_h, f_x:f_x + f_w]
        face = cv2.resize(face, (IMGSIZE, IMGSIZE))

    return face

def imgs2faces(imgs):
    haar = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    faces = []
    for img in imgs:
        gray_sample = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pin = haar.detectMultiScale(gray_sample, 1.3, 5)
        for f_x, f_y, f_w, f_h in pin:
            face= img[f_y:f_y + f_h, f_x:f_x + f_w]
            face = cv2.resize(face, (IMGSIZE, IMGSIZE))
            faces.append(face)

            # faces[n] = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))

    return np.array(faces)

def save_faces(save_path, faces):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    n=0
    for face in faces:
        face = np.array(face, dtype=np.int64)
        cv2.imwrite(os.path.join(save_path, str(n) + '.jpg'), face)
        n+=1

def save_face(save_path, face):
    face=np.array(face,dtype=np.int64)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    cv2.imwrite(os.path.join(save_path, 'test.jpg'), face)

def make_shade(img, alpha=1, bias=0):
    img = img.astype(float)
    img = img * alpha + bias
    img[img < 0] = 0
    img[img > 255] = 255
    img = img.astype(np.uint8)
    return img

def test_face_enter():
    imgs = []
    dir = "C:\\Users\\87216\\Documents\\bigRiverSystem\\python\\FaceProject\\image\\Zhang"
    for file in os.listdir(dir):
        if file.endswith(".jpg"):
            jpg = os.path.join(dir, file)
            # print("img path:",jpg)
            imgs.append(cv2.imread(jpg))
    # new_user = personal_info(userID="1000002", password="1000002")
    # new_user.save()
    face_enter("1000002", imgs)

def test_face_identify():
    img_path = "C:\\Users\\87216\\Documents\\bigRiverSystem\\python\\FaceProject\\image\\Zhang\\19.jpg"
    img=cv2.imread(img_path)

    print("img shape:",img.shape)
    userID=face_identify(img)
    print("user ID:",userID)

if __name__=="__main__":
   # test_face_enter()
   # test_face_identify()
   pass