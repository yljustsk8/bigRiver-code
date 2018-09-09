from basic_info.models import personal_info

# personal_info_management 内部函数，供接口进行调用
def modify_info(userID, type, info):
    #userID不改变，request中放置状态码、用户名和更改后的内容。
    #1：password 2：name 3：email 4：company 5：departmentName 6：modelLocation
    select_result = personal_info.objects.filter(userID=userID)
    if select_result:
        the_model=select_result[0]
        if(type==1):
            the_model.password=info
        elif(type==2):
            the_model.name=info
        elif(type==3):
            the_model.email=info
        elif(type==4):
            the_model.company=info
        elif(type==5):
            the_model.departName=info
        elif(type==6):
            the_model.modelLocation=info
        the_model.save()
        return True
    else:
        print("id doesn't exist. In personal_info_management.inside_func.modify_info()")
        return False
