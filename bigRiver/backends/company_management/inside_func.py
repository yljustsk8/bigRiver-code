from basic_info.models import company_info
from backends.personal_info_management import interfaces as pim


# company_management内部函数，供其接口进行调用
# 对一个以'@'为条目分隔符的字符串中的特定条目进行删除
def get_delete_result(original_str, delete_str):
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

