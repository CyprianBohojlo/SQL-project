import sqlite3 as db
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#The goal of the assigment was to use sqlite3 library in python, create a database, insert sample data, come up with 5 question that I will find answer to using SQL queries
conn = db.connect('final_project.db')
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS Employee;")
cursor.execute("DROP TABLE IF EXISTS Department;")
cursor.execute("DROP TABLE IF EXISTS Project;")


cursor.execute("""CREATE TABLE IF NOT EXISTS Department(
        Department VARCHAR(50),
        Manager_ID VARCHAR(8),
        Floor_Number VARCHAR(2),
        Annual_Budget NUMBER(6, 3),
        PRIMARY KEY(Department)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Employee(
        Employee_ID VARCHAR(8),
        First_Name VARCHAR(50),
        Last_Name VARCHAR(50),
        Department VARCHAR(50),
        Level VARCHAR(50),
        Birthdate DATE,
        PRIMARY KEY(Employee_ID),
        FOREIGN KEY(Department) REFERENCES Department
    );
    """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Project(
        Project_ID VARCHAR(6),
        Project_Name VARCHAR(50),
        Manager_ID VARCHAR(8),
        Department VARCHAR(50),
        PRIMARY KEY(Project_Name),
        FOREIGN KEY(Department) REFERENCES Department
    );
    """)
department_data = [['HR', '290363', '3', '100,000'],
                    ['IT', '173456', '5', '500,000'],
                    ['Finances', '139584', '4', '150,000'],
                    ['Marketing', '513536', '3', '200,000'],]
project_data = [['1', 'Hiring new software developers', '290363', 'HR'],
                    ['2', 'Creating ML model of a client', '173456', 'IT'],
                    ['3', 'creating a new website', '173456', 'IT'],
                    ['4', 'Creeating new database for HR', '173456', 'IT'],
                    ['5', 'Making a new ad', '513536', 'Marketing'],
                    ['6', 'Decreasing varaible costs', '139584', 'Finances'],
                    ['7', 'Buying new laptops for software developers', '139584', 'Finances'],
                    ['8', 'Hiring new CFO', '290363', 'HR'],
                    ['9', 'Creating an app for a client', '173456', 'IT']]

employee_data = [['173456', 'Andy', 'Williams', 'IT', 'Manager', '1975-12-03'],
                    ['139584', 'Hailey', 'Andrews', 'Finances', 'Manager', '1969-03-23'],
                    ['290363', 'Anne', 'Stevens', 'HR','Manager', '1985-05-17'],
                    ['513536', 'Jack', 'Brady', 'Marketing','Manager', '1987-01-02'],
                    ['394883', 'Alison', 'Warden', 'Finances','Senior', '1973-06-24'],
                    ['948362', 'Harvey', 'Kidd', 'IT','Junior', '1995-04-10'],
                    ['261836', 'Teresa', 'Rivas', 'HR','Junior', '1999-02-29'],
                    ['479473', 'Reggie', 'Hart', 'Marketing','Mid', '1993-12-12'],
                    ['296748', 'Mario', 'Cristo', 'Marketing','Senior', '1979-08-06'],
                    ['284538', 'Aaron', 'Wood', 'IT','Junior', '1994-09-30'],
                    ['153746', 'Natalia', 'Howard', 'IT','Mid', '1987-03-20'],
                    ['579377', 'Stefan', 'Perry', 'Finances','Senior', '1981-04-18'],
                    ['856255', 'Darius', 'Moreno', 'IT','Junior', '1999-11-25'],
                    ['957453', 'Violet', 'Reeves', 'HR','Senior', '1988-01-25'],
                    ['684493', 'Greta', 'Peterson', 'IT','Junior', '1997-11-01'],
                    ['134856', 'Carlo', 'Park', 'Finances','Junior', '2001-03-20'],
                    ['756732', 'Rita', 'Terry', 'HR','Mid', '1989-01-30'],
                    ['836284', 'Robbie', 'Vans', 'Marketing','Junior', '1999-11-19'],
                    ['856246', 'Jack', 'Evans', 'IT','Junior', '1999-05-13'],
                    ['098765', 'Max', 'Jackson', 'Marketing','Senior', '1981-10-11']]


cursor.executemany("INSERT INTO Department (Department, Manager_ID, Floor_Number, Annual_Budget) VALUES(?, ?, ?, ?)", department_data)
cursor.executemany("INSERT INTO Project (Project_ID, Project_Name, Manager_ID, Department) VALUES(?, ?, ?, ?)", project_data)
cursor.executemany("INSERT INTO Employee (Employee_ID, First_Name, Last_Name, Department, Level, Birthdate) VALUES(?, ?, ?, ?, ?, ?)", employee_data)

conn.commit()

cursor.execute("""SELECT * FROM Department;
""")

print('Department Table:') 
dep = cursor.fetchall()
for i in dep:
    print(i)

print('Project Table:')
cursor.execute("""SELECT * FROM Project;
""")
pro = cursor.fetchall()
for i in pro:
    print(i)

print('Employee Table:')
cursor.execute("""SELECT * FROM Employee;
""")
emp = cursor.fetchall()
for i in emp:
    print(i)


print("""QUESTIONS:
      \nQuestion 1: How many employees work in each department? 
      \nQuestion 2: How many juniors are supervised by each manager? 
      \nQuestion 3: How many employees work on each floor?
      \nQuestion 4: What is the average age of employees for each project?
      \nQuestion 5: What is the annual budget and the number of projects for each department? 
      """)

#Question 1 solution
cursor.execute("""SELECT DISTINCT(Department), COUNT(Department)
                  FROM Employee
                  GROUP by Department;
""")

q1 = cursor.fetchall()
Dep_names = []
emp_count = []
for i in q1:
    Dep_names.append(i[0])
    emp_count.append(i[1])


plt.bar(Dep_names,emp_count, color = 'blue', edgecolor = 'black')
plt.xlabel('Department')
plt.ylabel('Number of employees')
plt.title('Question 1')
plt.show()

#Question 2 solution
cursor.execute("""SELECT Department.Manager_ID, COUNT(Employee.Level)
                  FROM Department
                  LEFT JOIN Employee ON Employee.Department = Department.Department
                  WHERE Employee.Level == "Junior"
                  GROUP by Department.Manager_ID;

""")
q2 = cursor.fetchall()
Manager_ID = []
junior_count = []
for i in q2:
    Manager_ID.append(i[0])
    junior_count.append(i[1])

plt.bar(Manager_ID,junior_count, color='red')
plt.xlabel('Manager ID')
plt.ylabel('Number of juniors')
plt.title('Question 2')
plt.show()

#Question 3 solution
cursor.execute("""SELECT Department.Floor_Number, COUNT(Employee.Department)
                  FROM Department
                  LEFT JOIN Employee ON Employee.Department = Department.Department 
                  GROUP by Department.Floor_Number;
""")

q3 = cursor.fetchall()
floor_num = []
emp_floor_count = []
for i in q3:
    floor_num.append(i[0])
    emp_floor_count.append(i[1])

plt.bar(floor_num, emp_floor_count)
plt.xlabel('Floor Number')
plt.ylabel('Number of employees')
plt.title('Question 3')
plt.show()


#Question 4
cursor.execute("""SELECT Project.Project_ID, Project.Project_Name, ROUND(AVG(DATE() - Employee.Birthdate))
                   FROM Project
                   LEFT JOIN Employee ON Employee.Department = Project.Department
                   GROUP by Project.Project_ID;
""")   
print('Question 4 solution: ') 
q4 = cursor.fetchall()
for i in q4:
    print(i)


#Question 5 solution
cursor.execute("""SELECT Department.Department, Department.Annual_Budget, COUNT(Project.Project_ID)
                  FROM Department
                  LEFT JOIN Project ON Project.Department = Department.Department
                  GROUP by Department.Department
                  ORDER by Department.Annual_Budget DESC;
""")

q5 = cursor.fetchall()
print('Question 5 soltuion: ')
for i in q5:
    print(i)

conn.close()

