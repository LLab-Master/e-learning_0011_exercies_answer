
from datetime import datetime

class Employee:
    '''
    社員クラス
    '''
    def __init__(self,id,name,age,hiredate):
        self.id = id
        self.name = name
        self.age = age
        self.hiredate = hiredate

    def __str__(self):
        return f'社員ID={self.id} 氏名={self.name} 年齢={self.age} 入社日={self.hiredate}'



class EmployeeManager:
    '''
    社員データのCURD用クラス
    '''
    def __init__(self,filename):
        self.filename = filename
        with open(filename,'r',encoding='utf-8') as f:
            file_data = f.read()
        self.data = file_data.split('\n')
        if not self.data[-1]:
            del self.data[-1]

    def find_all(self):
        emp_list = []
        for lines in self.data:
            if lines:
                id,name,age,hiredate_str = lines.split(',')
                hiredate = datetime.strptime(hiredate_str,'%Y-%m-%d')
                emp_list.append(Employee(id,name,age,hiredate))

        return emp_list

    def find_byid(self,target_id):
        for lines in self.data:
            id, name, age, hiredate_str = lines.split(',')
            if  id == str(target_id):
                hiredate = datetime.strptime(hiredate_str, '%Y-%m-%d')
                emp = Employee(id,name,age,hiredate)
                return emp
        return None

    def _write_csv_file(self):

        with open(self.filename,'w',encoding='utf-8') as f:
            for line_data in self.data:
                f.writelines(line_data+ '\n')

    def add(self,emp):

        last_line =self.data[-1]
        last_id = int(last_line.split(',')[0])
        new_data = [str(last_id + 1), emp.name, str(emp.age),
                 datetime.strftime(emp.hiredate,'%Y-%m-%d')]
        new_data = ','.join(new_data)
        self.data.append(new_data)

        self._write_csv_file()


    def _find_location(self,id):
        idx = -1
        for i, emp in enumerate(self.data):
            if emp.split(',')[0] == str(id):
                idx = i
                break

        return idx

    def delete(self,id):
        idx = self._find_location(id)

        if idx >= 0:
            del self.data[idx]
            self._write_csv_file()


    def update(self,emp):
        update_id = emp.id
        new_data = [str(emp.id), emp.name, str(emp.age),
                    datetime.strftime(emp.hiredate, '%Y-%m-%d')]

        idx = self._find_location(emp.id)
        self.data[idx] = ','.join(new_data)
        self._write_csv_file()

