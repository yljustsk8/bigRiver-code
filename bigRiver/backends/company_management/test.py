str = "111ef@222fe@333re"
p = '222fe'
list = str.split('@')
print(list)
new_str = ''
for s in list:
    if(s != p):
        if(new_str):
            #不为空
            new_str += ('@' + s)
        else:
            new_str += s
    else:
        pass
print(new_str)