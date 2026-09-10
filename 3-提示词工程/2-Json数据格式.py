"""
案例： Json数据格式，主要是Json与python中的字典、列表的双向转换
"""

# 需要导入Json库
import json

# 1、字典转换为Json
d = {
    "name": "周杰轮",
    "age": 11,
    "gender": "男"
}

dictionary = json.dumps(d, ensure_ascii=True)
print(dictionary,type(dictionary))

# 2、列表转换为Json
l = [
    {
        "name": "周杰轮",
        "age": 11,
        "gender": "男"
    },
    {
        "name": "蔡依临",
        "age": 12,
        "gender": "女"
    },
    {
        "name": "小明",
        "age": 16,
        "gender": "男"
    }
]
list = json.dumps(l, ensure_ascii=True)
print(list,type(list))


# 3、 Json转换为字典和列表

json_str = '{"name": "周杰轮", "age": 11, "gender": "男"}'
json_array_str = '[{"name": "周杰轮", "age": 11, "gender": "男"}, {"name": "蔡依临", "age": 12, "gender": "女"}, {"name": "小明", "age": 16, "gender": "男"}]'
my_dictionary = json.loads(json_str)
my_list = json.loads(json_array_str)
print(json.loads(json_str))
print(json.loads(json_array_str))
print(type(my_dictionary),type(my_list))