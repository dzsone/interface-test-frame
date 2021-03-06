import unittest, time, re, sys, os
from comm.Log import logger
from comm.config import Config,CONFIG_FILE,LOG_PATH,REPORT_PATH,CASE_PATH
from comm.mail import Email
from comm.HTMLTestRunner import HTMLTestRunner


if __name__ == '__main__':
    discover = unittest.defaultTestLoader.discover(CASE_PATH, "btest_*.py") # run the test case file which in the path.
    logger.info('_*_*_*interface test start*_*_*_')
    nowtime = time.strftime("%Y-%m-%d-%H-%M")
    report = REPORT_PATH + '\\' + nowtime + '_report.html'
    log = LOG_PATH + '\\' + nowtime + '_.log'
    with open(report, 'wb') as f:  # build the test report.
        runner = HTMLTestRunner(f, verbosity=2, title='interface report', description='description')
        runner.run(discover)
        f.close()
    e = Email(title='report',
              message='This is a interface test report!',
              receiver='123@123.com; 1234@123.com',
              server='smtp.123.com',
              sender='123@123.com',
              password='123',
              path=[report, log]
              )
    e.send() # send the test mail with test report and test log.
  
