import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

#个人信息管理模块

from basic_info.models import *
from backends.personal_info_management import inside_func as inf

# 接口1：登录 输入：用户名，密码
# 返回内容包括：登录操作信息状态码，登录操作信息内容，用户名，职位
def login(userID, password):
    #在数据库中找出userID匹配项
    select_result = personal_info.objects.filter(userID=userID)
    #获取登录状态
    userID_rt = ''
    content_rt = ''
    title_rt = ''
    if not select_result:
        # id不存在
        content_rt = "id doesn't exist!"
        status = False
    elif(select_result[0].password != password):
        # 密码错误
        content_rt = "wrong password!"
        status = False
    else:
        # 登录成功
        status = True
        content_rt = 'success!'
        userID_rt = userID
        title_rt = select_result[0].title
    #构造返回的字典
    result_dict = {
        'status': status,
        'content': content_rt,
        'userID': userID_rt,
        'title': title_rt,
    }
    return result_dict

# 接口2：注册 输入：用户名，密码，姓名，邮箱
# 返回内容包括：注册操作信息状态码，注册操作信息内容，用户名
def register(userID, password, name, email):
    # 在数据库中寻找ID是否重复
    select_result = personal_info.objects.filter(userID=userID)
    userID_rt = ''
    content_rt = ''
    if select_result:
        #id已存在
        status = False
        content_rt = 'ID existed!'
    else:
        #注册成功
        the_model = personal_info(userID=userID, password=password, name=name, email=email, title=0)
        the_model.save()
        status = True
        content_rt = "register success!"

    result_dict = {
        'status': status,
        'content': content_rt,
        'userID': userID_rt,
    }
    return result_dict

# 接口3：修改 输入：用户名，(int)信息更改条目类型，更改后内容
# 返回内容包括：修改操作信息状态码，修改操作信息内容
def modify(userID, type, info):
    #userID不改变，request中放置状态码、用户名和更改后的内容。
    #type：1：password 2：name 3：email
    content_rt = ''
    if inf.modify_info(userID, type, info):
        status = True
        content_rt = "change success"
    else:
        status = False
        content_rt= "id doesn't exist"
    result_dict = {
        'status': status,
        'content': content_rt,
    }

    # test_string = str(type)
    # print('turn info '+test_string+' to '+ info)

    return result_dict

# 接口4：创建公司 输入：用户名、创建公司名、税号
# 返回内容包括：创建操作信息状态码，创建操作信息内容
def create_company(userID, company_name, taxNumber):
    content_rt = ''
    # 更新user的title条目
    if(personal_info.objects.filter(userID=userID)):
        # 更改用户身份
        user = personal_info.objects.filter(userID=userID)[0]
        user.title = 3
        user.save()
        # 当前companyID自增，获取新的companyID
        entire_model = company_info.objects.all()
        l = len(entire_model)
        new_company_id = int(entire_model[l - 1].companyID) + 1
        new_model = company_info(companyID=new_company_id, bossID=userID, name=company_name, taxNumber=taxNumber)
        new_model.save()
        #按照逻辑，税号和公司名需要进行判断，此处暂未进行编写
        status = True
        content_rt = '创建成功'
    else:
        # 异常处理：创建者未找到
        status = True
        content_rt = '用户无效，创建失败'
        print('invalid userID. In backends.company_management.create_company().')
    result_dict = {
        'status': status,
        'content': content_rt,
    }
    return result_dict

# 接口5：根据userID获取companyID 输入用户名 输出公司ID
def get_company_ID(userID):
    companyID = ''
    if(personal_info.objects.filter(userID=userID)):
        companyID = personal_info.objects.filter(userID=userID)[0].company
    else:
        print('invalid userID. In backends.company_management.get_company_ID().')
    return companyID

# 接口6：（内部接口）加入公司 输入员工用户名和公司ID
# 返回布尔值
def join_company(stuffID, companyID):
    if(personal_info.objects.filter(userID=stuffID)):
        the_model = personal_info.objects.filter(userID=stuffID)[0]
        if(company_info.objects.filter(companyID=companyID)):
            company = company_info.objects.filter(companyID=companyID)
            the_model.company = companyID
            the_model.title = 1
            the_model.save()
            status = True
        else:
            status = False
            print('invalid companyID. In backends.company_management.join_company().')
    else:
        status = False
        print('invalid stuffID. In backends.company_management.join_company().')
    return status

# 接口7：（内部接口）根据ID获取信息
# 返回值依次为：name, companyID, departName, title, modellocation
def get_info_by_id(userID):
    try:
        print('userID: ' + userID)
        the_model = personal_info.objects.get(userID=userID)
    except BaseException:
        print('invalid userID. In backends.personal_info_management.get_info_by_id().')
        return False
    return the_model.name, the_model.company, the_model.departName, the_model.title, the_model.modelLocation

# 接口8：（内外皆用接口）设置用户权限
# 返回布尔值
def set_title(userID, title):
    try:
        the_model = personal_info.objects.get(userID=userID)
        the_model.title = title
        the_model.save()
    except BaseException:
        print('invalid userID. In backends.company_management.set_title().')
        return False
    return True