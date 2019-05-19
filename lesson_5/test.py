import unittest
from unittest.mock import Mock
import json
import time
import datetime

from msgr_core import MsgrServer, MsgrClient, MsgrListener, MsgrBase
from config import HTTPResponseCode, Common


class MsgrTest(unittest.TestCase):
    def setUp(self):
        self.virt_msg = {
            'field_1': 'value_1',
            'field_2': 'value_2'
        }
        self.virt_addr = ('127.0.0.1', '7777')
        self.virt_bytes = json.dumps(self.virt_msg).encode()
        self.virt_msgr_obj = Mock()
        self.virt_msgr_obj._sock.recv.return_value = self.virt_bytes
        self.virt_msgr_obj._sock.accept.return_value = (self.virt_msgr_obj._sock, self.virt_addr)

        self.code = HTTPResponseCode.OK
        self.checking_field = Common.RESPONSE

        self.user, self.status = 'some_user', 'some status'
        self.test_msg = {
            Common.ACTION: Common.PRESENCE,
            Common.TIME: time.time(),
            Common.TYPE: Common.STATUS,
            Common.USER: {
                Common.ACCOUNT: self.user,
                Common.STATUS: self.status
            }
        }

        self.code, self.f_time, self.alert = HTTPResponseCode.OK, time.time(), "OK"
        self.response = {
            Common.RESPONSE: self.code,
            Common.TIME: self.f_time,
            Common.ALERT: self.alert
        }

    def tearDown(self):
        pass

    def test_MsgrBase_send(self):
        # Really nothing to test.
        pass

    def test_MsgrBase_receive(self):
        msg = MsgrBase.receive(self.virt_msgr_obj)
        self.assertEqual(self.virt_msg, msg)

    def test_MsgrListener_accept_connection(self):
        res_server = MsgrListener.accept_connection(self.virt_msgr_obj)
        self.assertIsInstance(res_server, MsgrServer)
    
    def test_MsgrServer_create_response(self):
        srv_resp = MsgrServer.create_response(Mock(), code=self.code, msg=self.alert)
        self.assertEqual(self.response, srv_resp)

    def test_MsgrClient_parse_response(self):
        strf_time = datetime.datetime.fromtimestamp(float(self.response[Common.TIME])).strftime(Common.DATETIME_FORMAT)
        res_code, res_f_time, res_alert = MsgrClient.parse_response(Mock(), self.response)
        self.assertEqual(self.code, res_code)
        self.assertEqual(strf_time, res_f_time)
        self.assertEqual(self.alert, res_alert)

    def test_MsgrClient_generate_message(self):
        res_msg = MsgrClient.create_presence(Mock(), account_name=self.user, status=self.status)
        self.assertEqual(self.test_msg[Common.ACTION], res_msg[Common.ACTION])
        self.assertEqual(self.test_msg[Common.TYPE], res_msg[Common.TYPE])
        self.assertEqual(self.test_msg[Common.USER], res_msg[Common.USER])

    def test_MsgrServer_generate_response(self):
        resp = MsgrServer.create_response(Mock(), self.code)
        self.assertEqual(self.code, resp[self.checking_field])
