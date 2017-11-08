#! /user/bin/env python
# encoding=utf-8
#__author__ ='zx'
#__time__ ='2017-10-279:14'
'''
GetDataInfo_testcode
'''
import unittest
import paramunittest
import readConfig as readConfig
import json
from base import Log as Log
from base import common
from base import configHttp as ConfigHttp

login_xls = common.get_xls("LTClogin.xls", "LTClogin")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, CommandCode, Marker, TransferData,result, ExecuteResult, ErrorInfo,ErrorCode,ResultInfo):
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(int(token))
        self.CommandCode = str(CommandCode)
        self.marker = str(Marker)
        self.TransferData=str(TransferData)
        self.result = str(int(result))
        self.ExecuteResult =str(ExecuteResult)
        self.ErrorInfo =str(ErrorInfo)
        self.ErrorCode=str(ErrorCode)
        self.ResultInfo=str(ResultInfo)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        return (self.case_name+'测试数据获取的接口')

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.description(),"测试开始前准备")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('LTClogin')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token
        if self.token == '0':
            self.marker = self.login_token
        if self.token == '1':
            self.TransferData = localReadConfig.get_headers("marker_u")
        # set headers
        header = {"Content-type": "application/json"}
        configHttp.set_headers(header)
        print("第二步：设置header(token等)")
        # set params
        param={"CommandCode": self.CommandCode,"Marker": self.marker,"TransferData":self.TransferData}
        data =json.dumps(param)
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        self.info = self.return_json.json()
        print("第五步：检查结果")

    def tearDown(self):
        """
        :return:
        """
        #保存登录token
        info = self.info
        if info['ExecuteResult'] == True:
            # get uer token
            marker_u = common.get_value_from_return_json(info, 'ResultInfo', 'tokenNo')
            # set user token to config file
            localReadConfig.set_headers("marker_u", marker_u)
        else:
            pass
        self.log.build_case_line(self.case_name,str(info['ExecuteResult']),str(info['ErrorInfo']))
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            userName=common.get_value_from_return_json(self.info, 'ResultInfo','userName')
            self.assertEqual(str(self.info['ExecuteResult']),self.ExecuteResult)
            self.assertEqual(str(self.info['ErrorInfo']), self.ErrorInfo)
            self.assertEqual(userName,self.ResultInfo)

        if self.result == '1':
            self.assertEqual(str(self.info['ExecuteResult']), self.ExecuteResult)
            self.assertEqual(str(self.info['ErrorInfo']), self.ErrorInfo)