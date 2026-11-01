class Employee:
    def __init__(self, id, name, base_money):
        self.id = id
        self.name = name
        self.base_money = base_money

    def calculate_salaries(self):
        return self.base_money

class Manager(Employee):
    def __init__(self, id, name, base_money, bonus):
        super().__init__(id, name, base_money)
        self.bonus = bonus

    def calculate_salaries(self):
        return self.base_money + self.bonus


class Developer(Employee):
    def __init__(self, id, name, base_money, project_sum):
        super().__init__(id, name, base_money)
        self.project_sum = project_sum

    def calculate_salaries(self):
        return self.base_money + self.project_sum * 10_000


emp_alex = Employee(0, "Alex", 50_000)
manager_ivan = Manager(1, "Ivan", 50_000, 10_000)
dev_eva = Developer(2, "Eva", 50_000, 5)

print(emp_alex.calculate_salaries())
print(manager_ivan.calculate_salaries())
print(dev_eva.calculate_salaries())