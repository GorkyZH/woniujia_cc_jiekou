#coding:utf-8

"""
封装常量
"""
class global_var:
    module = '0'         #模块
    Id = '1'             #ID
    case = '2'           #用例
    url = '3'            #url接口地址
    run = '4'            #是否运行
    request_type = '5'   #请求类型
    header = '6'         #头部
    case_dependent = '7' #case依赖
    data_dependent = '8' #依赖的返回数据
    key_depedent = '9'   #请求数据依赖字段
    parameter = '10'     #请求参数
    response_key = '11'  #接口返回字段
    conn_db = '12'       #是否连接数据库
    sql_key = '13'       #查询表返回的字段名
    sql_type = '14'
    expect = '15'        #预期结果
    result = '16'        #实际结果
    response = '17'      #返回结果

#获取模块
def get_module():
    return global_var.module

#获取id
def get_id():
    return global_var.Id

#获取url
def get_url():
    return global_var.url

#是否运行
def get_run():
    return global_var.run

#获取请求类型
def get_request_type():
    return global_var.request_type

#获取头部
def get_header():
    return global_var.header

#获取头部值
def get_header_value():
    Headers = {
        "Content-Type":"application/json"
    }
    return Headers

#获取带token的头部值
def get_token_header_value(token_value):
    Headers = {
        "Authorization":'Bearer '+token_value,
        "Content-Type":"application/json"
    }
    return Headers

#获取case依赖
def get_case_dependent():
    return global_var.case_dependent

#获取返回数据依赖
def get_data_dependent():
    return global_var.data_dependent

#获取返回数据的依赖字段
def get_key_dependent():
    return global_var.key_depedent

#获取请求参数
def get_parameter():
    return global_var.parameter

#获取接口返回的字段名
def get_response_key():
    return global_var.response_key

#获取是否连接数据库
def get_conn_db():
    return global_var.conn_db

#获取表中查询出的字段名
def get_sql_key():
    return global_var.sql_key

#获取对比列表还是总数
def get_sql_type():
    return global_var.sql_type

#获取预期结果
def get_except():
    return global_var.expect

#获取实际结果
def get_result():
    return global_var.result

#获取实际返回结果
def get_response():
    return global_var.response

