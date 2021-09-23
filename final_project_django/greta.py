import random

# x = chr(65)
# print(x)
#
# y = ord('A')
# print(y)
#
# c = 'p'
# print("The ASCII value of '" + c + "' is", ord(c))

# zmienna = "moze troche bardziej niz troche"


def reverse(string):
    arr = []
    for i in string:
        arr.append(i)
    arr.reverse()
    x = "".join(arr)
    return x


zmienna = reverse(zmienna)
print(zmienna)


def code(string):
    arr = []
    for i in string:
        arr.append(ord(i))
    return arr


print(code(zmienna))



def dic_maker(string):
    dic = {}
    counter = 1
    for i in string:
        dic[counter] = i
        counter += 1
    return dic


print(dic_maker(mess))
tt = dic_maker(link)

new_link = random.sample(tt.items(), 28)
print(new_link)
