#python -m unittest test_manager -v で実行
from manager import Employee,EmployeeManager
from datetime import datetime
import unittest
import os
import shutil

class TestEmployee(unittest.TestCase):

    def test___init__(self):
        name = "立川太郎"
        age = 33
        hiredate = "2001-01-01"
        emp = Employee(None,name,age,hiredate)
        self.assertEqual(emp.name, name)
        self.assertEqual(emp.age, age)
        self.assertEqual(emp.hiredate, hiredate)

    def test___str__(self):
        name = "立川太郎"
        age = 33
        hiredate = "2001-01-01"
        emp = Employee(None,name,age,hiredate)
        self.assertEqual(str(emp), "社員ID=None 氏名=立川太郎 年齢=33 入社日=2001-01-01")

class TestEmployeeManager(unittest.TestCase):

    #テスト前に一度だけ呼ばれる
    @classmethod
    def setUpClass(cls): 
        cls.filename = 'data.csv'
        cls.emp_m = EmployeeManager(cls.filename)
        
    # テスト後に一度だけ呼ばれる data.csvの退避と初期化
    @classmethod
    def tearDownClass(cls):
        if os.path.exists("data_old.csv"):
            os.remove("data_old.csv")
        os.rename("data.csv", "data_old.csv")
        shutil.copy2("data_org.csv", "data.csv")

    def test___init__(self):
        filename = 'data.csv'
        self.assertEqual(self.emp_m.filename, filename)

    def test_01_find_all(self):
        result = self.emp_m.find_all()
        self.assertEqual(f'{result[0].id} {result[0].name} {result[0].age} {result[0].hiredate}', "1 山田太郎 23 2010-03-21 00:00:00")
        self.assertEqual(f'{result[1].id} {result[1].name} {result[1].age} {result[1].hiredate}', "2 鈴木一郎 33 2008-12-01 00:00:00")
        self.assertEqual(f'{result[2].id} {result[2].name} {result[2].age} {result[2].hiredate}', "3 田中美智子 34 2010-04-01 00:00:00")

    def test_02_find_byid(self):
        result = self.emp_m.find_byid(1)
        self.assertEqual(f'{result.id} {result.name} {result.age} {result.hiredate}', "1 山田太郎 23 2010-03-21 00:00:00")

        result = self.emp_m.find_byid(99)
        self.assertEqual(result, None)

    def test__write_csv_file(self):
        tmp = self.emp_m.data[0]
        self.emp_m.data[0] += " test"
        self.emp_m._write_csv_file()
        self.emp_m.data[0] = tmp
        result = self.emp_m.find_byid(1)
        self.assertEqual(f'{result.id} {result.name} {result.age} {result.hiredate}', "1 山田太郎 23 2010-03-21 00:00:00")

    def test_add(self):
        name = "テスト太郎"
        age = 43
        hiredate = datetime.strptime("2011-01-01", '%Y-%m-%d')
        emp = Employee(None,name,age,hiredate)
        self.emp_m.add(emp)
        
        result = self.emp_m.find_byid(4)
        self.assertEqual(f'{result.id} {result.name} {result.age} {result.hiredate}', "4 テスト太郎 43 2011-01-01 00:00:00")

    def test__find_location(self):
        result = self.emp_m._find_location(1)
        self.assertEqual(result, 0)

    def test_delete(self):
        self.emp_m.delete(1)
        result = self.emp_m.find_byid(1)
        self.assertEqual(result, None)

    def test_update(self):
        id = 1
        name = "テスト太郎"
        age = 23
        hiredate = datetime.strptime("2010-03-21", '%Y-%m-%d')
        emp = Employee(id,name,age,hiredate)
        self.emp_m.update(emp)
        result = self.emp_m.find_byid(1)
        self.assertEqual(f'{result.id} {result.name} {result.age} {result.hiredate}', "1 テスト太郎 23 2010-03-21 00:00:00")
