mylist = [123,124,234,236,345,347,349,343,456,458,567,678,789]
print(f'Mylist: {mylist}')

for i in mylist:
    if i % 2:
        print(f'odd: {i}')
        mylist.remove(i)
    else:
        print(f'even: {i}')

print(f'Mylist: {mylist}') 
exit(0)






























mylen = len(mylist)
i = 0
while i < mylen:
    if mylist[i] % 2:
        print(f'odd: {mylist[i]}')
        mylist.remove(mylist[i])
    else:
        print(f'even: {mylist[i]}')
        i += 1
    mylen = len(mylist)

print(f'Mylist: {mylist}') 
exit(0)