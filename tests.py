import unittest
from inspect import isfunction

from db import get_connection

from scripts import fetch
from scripts import export
from scripts import grab_all
from scripts import migrate_v1
from scripts import migrate
from scripts import select

from scripts.utils import grab

class TestDataBase(unittest.TestCase):
    '''用于测试数据库连接'''

    def test_connection(self):
        '''测试数据库连接'''
        database_connection = get_connection()
        self.assertFalse(database_connection.is_closed())
        database_connection.close()

class TestCode(unittest.TestCase):
    '''用于测试代码问题'''

    def test_function_name(self):
        '''防止手贱改错'''
        self.assertTrue(isfunction(fetch.mainloop))
        self.assertTrue(isfunction(export.mainloop))
        self.assertTrue(isfunction(grab_all.mainloop))
        self.assertTrue(isfunction(migrate_v1.mainloop))
        self.assertTrue(isfunction(migrate.mainloop))
        self.assertTrue(isfunction(select.mainloop))

    def test_benben_api(self):
        '''判断全网犇犇api是否可用 / 可达 / 格式正确'''
        res = grab(1)
        print(res)
        self.assertTrue(isinstance(res,(list)))


if __name__ == '__main__':
    unittest.main()
