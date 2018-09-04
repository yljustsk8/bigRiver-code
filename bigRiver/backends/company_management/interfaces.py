from basic_info.models import company_info
from backends.personal_info_management import interfaces as pim

def get_delete_result(original_str, delete_str):
    #split by '@'
    list = str(original_str).split('@')
    new_str = ''
    for s in list:
        if (s != delete_str):
            if (new_str):
                # 不为空
                new_str += ('@' + s)
            else:
                new_str += s
        else:
            pass
    return new_str

def set_admin(cID, aID):
    companyID = cID
    adminID = aID
    company_model = company_info.objects.filter(companyID=companyID)[0]
    original_admins = str(company_model.adminID)
    if(original_admins):
        #不为空
        new_admins = original_admins + '@' + adminID
    else:
        new_admins = adminID
    company_model.adminID = new_admins
    company_model.save()

def delete_admin(cID, aID):
    companyID = cID
    adminID = aID
    company_model = company_info.objects.filter(companyID=companyID)[0]
    original_admins = str(company_model.adminID)
    new_admins = get_delete_result(original_str=original_admins, delete_str=adminID)
    company_model.adminID = new_admins
    company_model.save()
    return True

def create_department(cID, d_name):
    companyID = cID
    department = d_name
    company_model = company_info.objects.filter(companyID=companyID)[0]
    original_departments = str(company_model.departNames)
    if (original_departments):
        # 不为空
        new_departments = original_departments + '@' + department
    else:
        new_departments = department
    company_model.departNames = new_departments
    company_model.save()

def delete_department(cID, d_name):
    companyID = cID
    department = d_name
    company_model = company_info.objects.filter(companyID=companyID)[0]
    original_departments = str(company_model.departNames)
    new_departments = get_delete_result(original_str=original_departments, delete_str=d_name)
    company_model.adminID = new_departments
    company_model.save()
    return True

def distribution(cID, sID, d_name):
    stuffID = sID
    department = d_name
    if(pim.join_department(stuffID=stuffID, department=department)):
        return True
    else:
        return False