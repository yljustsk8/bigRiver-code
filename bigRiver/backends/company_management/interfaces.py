from basic_info.models import *
from backends.personal_info_management import interfaces as pim
from backends.company_management import inside_func as inf

# 接口1：设置管理员 输入：公司ID，被设置的管理员ID 无返回值
def set_admin(companyID, adminID):
    if(company_info.objects.filter(companyID=companyID)):
        # 获取公司模型
        company_model = company_info.objects.filter(companyID=companyID)[0]
        # 获取原管理员str
        original_admins = str(company_model.adminID)
        if(original_admins):
            # 原str不为空，直接增加'@newID'
            new_admins = original_admins + '@' + adminID
        else:
            # 原str为空，str即为新admin
            new_admins = adminID
        company_model.adminID = new_admins
        company_model.save()
        # 修改新管理员个人信息，设置其为管理员
        pim.set_title(userID=adminID, title=2)
        return
    else:
        # 异常处理：公司未找到
        print('invalid companyID. In backends.company_management.set_admin().')
        return

# 接口2：删除管理员 输入：公司ID，被删除的管理员ID 无返回值
def delete_admin(companyID, adminID):
    if(company_info.objects.filter(companyID=companyID)):
        # 获取公司模型
        company_model = company_info.objects.filter(companyID=companyID)[0]
        # 获取原管理员str
        original_admins = str(company_model.adminID)
        # 调用get_delete_result函数，对原管理员进行删除
        new_admins = inf.get_delete_result(original_str=original_admins, delete_str=adminID)
        company_model.adminID = new_admins
        company_model.save()
        # 修改被删除的管理员个人信息，设置其为普通员工
        pim.set_title(userID=adminID, title=1)
    else:
        # 异常处理：公司未找到
        print('invalid companyID. In backends.company_management.delete_admin().')
        return

# 接口3：创建部门 输入：公司ID，部门名 无返回值
def create_department(companyID, department):
    if (company_info.objects.filter(companyID=companyID)):
        # 获取公司模型
        company_model = company_info.objects.filter(companyID=companyID)[0]
        # 获取原部门str
        original_departments = str(company_model.departNames)
        if (original_departments):
            # 原str不为空，直接增加'@new_department'
            new_departments = original_departments + '@' + department
        else:
            # 原str为空，str即为新department
            new_departments = department
        company_model.departNames = new_departments
        company_model.save()
    else:
        # 异常处理：公司未找到
        print('invalid companyID. In backends.company_management.create_department().')
        return

# 接口4：删除部门 输入：公司ID，被删除的部门名 无返回值
def delete_department(companyID, department):
    if (company_info.objects.filter(companyID=companyID)):
        # 获取公司模型
        company_model = company_info.objects.filter(companyID=companyID)[0]
        # 获取原部门str
        original_departments = str(company_model.departNames)
        # 调用get_delete_result函数，对原部门进行删除
        new_departments = inf.get_delete_result(original_str=original_departments, delete_str=department)
        company_model.adminID = new_departments
        company_model.save()
        # 获取原部门员工模型集
        stuff_model_set = personal_info.objects.filter(departName=department)
        if(stuff_model_set):
            # 将原部门员工的department设置为空
            for s_model in stuff_model_set:
                s_model.departName = ''
                s_model.save()
    else:
        # 异常处理：公司未找到
        print('invalid companyID. In backends.company_management.delete_department().')
        return

# 接口5：更改员工部门 输入：员工ID，变更后的部门名称 无返回值
def distribution(stuffID, department):
    if(personal_info.objects.filter(userID=stuffID)):
        # 该员工存在
        s_model = personal_info.objects.get(userID=stuffID)[0]
        s_model.departName = department
        s_model.save()
    else:
        # 异常处理：员工未找到
        print('invalid stuffID. In backends.company_management.distribution().')
        return
