import unittest
from unittest.mock import Mock
import json
import time
import datetime

from msgr_core import MsgrServer, MsgrClient, MsgrListener, MsgrBase
from config import Code, Const, Common


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

        self.code = Code.OK
        self.checking_field = Const.RESPONSE

        self.user, self.status = 'some_user', 'some status'
        self.test_msg = {
            Const.ACTION: Const.PRESENCE,
            Const.TIME: time.time(),
            Const.TYPE: Const.STATUS,
            Const.USER: {
                Const.ACCOUNT: self.user,
                Const.STATUS: self.status
            }
        }

        self.code, self.f_time, self.alert = Code.OK, time.time(), "OK"
        self.response = {
            Const.RESPONSE: self.code,
            Const.TIME: self.f_time,
            Const.ALERT: self.alert
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
        strf_time = datetime.datetime.fromtimestamp(float(self.response[Const.TIME])).strftime(Common.DATETIME_FORMAT)
        res_code, res_f_time, res_alert = MsgrClient.parse_response(Mock(), self.response)
        self.assertEqual(self.code, res_code)
        self.assertEqual(strf_time, res_f_time)
        self.assertEqual(self.alert, res_alert)

    def test_MsgrClient_generate_message(self):
        res_msg = MsgrClient.create_presence(Mock(), account_name=self.user, status=self.status)
        self.assertEqual(self.test_msg[Const.ACTION], res_msg[Const.ACTION])
        self.assertEqual(self.test_msg[Const.TYPE], res_msg[Const.TYPE])
        self.assertEqual(self.test_msg[Const.USER], res_msg[Const.USER])

    def test_MsgrServer_generate_response(self):
        resp = MsgrServer.create_response(Mock(), self.code)
        self.assertEqual(self.code, resp[self.checking_field])
