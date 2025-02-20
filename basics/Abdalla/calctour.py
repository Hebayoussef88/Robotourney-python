
op = input("choose an opreator (/.-.*.+):  ")
num1 = int(input("enter first number:  "))
num2 = int(input("enter second number:  "))
if op == "/":
    res = num1/num2
elif op == "-":
    res = num1-num2
elif op == "+":
    res = num1+num2
elif op == "*":
    res = num1*num2
print(num1,op,num2, "=" ,res)
