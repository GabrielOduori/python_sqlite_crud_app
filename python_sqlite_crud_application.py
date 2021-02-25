import sqlite3
import re

# Define DBOperation class to manage all data into the database. 
# Give a name of your choice to the database

class DBOperations:
  sql_create_table_firsttime = '''CREATE TABLE 
    EmployeeUoB(Title TEXT, Forename TEXT, Surname TEXT, Email_Address TEXT, Salary DOUBLE)'''

  sql_create_table = '''CREATE TABLE IF NOT EXISTS 
    EmployeeUoB(EmployeeID INTEGER PRIMARY KEY, Title TEXT, Forename TEXT, Surname TEXT, Email_Address TEXT, Salary DOUBLE) WITHOUT ROWID
	'''
  sql_check_table_exists = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='EmployeeUoB' '''
  sql_insert = '''INSERT INTO EmployeeUoB(EmployeeID, Title, Forename, Surname, Email_Address, Salary )
	    	    VALUES ( ?,?,?,?,?,? )'''

  sql_select_all = "SELECT * FROM EmployeeUoB"
  sql_search = "SELECT * FROM EmployeeUoB WHERE EmployeeID = ?"
  
  sql_update_data = ''' UPDATE EmployeeUoB
                  SET Title = ?, Forename = ?, Surname = ?, Email_Address= ?, Salary= ?
	        WHERE EmployeeID = ?
	'''
  sql_delete_data ='''DELETE FROM EmployeeUoB WHERE EmployeeID = ?'''

 
  def __init__(self):
    try:
      self.conn = sqlite3.connect('main.db')
      self.cur = self.conn.cursor()

      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect('main.db')
    self.cur = self.conn.cursor()

  def create_table(self):
    try:
      self.get_connection()

      # Check is the table is aleady created
      self.cur.execute(self.sql_check_table_exists)
      if self.cur.fetchone()[0]==1:
        print('Table EmployeeUoB aleady exists')
      else:
        self.cur.execute(self.sql_create_table)
        self.conn.commit()
        print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()

      emp = Employee()
      employee_id = input("Enter Employee ID: ")
      if (self.check_input_whitespace(employee_id) == False and employee_id.isdigit()==False):
        print('Invalid Employee ID')
        return 

      employee_title = input("Enter Title: ")
      if self.check_input_whitespace(employee_title) == True:
        print('Invalid inout for employee title')
        return 
     

      forename = input("Enter Forename: ")
      if self.check_input_whitespace(forename) == True:
        print('Invalid inout for employee Forename')
        return 

      surname = input("Enter Surname: ")    
      if self.check_input_whitespace(surname) == True:
        print('Invalid inout for employee Surname')
        return 
    

      email = input("Enter Email Address: ")
      if email is not None and self.check_valid_email(email) == False:
        print('Invalid email')
        return

      salary = input("Enter Salary: ")
      if self.is_integer(salary) == False and self.is_float(salary)==False:
        print('Invalid salary input')
        return

      emp.set_employee_id(int(employee_id))
      emp.set_employee_title(str(employee_title))
      emp.set_forename(str(forename))
      emp.set_surname(str(surname))
      emp.set_email(str(email))
      emp.set_salary(float(salary))

      self.cur.execute(self.sql_insert,tuple(str(emp).split("\n")))
      if self.cur.fetchall() is None:
        print('Supplied EMployee ID already exists')
        return
      self.conn.commit()
      print("\n")
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# Select all records in a database
  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      results = self.cur.fetchall()
      if len(results) <1:
        print('Table is still empty table. Please insert some data')

      else:
        for result in results:
          print(result)

        # think how you could develop this method to show the records
        # Display all the records as tuple


    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
  def search_data(self):
    try:
      self.get_connection()
      employeeID = int(input("Enter Employee ID: "))
      self.cur.execute(self.sql_search,tuple(str(employeeID)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Employee ID: " + str(detail))
          elif index == 1:
            print("Employee Title: " + detail)
          elif index == 2:
            print("Employee Name: " + detail)
          elif index == 3:
            print("Employee Surname: " + detail)
          elif index == 4:
            print("Employee Email: " + detail)
          else:
            print("Salary: "+ str(detail))
      else:
        print("\n")
        print ("No Record for EmployeeID :" + str(employeeID))
            
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Checks for a valid email input
  def check_valid_email(self, email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return True if(re.search(regex,email)) else False

  # Checks if an input is a fload. This is for salary checks
  def is_integer(self, salary_input):
    try:
      int(salary_input)
      return True
    except Exception as e:
      return False
  
  # Checks if an input is a fload. This is for salary checks
  def is_float(self, salary_input):
    try:
      float(salary_input)
      return True
    except Exception as e:
      return False
    
  # Checks all while space so that empty data isnt added to the database during an update routine.
  def check_whitespace(self, input_value, db_value):
    return db_value if input_value.isspace() else input_value

  def check_input_whitespace(self,input_String):
    return True if input_String.isspace() else False

# Method to update a record in the database
  def update_data(self):
    try:
      self.get_connection()
      id = int(input("Enter Employee ID to be updated: "))
      self.cur.execute(self.sql_search,[id])
      result = self.cur.fetchone()
      if result is None:
        print('The ID doesnt exit')
        return
      print(result)
      print('Proceed to update the record as follows:')

      # The user is given an option to choose a field to update as they may not want to update everything 
      # in the database.
      title = (self.check_whitespace(str(input("Enter Title: ")), result[1]) or result[1])
      forename = (self.check_whitespace(str(input("Enter Forename: ")), result[2]) or result[2])
      surname = (self.check_whitespace(str(input("Enter Surname: ")), result[3]) or result[3])
      email = (self.check_whitespace(str(input("Enter Email Address: ")), result[4]) or result[4])
      
      if email is not None and self.check_valid_email(email) == False:
        print('Invalid email')
        return

      salary = (self.check_whitespace(str(input("Enter Salary: ")), result[5]) or result[5])
  
      if self.is_integer(salary) == False and self.is_float(salary)==False:
        print('Invalid salary input')
        return
      self.cur.execute(self.sql_update_data,[title,forename,surname, email, salary,id])
      result  = self.cur.fetchall()
      if result is not None:
        self.conn.commit()  
        print("Updated record data successfully")
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# Define Delete_data method to delete data from the table.
# The user will need to input the employee id to delete the
# corrosponding record. 
  def delete_data(self):
    id = int(input("Enter Employee ID: "))
    try:
      self.get_connection()
      self.cur.execute(self.sql_search,[id])
      result = self.cur.fetchone()
      if result is not None:
        confirm_delete = input('Are you sure you want to delete this record (Y/N)?')
        if confirm_delete =='Y':
          self.cur.execute(self.sql_delete_data,[id])
          self.conn.commit()
          print("\n")
          print("Record deleted successfully")
        else:
          print('No delettion initiated')
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally: 
      self.conn.close()

class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary
  
  def get_employee_id(self):
    return self.employeeId

  def get_employee_title(self):
    return self.empTitle
  
  def get_forename(self):
    return self.forename
  
  def get_surname(self):
    return self.surname
  
  def get_email(self):
    return self.email
  
  def get_salary(self):
    return self.salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)


# The main function will parse arguments. 
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
  
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeeUoB")
  print (" 2. Insert data into EmployeeUoB")
  print (" 3. Select all data into EmployeeUoB")
  print (" 4. Search an employee")
  print (" 5. Update data some records")
  print (" 6. Delete data some records")
  print (" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print ("Invalid Choice")



