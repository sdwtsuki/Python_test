
while 1 >0 :
    num_in = input("请输入：").strip()
    if num_in != None or num_in != '\r\n':
        num_out = float(num_in) * 1024
        print("输出结果为：", num_out)
    else:
        print("请输入非空值")


