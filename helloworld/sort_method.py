"""
排序算法：
LB三人组
	冒泡排序
	选择排序
	插入排序
快速排序
NB二人组
	堆排序
	归并排序
"""
import random, time


def cal_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print("%s running time: %s secs." % (func.__name__, t2 - t1))
        return result
    return wrapper


@cal_time
def sort_bubble(li):
    """
    冒泡排序
    原始算法：复杂度n*n
    :param li:
    :return:
    """
    for i in range(len(li) - 1):
        for j in range(len(li) - i - 1):
            if li[j] > li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]


@cal_time
def sort_bubble_X(li):
    """
    冒泡排序
    优化算法：效果不明显，可能效率更低
    :param li:
    :return:
    """
    for i in range(len(li) - 1):
        bChanged = False
        for j in range(len(li) - i - 1):
            if li[j] > li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]
                bChanged = True
        if not bChanged:
            # 如果这次没有位置变更，说明顺序已正确，不需要再排序
            break


@cal_time
def sort_select(li):
    """
    选择排序：复杂度n*n
    :param li:
    :return:
    """
    for i in range(len(li) - 1):
        posMin = i
        for j in range(i+1, len(li)):
            if li[j] < li[posMin]:
                posMin = j
        if i != posMin:
            li[i], li[posMin] = li[posMin], li[i]


@cal_time
def sort_insert(li):
    """
    插入排序：复杂度n*n
    :param li:
    :return:
    """
    for i in range(1, len(li)):
        j = -1
        bFind = False
        for j in range(i - 1, -1, -1):
            if li[i] >= li[j]:
                bFind = True
                break
        if bFind:
            li.insert(j + 1, li.pop(i))
        else:
            li.insert(0, li.pop(i))


@cal_time
def sort_quick0(li):
    sort_quick(li)

def sort_quick(li, pStart=0, pEnd=-1):
    """
    快速排序：复杂度nlogn
    :param li:
    :return:
    """
    if pEnd == -1:
        pEnd = len(li) - 1
    if pStart < pEnd:
        pMid = sort_quick_cut(li, pStart, pEnd)
        sort_quick(li, pStart, pMid - 1)
        sort_quick(li, pMid + 1, pEnd)

def sort_quick_cut(li, pStart, pEnd):
    tmp = li[pStart]
    while pStart < pEnd:
        while pStart < pEnd and li[pEnd] >= tmp:
            pEnd -= 1
        li[pStart] = li[pEnd]
        while pStart < pEnd and li[pStart] <= tmp:
            pStart += 1
        li[pEnd] = li[pStart]
    li[pStart] = tmp
    return pStart

@cal_time
def sort_heap(li):
    """
    堆排序：复杂度nlogn
    :param li:
    :return:
    """
    n = len(li)
    for i in range(n // 2 - 1, -1, -1):
        sort_heap_shift(li, i, n - 1)
    for i in range(n - 1, -1, -1):
        li[i], li[0] = li[0], li[i]
        sort_heap_shift(li, 0, i - 1)

def sort_heap_shift(li, pStart, pEnd):
    i = pStart
    j = 2 * i + 1
    tmp = li[i]
    while j <= pEnd:
        if j < pEnd and li[j] < li[j + 1]:
            j += 1
        if tmp < li[j]:
            li[i] = li[j]
            i = j
            j = 2 * i + 1
        else:
            break
    li[i] = tmp


data = list(range(5000))
random.shuffle(data)
data1 = data[:]
data2 = data[:]
data3 = data[:]
data4 = data[:]
data5 = data[:]
print(data)
sort_bubble(data1)
print(data1)
sort_select(data2)
print(data2)
sort_insert(data3)
print(data3)
sort_quick0(data4)
print(data4)
sort_heap(data5)
print(data5)