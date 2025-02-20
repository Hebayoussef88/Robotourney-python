for i in range(5):
    print("hello")
for i in range(0,5,2):
    print(i)
num = int(input("enter num:"))
for i in range(1,num+1,2):
    print(i)
for i in range(10):
    if i == 3:
        continue
    print(i)
for i in range(10):
    if i == 3:
        pass
    print(i)
for i in range(10):
    if i == 3:
        break
    print(i)
st = "kjkfzljjokl"
for c in range(len(st)):
    if st[c] == "z":
        break
    print(st[c])


