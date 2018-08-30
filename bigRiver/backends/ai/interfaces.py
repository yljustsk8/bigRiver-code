from . import  face_model

def face_enter(userID,imgs):
    '''输入人脸录入时候采集到的照片和userID，进行训练，照片为jpg格式，返回训练成功或失败'''
    return face_model.face_enter(userID,imgs)

def face_identify(img):
    '''输入人脸识别时拍的照片，返回识别得到的usrID，如果没有识别结果，返回None'''
    return face_model.face_identify(img)