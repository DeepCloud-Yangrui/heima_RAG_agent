"""
本节为扩展内容，展示python中的运算符的重载
"""


class Test(object):
    def __init__(self, name):
        self.name = name
    def __or__(self, other):
        return NewTest(self,other)
    def __str__(self):
        return self.name

class NewTest(object):
    def __init__(self,*args):
        self.my_list=[]         # 这里在NewTest内部我们自己维护一个列表
        for arg in args:
            self.my_list.append(arg)
    def __or__(self, other):
        self.my_list.append(other)
        return self

    def run(self):
        for i in self.my_list:
            print(i)



if __name__ == '__main__':
    a = Test('a')
    b = Test('b')
    c = Test('c')
    d = a | b | c           # 我们期望得到[a,b,c],为了得到这样的结果，就要对Test的or方法重写
    d.run()
    print(type(d))