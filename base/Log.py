import os
import readConfig as readConfig
import logging
from datetime import datetime
import threading

localReadConfig = readConfig.ReadConfig()

#初始化,创建日志文件
class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # 创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))

        # defined formatter
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #格式化
        handler.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(handler)
    #获取日志
    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger
    #创建开始分隔线
    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    #创建结束分隔线
    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    #创建日志内容
    def build_case_line(self, case_name, ExecuteResult,ErrorInfo):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+" - ExecuteResult:"+ExecuteResult+" - ErrorInfo:"+ErrorInfo)

    #输出测试报告
    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    #获取日志路径
    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath

    #写入测试报告
    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logger.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if  MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")

