#!/usr/bin/env python
# #coding=utf-8
dict_de = {}
dict_de[''] = ''
dict_en = {'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','a':'1010','b':'1011','c':'1100','d':'1101','e':'1110','f':'1111','A':'1010','B':'1011','C':'1100','D':'1101','E':'1110','F':'1111'}
dict_en[' '] = 'space'
for key in dict_en.keys():
    dict_de[dict_en[key]] = key

#字符串转二进制码,mode默认为'a',s为ascii码，设为'b'时视作16进制按位转为二进制码
def encode(s,mode = None):
    if mode is None or mode == 'a':
        return ' '.join([bin(ord(c)).replace('0b', '')for c in s])
    if mode == 'b':
        return ' '.join([dict_en[c] for c in s])
#解码,二进制转字符串a/或16进制b
def decode(s,mode = None):
    if mode is None or mode == 'a':
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
    if mode == 'b':
        return ''.join([dict_de[b] for b in s.split(' ')])

#将16进制数按位转为2进制，并去空格等不属于16进制的杂质字符
def hex2bin(str):
    out = ''
    for char in str:
        # if char != ' ':
        if char in dict_en.keys() and char != ' ':
            out += dict_en[char]
    return out

#将16进制数按位转为2进制，并保留空格
def hex2bin_space_stay(str):
    out = ''
    for char in str:
        if char != ' ':
            out += dict_en[char]
        else:
            out +=' '
    return out

#ascii转16进制，输入、输出都是字符串形式
def a2h(str_a):
    temp = encode(str_a)
    # print(temp)
    temp1 = []
    for i in temp.split(' '):
        # x = '0'+i if len(i)==7 else '00'+i
        x = '0'*(8-len(i))+i
        temp1.append(x[0:4]+' '+x[4:9])
    temp2 = ''
    for i in temp1:
        temp2 = temp2 + i + ' '
    # print(temp2)
    return decode(temp2, 'b')
#16进制转ascii,str_h为int型或long型(无论进制)或str型但不含'0x'不含'L'，输出是字符串
def h2a(str_h):
    if type(str_h) == int:
        return ten2a(str_h)
    if type(str_h) == long:
        return ten2a(str_h)
    temp = hex2bin(str_h)
    #print(temp)
    temp1 = []
    length = len(temp)/8
    for i in range(int(length)):
        temp1.append(temp[0+i*8:8+i*8])
    #print(temp1)
    temp2 = temp1[0]
    for i in temp1[1:]:
        temp2 = temp2 + ' ' + i
    #print(temp2)
    return decode(temp2)

def bin2hex(str1):
    s = int(str1,2)
    if type(s) == int:
        s = str(hex(s))[2:]
    if type(s) == long:
        s = str(hex(s))[2:-1]
    return s

#s为10进制数字或字符串，输出ascii编码字符串
def ten2a(s):
    if type(s) == str:
        s = int(s)
        return ten2a(s)
    elif type(s) == long:
        return h2a(str(hex(s))[2:-1])
    elif type(s) == int:
        return h2a(str(hex(s))[2:])

#把含杂质的16进制字符串提纯，第二个参数为空默认是去除所有杂质符号，例如' ',':'等
# 也可指定剔除符号，输入的第二个参数为列表或单个字符表示要剔除的符号
def str_purification(s,mode = None):
    temp = ''
    if mode == None:
        for c in s:
            temp += c if c in dict_en.keys() and c != ' ' else ''
    elif type(mode) == list:
        for c in s:
            temp += c if c not in mode else ''
    elif type(mode) == str:
        assert len(mode) == 1,'if want to remove more than one element,use "list" Instead of "str" '
        for c in s:
            temp += c if c != mode else ''
    return temp

def read2hex(name):
    import binascii
    f = open(name, 'rb')
    ss = f.read()
    f.close()
    s = ''
    for c in ss:
        s += str(binascii.hexlify(c))
    return s

def hon(str1, mode=None):
    result = ''
    if mode == None:
        temp = ''
        if len(str1)%4 != 0:
            temp = str1[-1]
        i = 3
        while i < len(str1):
            result += str1[i]
            result += str1[i-2]
            i += 4
        result += temp
    if mode == 's2h':
        str1 = a2h(str1)
        i = 0
        str1 = str1 + '00'
        while i < len(str1):
            result += '00' + str1[i+2:i+4]
            result += '00' + str1[i:i+2]
            i += 4
        # if i <= len(str1) - 2:
        #     result += '00' + str1[i:i+2]
    return result

def test():
    out = hex2bin('a 8')
    print 'hex2bin("a 8"):', out
    out = hex2bin_space_stay('aa 8')
    print'hex2bin_space_stay("a 8"):', out
    out = hex2bin_space_stay('1856 ab90')
    print(out)
    xx = encode('a bc', 'a')
    print "encode('a bc', 'a')", xx
    print "decode(xx, 'a')", decode(xx, 'a')
    print "ten2a(123456789)", ten2a(123456789)
    print(a2h('Happy birthday to FaChang!'))
    print(h2a('486170707920626972746864617920746f2046614368616e6721'))
    print(bin2hex('1111100010100100100'))
    print(str_purification('4861707!@079 20::@@@8%%61-~7920746f20@@14368616e6721'))

#某值是否在区间内，默认算闭区间，m是其它值时算开区间
def isin_Interval(item, l, m=None):
    l.sort
    if m==None:
        for i in l:
            if item >= i[0] and item <= i[1]:
                return True
        return False
    # if m!=None:
    for i in l:
        if item > i[0] and item < i[1]:
            return True
    return False
#区间取并
def Interval_and(l, tuple):
    if l == []:
        l.append(tuple)
        return l
    l.sort()
    for i in range(len(l)):
        if l[i][0] <= tuple[0]:#第一大类，原操作数左区间更左，细分为原操作数第一部分右区间更右，原操作数第n部分右区间更右，和新操作数右区间更右
            if l[i][1] >= tuple[1]:
                return l
            elif tuple[0] <= l[i][1]:
                j = i + 1
                while j < len(l) and tuple[1] >= l[j][0]:
                    j += 1
                l[i] = (l[i][0], max(tuple[1],l[j -1][1]))
                if j == i + 1:
                    return l
                while j != i + 1:
                    del l[j - 1]
                    j -= 1
                return l
            if i < len(l) - 1:
                print(len(l) - 1)
                continue
            l.append(tuple)
            l.sort()
            return l
        # if tuple[0] < l[i][0]:第二大类，新操作数左区间更左
        if tuple[1] < l[i][0]:
            l.append(tuple)
            return l.sort()
        # if tuple[1] >= l[i][0]:
        j = i + 1
        while j < len(l) and tuple[1] >= l[j][0]:
            j += 1
        l[i] = (tuple[0], max(tuple[1], l[j - 1][1]))
        if j == i + 1:
            return l
        while j != i + 1:
            del l[j - 1]
            j -= 1
        return l

if __name__ == '__main__':
    #test()
    s = '0074006800700074002f003a0067002f0074006500700075006e006100630064006f0062002e007a006f0063002f006d0069006e0065006e006a002f006e006f00300030002e0031007800650000006500410025005000500041004400410054005c00250065006900700078006f006c002e00720078006500000065'
    s1 = '0074006800700074002f003a0067002f0074006500700075006e006100630064006f0062002e007a006f0063006e006f00300030002e00310078006500000065'
    print(h2a(s))
    print(hon(h2a(s)))
    print(hon(h2a(s1)))
    s = '%SystemRoot%\System32\cmd.exe'
    # print(a2h(s))
    print(hon(s, 's2h'))
    print(hon(h2a(hon(s, 's2h'))))
    print(hon('ComSpec', 's2h'))
    print(hon(h2a(hon('ComSpec', 's2h'))))
    c = '00530025 00730079 00650074 0052006d 006f006f 00250074 0063005c 0064006d 0065002e 00650078 00000000'
    print(len('006f00430053006d006500700000006300000000002500740063005c0064006d0065002e0065007800000000'))
    print(len('0053002500730079006500740052006d006f006f002500740053005c00730079006500740033006d005c0032006d0063002e00640078006500000065'))
    print(len('002f006d0069006e0065006e006a002f'))
