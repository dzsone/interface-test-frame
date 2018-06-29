import unittest, os, sys, time, re, json, requests, random, hashlib, string
from comm.excel_reader import *
from comm.Log import logger
from comm.connDB import *
from comm.config import Config, DATA_PATH, CONFIG_FILE, LOG_PATH, REPORT_PATH


class APPinterface(unittest.TestCase):
    c = Config().get('Http')
    URL = c.get('turl')  # get test url
    port = c.get('port')
    host = str(URL) + ':' + str(port)  

    def setUp(self):
        pass

    def test_001_APP_login(self):
        '''APP Login'''
        logger.info('-*-*-*-*-*login test start*-*-*-*-*-')
        url = self.host + readExcel(2, 1, 1)
        param = readExcel(2, 1, 2)
        headers = json.loads(readExcel(2, 1, 3))
        logger.debug([url, param, headers])
        print([url, param, headers])
        r = requests.post(url, data=param, headers=headers)
        logger.debug(r.status_code)
        rq = json.loads(r.text)
        logger.info(rq)
        try:
            self.assertEqual(0, rq['retCode'])
            self.assertEqual(u'OK', rq['msg'])
            self.assertEqual(200, r.status_code)
            token = rq['data']['token']
            writeExcel(2, 1, 5, token)
            logger.debug(token)
            logger.info('success!')
            logger.info('-*-*-*-*-*login test end*-*-*-*-*-')
            return token
        except Exception as e:
            print(str(e))
            token = rq['data']['token']
            writeExcel(2, 1, 5, token)
            logger.debug(token)
            logger.info('fail')
            logger.info(r.text)
            logger.info('-*-*-*-*-*login test end*-*-*-*-*-')
            raise

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
