READ ME

This program main.py is a car rental management system implemented in python3. It provides functionality for managing cars, customers, and employees within a rental service.

IMPORTANT NOTES:
The password of the manager/admin is A ( Just Capital A ).
The password of the all the initial employees and customer are like password#{n} where n is the user ID.
For example , Password for Customer with userid=1 is "password1".
similarly password for employee with userid=102 is "password102".
Rating would be from -5 to 5. Depending on the conditions of the car and timely return.
If there is some error with password or name of a user , the user should contact the admin to fix or change his details.

IMPORTANT FUNCTIONALITIES:
You need to run the code simultaneously.
**If you log out of system and erase the files ; the files would be new the next time you would write . It would be from start , with initial 5 employees and 5 customers as predefined.**
New txt files will be added if you add new users.
Txt files will be deleted if you delete existing users.
The Bill for customer is with no discount ; while for employee is with 15% discount.
Manager is only 1 , but class has been made properly for the manager.(It was not defined properly in the Problem Statement leading to confusion)

The number of total cars allowed to rent is 3 for employees and 2 for customers.

The customer and employee record/ rating should be >= 1 to obtain a car , else they will not be able to rent cars.




1. Classes:
   - Car: Represents a car available for rental. It includes attributes such as model, condition, availability, and return date. The class provides methods for setting conditions, renting, returning, and managing return dates.

   - Customer: Represents a customer who can rent cars. It includes attributes such as ID, rented cars, fine due, customer record, name, and password. This class provides methods for renting, returning, browsing rented cars, managing dues, saving to/loading from files, and more.

   - Employee: Represents an employee who can rent cars. It has similar attributes and functionalities as the Customer class but with a higher limit on the number of cars that can be rented.
     
   - Manager: Derived from the Employee class, this class adds additional functionalities for managing customers, employees, and cars.

2. Functionality:
   - The program allows the creation, updating, and deletion of customers, employees, and cars.
   - Customers and employees can rent cars, and the system manages due dates, fines, and bills accordingly.
   - Managers have additional capabilities to manage customers, employees, and cars.

3. Usage:
   - The main() function initializes car, customer, and employee objects, adds them to respective databases, and demonstrates some functionalities.
   - Customers and employees are added to their respective databases using the addCustomer() and addEmployee() methods of the corresponding classes.
   - Cars are added to the carDatabase using the addCar() method of the Manager class.
   - Renting and returning cars are demonstrated using the rentCar() and returnCar() methods of the Customer and Employee classes.
   - The program also provides functionalities to browse rented cars, view all cars, and view rented cars, which are demonstrated in the main() function.

4. Additional Notes:
   - Error handling and user input validation are minimal in this code and can be further enhanced for robustness.
   - The program utilizes file I/O for saving and loading data. Each customer and employee is associated with a text file for data storage.
   - The program demonstrates basic object-oriented principles such as inheritance and polymorphism.

5. Requirements:
   - Requires pytohn3
   - Standard Python libraries used:
       os → File operations
       datetime → Managing due dates

6. Execution:
   - **Run the Python script using a Python interpreter to execute the program.**
