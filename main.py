import pandas,multiprocessing
group={}
def group_def(name={},fast:bool=False):
    if fast==True:
        global group
    group={}
    class7 = ('语文', '数学', '英语', '物理', '地理', '生物', '个人总分')
    for i in range(0, 7):  # 表单读取循环
        p = pandas.read_excel('七班课堂量化.xlsx', sheet_name=i)
        for j in range(0, 6):  # 行读取循环
            L = p.iloc[j].values
            for k in range(1, 8):  # 列读取循环
                group[(name[j+i*6], class7[k - 1])] = L[k]  # 将分数复制给[姓名][科目]二重键值字典
                #print(data[(name[j+i*6], class7[k - 1])])
    del class7
    return group
def class_def(name={},fast:bool=False):
    if fast==True:
        global group
        group={}
    p = pandas.read_excel('七班课堂量化.xlsx', sheet_name=7)
    class7 = ('课堂有效', '课堂实际', '作业情况', '得分补充','小组总分')
    for i in range(0, 7):
        L = p.iloc[i].values
        for j in range(1, 6):
            group[(name[i], class7[j - 1])] = L[j]
    del class7
    return group
def fast_group():
    fast_group_start=multiprocessing.Process(target=group_def(),args=(people(),True)) # 实例化group进程对象
    fast_group_start.start() #开启group线程
    fast_group_start.join()
    return group
def fast_class():
    fast_class_start=multiprocessing.Process(target=class_def) #实例化class进程对象
    fast_class_start.start()#开启class线程
def people():
    name={}
    for i in range(0,7):
        p=pandas.read_excel('七班课堂量化.xlsx',sheet_name=i)
        for j in range(0,6):
            L=p.iloc[j].values
            name[j+i*6]=L[0]
            #print(name[j+i*6])
    return name
def fast_sort(reverse:bool):
    fast_sort=multiprocessing.Process(target=group_sort,args=(reverse,True))
    fast_sort.start()
    fast_sort.join()
    return group
def group_sort(reverse:bool,fast:bool=False):
    if fast==True:
        global group
    p=pandas.read_excel('七班课堂量化.xlsx',sheet_name=7)
    for i in range(0,7):
        L=p.iloc[i].values
        group[i]=L[5]
    if reverse:
        return sorted(group.items(), key=lambda x: x[1], reverse=True)[0]
    else:
        return sorted(group.items(), key=lambda x: x[1], reverse=False)[0]
'''
if __name__=='__main__':
    class7 = ('语文', '数学', '英语', '物理', '地理', '生物', '个人总分')
    name=people()
    group_dict=group_def(name)
    group_dict=sorted(group_dict.items(), key=lambda e:e[1], reverse=True)
    print(group_dict)
'''
name=people()
group=group_def(name).keys()
#print(list(group)[1])
