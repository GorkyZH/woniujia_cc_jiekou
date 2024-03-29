# _*_ coding:utf-8 _*_
import json

"""
读取json文件工具类
"""
class OperationJson:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.read_data()
        #"/Users/mac/Desktop/practise/Demo/dataconfig/logincom.json"

    #读取json文件
    def read_data(self):
        #with open("../dataconfig/logincom.json") as fp:
         with open(self.json_file) as fp:
            data = json.load(fp)
            return data

    #获取json文件中某个字段的key
    def get_new_json(self, key, value):
        str_data = self.get_data(key)
        list_data = self.get_data(key)[1:-1].split(",")
        str_no_value = list_data[0]
        no_value = str_no_value.split(":")[1]
        new_no_value = str_data.replace(no_value, value)
        return new_no_value

    #根据关键字获取数据
    def get_data(self, key):
        #return self.data[id]
        return json.dumps(self.data[key])


if __name__ == '__main__':
    operJson = OperationJson("/Users/mac/Desktop/测试资料/蜗牛家产品线/woniujia_cc_jiekou/woniujia_cc_jiekou_git/woniujia_cc_project/dataconfig/request_pram.json")
    print(operJson.get_data('login'))
    print(operJson.get_data('boroughtList'))
    print(operJson.get_new_json('boroughtList', '"'+str(12)+'"'))
    # print(type(operJson.get_data('demo')))
    # print(operJson.get_new_json('login', 'operId', '112'))
    # print(operJson.get_new_json('boroughtList', 'pageNo', '3'))

