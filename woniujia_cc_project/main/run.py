# coding=utf-8
from data.get_data import GetData
from util.common_util import CommonUtil
from base.run_method import RunMethod
from data.dependent_data import DependentData
from util.send_email import SendEmail
import json

"""运行excel中的用例"""
class Run:
    def __init__(self, json_file, sheet_name, sheet_id, sql_base=None):
        self.json_file = json_file
        self.sheet_name = sheet_name
        self.sheet_id = sheet_id
        self.sql_base = sql_base
        self.data = GetData(self.json_file, self.sheet_name)
        self.run_method = RunMethod()
        self.util = CommonUtil()
        self.email = SendEmail()

    # 连接数据库,查询某字段的所有记录、总数、页数
    def get_sql_expect(self, i, sql_key):
        token = self.util.getToken(0)
        operid = self.util.getToken(1)
        # token_header = self.data.get_token_header(i, token)
        expect_res = self.data.get_except_data_for_sql(i, self.sql_base)  # 获取数据库返回的所有楼盘记录（返回类型：数组型）
        expect_value_list = []
        if len(expect_res) == 0:
            count = 0
            new_count = 1
            return count, new_count, expect_value_list
        else:
            for expect_index in range(0, len(expect_res)):
                expect_value = expect_res[expect_index][sql_key]  # 循环获取数据库返回的某个字段
                expect_value_list.append(expect_value)  # 将数据库中所有该字段存入该数组中
            count = len(expect_value_list)
            if count / 15 < 1:
                new_count = 1
            elif (count / 15) >= 1 and (count % 15) >= 1:
                new_count = int(count / 15) + 1
            else:
                new_count = int(count / 15)
            return count, new_count, expect_value_list

    # 获取response
    def is_depend(self, i, depend_morecase, request_type, url, token_header, data):
        # 判断是否存在依赖
        if depend_morecase != None:
            depend_data = DependentData(depend_morecase, self.sheet_name, self.json_file)
            dependent_response_data = depend_data.get_data_for_key(i, 0)
            if request_type == "get":
                request_url = url + dependent_response_data
                response = self.run_method.run_main(request_type, request_url, data, token_header)
            else:
                depend_key = self.data.get_dependent_key(i, 0)
                jsonData = json.loads(data)
                jsonData[depend_key] = dependent_response_data
                requestData = json.dumps(jsonData)
                response = self.run_method.run_main(request_type, url, requestData, token_header)  # 获取接口返回数据（返回类型：string型）
        else:
            response = self.run_method.run_main(request_type, url, data, token_header)  # 获取接口返回数据（返回类型：string型）
        return response

    # 判断expect表中记录和response列表记录是否相等，返回result是True或者False
    def get_result(self, count, expect_value_list, response, response_key):
        is_result = True
        response_dict = json.loads(response)  # 将response字符串型转换成字典型
        # if self.type == "data":
        #     response_list = response_dict['data']
        # elif self.type == "list":
        #     response_list = response_dict['data']['list']
        response_dict_data = response_dict['data']
        if 'list' in response_dict_data:
            response_list = response_dict['data']['list']
        else:
            response_list = response_dict_data
        if len(response_list) == count:
            is_result = True
        else:
            for response_index in range(len(response_list)):
                response_name = response_list[response_index][response_key]  # 循环获取接口返回的字段名称
                if self.util.is_contain(response_name, expect_value_list):  # 判断如果接口返回的xx字段存在数据库xx字段数组中，则测试通过
                    is_result = True
                else:
                    is_result = False
        return is_result

    # 判断expect表中记录的总数和response中某字段的数量是否相等，返回result是True或者False
    def get_result_count(self, count, response, response_key):
        response_dict = json.loads(response)  # 将response字符串型转换成字典型
        response_opt= response_dict['data'][response_key]
        if int(response_opt) == count:
            result = True
        else:
            result = False
        return result

    # 写入实际结果
    def write_result(self, fail_count, i, pass_count, result):
        if result:
            self.data.write_result(i, "测试通过", self.sheet_id)
            pass_count.append(i)
            print("测试通过")
        else:
            self.data.write_result(i, "测试失败", self.sheet_id)
            fail_count.append(i)
            print("测试失败")

    # 执行用例
    def go_to_run(self):
        # 获取用例行数
        row_count = self.data.get_case_line()
        pass_count = []
        fail_count = []
        result = True
        # 循环用例
        for i in range(1, row_count):
            # 获取isrun，是否运行该用例
            is_run = self.data.get_is_run(i)
            response_key = self.data.get_response_key(i)
            sql_key = self.data.get_sql_key(i)
            sql_type = self.data.get_sql_type(i)
            if is_run:
                url = self.data.get_url(i)
                request_type = self.data.get_request_type(i)
                is_connect = self.data.get_is_conn_db(i)  # 获取是否连接数据库，若是则执行sql，若不是直接获取期望结果
                depend_morecase = self.data.is_more_depend(i, 0)  # 获取依赖数据
                data = self.data.get_data_for_json(i)
                if is_connect:
                    token = self.util.getToken(0)
                    token_header = self.data.get_token_header(i, token)
                    # 获取预期结果
                    count = self.get_sql_expect(i, sql_key)[0]  # 数据库查询结果记录总数
                    new_count = self.get_sql_expect(i, sql_key)[1]  # 获取接口执行次数，翻页
                    expect_value_list = self.get_sql_expect(i, sql_key)[2]  # 获取某个字段在表中的所有值
                    # 获取返回数据
                    response = self.is_depend(i, depend_morecase, request_type, url, token_header, data)
                    if sql_type == "count":
                        # 比较接口返回的总数与数据库查询出的记录总数是否相等，相等返回True
                        actrual_result = self.get_result_count(count, response, response_key)
                    else:
                        for n in range(1, new_count + 1):
                            data = self.data.get_data_for_newjson(i, '"' + str(n) + '"')
                            # 比较预期结果和返回结果是否相等，相同返回result=True
                            actrual_result = self.get_result(count, expect_value_list, response, response_key)
                    self.write_result(fail_count, i, pass_count, actrual_result)
                else:
                    expect_res = self.data.get_except(i)
                    if i == 1:
                        header = self.data.get_header(i)
                        response = self.run_method.run_main(request_type, url, data, header)
                        res = json.loads(response)
                        # 获取token、operid并写入文件中
                        with open(self.util.base_dir(), 'w') as f:
                            f.write(res["data"]["token"] + "," + res["data"]["id"])
                        # print("获取token：", res["data"]["token"])
                    else:
                        token = self.util.getToken(0)
                        operid = self.util.getToken(1)
                        token_header = self.data.get_token_header(i, token)
                        response = self.is_depend(i, depend_morecase, request_type, url, token_header, data)
                        # response = self.run_method.run_main(request_type, url, data, token_header)
                    # print("返回结果：", response)
                    result = self.util.is_contain(expect_res, response)
                    self.write_result(fail_count, i, pass_count, result)

                self.data.write_response(i, response, self.sheet_id)
        # self.email.send_main(pass_count, fail_count)
        return response

if __name__ == '__main__':
    run = Run()
    run.go_to_run()