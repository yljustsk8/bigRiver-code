import tensorflow as tf
import numpy as np
import cv2
from backends.ai import light_cnn
import os
import re
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from basic_info.models import personal_info

def identify(matrix):
    model=light_cnn.loadModel("./bigRiver/backends/ai/model/LightCNN_29Layers_checkpoint.pth.tar")
    if model is None:
        print("加载模型失败")
        return None
    if matrix.shape!=(1,1,128,128) or matrix is None:
        print("matrix格式不合法")
        return None
    max_possi=0.9
    user_id=None

    people_path="./bigRiver/backends/ai/people"
    people=os.listdir(people_path)
    possi=[]
    for user in people:
        imgs = []
        user_path=os.path.join(people_path,user)
        img_num = len(os.listdir(user_path))
        r=np.random.permutation(range(img_num))
        select=r[0:20]
        for i in range(20):
            img_path = os.path.join(user_path, "{}.jpg".format(select[i]))
            img=cv2.cvtColor(cv2.imread(img_path),cv2.COLOR_BGR2GRAY)
            imgs.append(img)

        imgs=np.array(imgs,dtype=np.float32)
        imgs=imgs[:,:,:,np.newaxis]
        imgs=np.transpose(imgs,[0,3,1,2])
        matrix=matrix.astype(np.float32)
        Cos=light_cnn.CosSim(model,matrix,imgs)
        if Cos is None:
            return None
        possi.append(np.mean(Cos))
    np_possi=np.array(possi)
    current_max=np.max(np_possi)
    print(current_max)
    if current_max >max_possi:
        person_index=np.argmax(np_possi)
        user_id=people[int(person_index)]
    return user_id

def face_enter(userID,imgs):
    # 调用face_identify.imgs2faces(imgs)把图片变为矩阵
    matrices=imgs2faces(imgs)
    if matrices is None:
        return False

    #获取数据库中userID对应的模型
    entire_model=personal_info.objects.exclude(modelLocation="")
    count = len(entire_model)
    user=personal_info.objects.get(userID=userID)
    if user.modelLocation!='':
        count-=1

    #将matrices存到相应的模型源文件下
    file_name="./bigRiver/backends/ai/people/{}".format(userID)
    if os.path.exists(file_name) == False:
        os.makedirs(file_name)
    success=save_faces(file_name,matrices)
    return success

def face_identify(img):
    if img is None:
        return None
    # 将img变成增加一个维度，符合输入要求
    img_list=[]
    img_list.append(img)
    img_list=np.array(img_list)
    print("identify img shape",img_list.shape)
    # 调用face_identify.img2face(img)
    matrix=imgs2faces(img_list)
    if matrix is None or matrix.shape!=(1,128,128):
        return None
    matrix=matrix[:,:,:,np.newaxis]
    matrix=np.transpose(matrix,[0,3,1,2])
    # 调用face_identify.identify(matrix)
    userID=identify(matrix)
    return userID

####Constants####

IMGSIZE = 128

#################

def img2face(img):
    if img is None:
        return None
    cv2_path = os.path.dirname(cv2.__file__)
    haar_path = os.path.join(cv2_path, "data/haarcascade_frontalface_alt2.xml")
    haar = cv2.CascadeClassifier(haar_path)
    print("haar_path exists:",os.path.exists(haar_path))
    if haar is None:
        return None
    gray_sample = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pin = haar.detectMultiScale(gray_sample, 1.3, 5)
    face = None
    for f_x, f_y, f_w, f_h in pin:
        if f_w == 0 or f_h == 0:
            return None
        face = img[f_y:f_y + f_h, f_x:f_x + f_w]
        face = cv2.resize(face, (IMGSIZE, IMGSIZE))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    print("face is None:",face is None)
    return np.array(face)

def imgs2faces(imgs):
    if imgs is None:
        return None
    cv2_path=os.path.dirname(cv2.__file__)
    haar_path=os.path.join(cv2_path,"data/haarcascade_frontalface_alt2.xml")
    haar = cv2.CascadeClassifier(haar_path)
    if haar is None:
        return None
    faces = []
    for img in imgs:
        if img is None:
            return None
        gray_sample = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pin = haar.detectMultiScale(gray_sample, 1.3, 5)
        for f_x, f_y, f_w, f_h in pin:
            face= img[f_y:f_y + f_h, f_x:f_x + f_w]
            face = cv2.resize(face, (IMGSIZE, IMGSIZE))
            face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
            faces.append(face)

    if len(faces)==0:
        return None
    return np.array(faces)

def save_faces(save_path, faces):
    if faces is None:
        return False
    if faces.shape[1]!=128 or faces.shape[2]!=128:
        return False
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    n=0
    for face in faces:
        face = np.array(face, dtype=np.int64)
        cv2.imwrite(os.path.join(save_path, str(n) + '.jpg'), face)
        n+=1
    return True

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

def is_useful(img_url):
    img=cv2.imread(img_url)
    if img is None:
        return False
    face=img2face(img)
    if face is None or face.shape!=(128,128):
        return False
    return True

def face_enter_url(userID,imgs_url):
    if not os.path.exists(imgs_url):
        return False
    imgs=[]
    for i in os.listdir(imgs_url):
        if i.endswith(".jpg"):
            img=cv2.imread(os.path.join(imgs_url,i))
            imgs.append(img)
    return face_enter(userID,np.array(imgs))


def test_face_enter():
    imgs = []
    dir = "C:/Users/87216/Documents/bigRiverSystem/python/FaceProject1/image/test_image"
    for file in os.listdir(dir):
        if file.endswith(".jpg"):
            jpg = os.path.join(dir, file)
            # print("img path:",jpg)
            imgs.append(cv2.imread(jpg))
    # new_user = personal_info(userID="1000002", password="1000002")
    # new_user.save()
    face_enter("100004", imgs)

def test_face_identify():
    img_path = "C:/Users/87216/Documents/bigRiverSystem/python/FaceProject1/image/test_image/53.jpg"
    img=cv2.imread(img_path)
    userID=face_identify(img)
    print("user ID:",userID)

if __name__=="__main__":
    # test_face_enter()
    # test_face_identify()
    # user3=personal_info(userID="100003",password="100003")
    # user4 = personal_info(userID="100004", password="100004")
    # user3.save()
    # user4.save()
    #  img=cv2.imread("C:/Users/87216/Documents/bigRiverSystem/bigRiver-code/bigRiver/static/temp/100003/1.jpg")
    pass