from collections import defaultdict
from normal_tools import gcd,hex_to_int,int_to_hex

def get_nec():
    ns,es,cs = [],[],[]
    for i in range(21):
        with open("my_tools\\Frame"+str(i),"r") as f:
            datas = f.read()
            ns.append(datas[0:256])
            es.append(datas[256:512])
            cs.append(datas[512:768]) 
    return ns,es,cs

def find_equal_data(li):
    e_dict = defaultdict(set)
    for i in range(len(li)):
        for j in range(len(li)):
            if i!=j:
                if li[i] == li[j]:
                    if i not in e_dict[li[i]]:
                        e_dict[li[i]].add(i)
                    if j not in e_dict[li[i]]:
                        e_dict[li[i]].add(j)
    return e_dict
def find_gyz(li):
    """
    li的内容是十六进制
    返回十六进制公因子
    """

    tem_dict = defaultdict(set)
    for i in range(len(li)):
        for j in range(len(li)):
            if i!=j:
                tem_gcd = gcd(hex_to_int(li[i]),hex_to_int(li[j]))
                if tem_gcd != 1:
                    if i not in tem_dict[tem_gcd]:
                        tem_dict[tem_gcd].add(i)
                    if j not in tem_dict[tem_gcd]:
                        tem_dict[tem_gcd].add(j)
    return tem_dict
if __name__ == "__main__":
    ns,es,cs = get_nec()
    #看看有没有相同n或有公因子n
    print(find_equal_data(ns))
    print(find_gyz(ns))

    #看看有没有低指数
    tem_es = []
    for i in range(len(es)):
        tem_es.append((i,hex_to_int(es[i])))
    print(sorted(tem_es,key=lambda x: x[1]))

    print(find_equal_data(es))
