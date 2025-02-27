import os
import time
from datetime import datetime, timedelta

class Car:
    car_database = {}

    def __init__(self, model, condition):
        self.model = model
        self.condition = condition
        self.available = True
        self.return_date = None

    def set_condition(self, new_condition):
        self.condition = new_condition

    def rent(self):
        self.available = False

    def return_car(self):
        self.available = True

    def set_return_date(self, days):
        self.return_date = datetime.now() + timedelta(days=days)

    def show_due_date(self):
        if self.return_date:
            print(f"Due date: {self.return_date.strftime('%Y-%m-%d %I:%M:%S %p')}")
        else:
            print("Due date is not set.")

    def is_available(self):
        return self.available

    def get_model(self):
        return self.model

    def get_condition(self):
        return self.condition

    def get_return_date(self):
        return self.return_date

# Customer class
class Customer:
    customer_database = {}

    def __init__(self, customer_id, customer_record):
        self.id = customer_id
        self.rented_cars = []
        self.fine_due = 0
        self.customer_record = customer_record
        self.name = ""
        self.password = ""
        self.current_bill = 0

    def set_pass(self, password):
        self.password = password

    def get_pass(self):
        return self.password

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_id(self, new_id):
        self.id = new_id

    def set_customer_record(self, new_customer_record):
        self.customer_record = new_customer_record

    def get_id(self):
        return self.id

    def rent_car(self, car):
        if self.customer_record >= 1 and len(self.rented_cars) < 2 and car.is_available():
            self.rented_cars.append(car)
            car.rent()
            car.set_return_date(7)
            print("Car rented successfully!")
            self.save_to_file()
        else:
            if self.customer_record < 0:
                print("Customer Record not enough.")
            elif len(self.rented_cars) >= 2:
                print("You can't rent so many cars.")
            else:
                print("Unable to rent the car. Please check car availability.")

    def return_car(self, car):
        car.return_car()
        self.rented_cars.remove(car)
        current_time = datetime.now()
        rental_duration_weeks = (current_time - (car.get_return_date() - timedelta(days=7))).total_seconds() / (7 * 24 * 60 * 60)
        rental_balance = rental_duration_weeks * 100
        self.current_bill += rental_balance

        if (current_time - car.get_return_date()).total_seconds() > 0:
            self.fine_due += (current_time - car.get_return_date()).total_seconds() / (24 * 60 * 60) * 10
        self.save_to_file()

    def browse_rented_cars(self):
        print("Rented Cars:")
        for car in self.rented_cars:
            print(car.get_model())

    def get_fine_due(self):
        return self.fine_due

    def clear_due(self):
        self.fine_due = 0
        self.save_to_file()

    def clear_bill(self):
        self.current_bill = 0
        self.save_to_file()

    def save_to_file(self):
        with open(f"{self.id}_customer.txt", "w") as file:
            file.write(f"{self.id},{self.customer_record},{self.fine_due}\n")
            for car in self.rented_cars:
                file.write(f"{car.get_model()}\n")

    @staticmethod
    def load_from_file(customer_id):
        try:
            with open(f"{customer_id}_customer.txt", "r") as file:
                lines = file.readlines()
                loaded_id, loaded_customer_record, loaded_fine_due = map(int, lines[0].strip().split(','))
                customer = Customer(loaded_id, loaded_customer_record)
                customer.fine_due = loaded_fine_due
                for line in lines[1:]:
                    car = Car(line.strip(), "Good")
                    customer.rented_cars.append(car)
                return customer
        except FileNotFoundError:
            return None

    @staticmethod
    def add_customer(customer_id, customer):
        Customer.customer_database[customer_id] = customer
        customer.save_to_file()

    @staticmethod
    def delete_customer(customer_id):
        if customer_id in Customer.customer_database:
            del Customer.customer_database[customer_id]
        try:
            os.remove(f"{customer_id}_customer.txt")
        except FileNotFoundError:
            pass

    @staticmethod
    def search_customer(customer_id):
        if customer_id in Customer.customer_database:
            return Customer.customer_database[customer_id]
        loaded_customer = Customer.load_from_file(customer_id)
        if loaded_customer:
            Customer.customer_database[customer_id] = loaded_customer
        return loaded_customer

    def calculate_bill(self):
        return self.current_bill

# Employee Class
class Employee:
    employee_database = {}

    def __init__(self, employee_id, employee_record):
        self.id = employee_id
        self.rented_cars = []
        self.fine_due = 0
        self.employee_record = employee_record
        self.name = ""
        self.password = ""
        self.current_bill = 0

    def set_pass(self, password):
        self.password = password

    def get_pass(self):
        return self.password

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_id(self, new_id):
        self.id = new_id

    def set_employee_record(self, new_employee_record):
        self.employee_record = new_employee_record

    def get_id(self):
        return self.id

    def rent_car(self, car):
        if self.employee_record >= 1 and len(self.rented_cars) < 3 and car.is_available():
            self.rented_cars.append(car)
            car.rent()
            car.set_return_date(7)
            print("Car rented successfully!")
            self.save_to_file()
        else:
            if self.employee_record < 0:
                print("Employee Record not enough.")
            elif len(self.rented_cars) >= 3:
                print("You can't rent so many cars.")
            else:
                print("Unable to rent the car. Please check car availability.")

    def return_car(self, car):
        car.return_car()
        self.rented_cars.remove(car)
        current_time = datetime.now()
        rental_duration_weeks = (current_time - (car.get_return_date() - timedelta(days=7))).total_seconds() / (7 * 24 * 60 * 60)
        rental_balance = rental_duration_weeks * 85
        self.current_bill += rental_balance

        if (current_time - car.get_return_date()).total_seconds() > 0:
            self.fine_due += (current_time - car.get_return_date()).total_seconds() / (24 * 60 * 60) * 10
        self.save_to_file()

    def browse_rented_cars(self):
        print("Rented Cars:")
        for car in self.rented_cars:
            print(f"Model: {car.get_model()}, Condition: {car.get_condition()}")

    def get_fine_due(self):
        return self.fine_due

    def clear_due(self):
        self.fine_due = 0
        self.save_to_file()

    def clear_bill(self):
        self.current_bill = 0

    def save_to_file(self):
        with open(f"{self.id}_employee.txt", "w") as file:
            file.write(f"{self.id},{self.employee_record},{self.fine_due}\n")
            for car in self.rented_cars:
                file.write(f"{car.get_model()}\n")

    @staticmethod
    def load_from_file(employee_id):
        try:
            with open(f"{employee_id}_employee.txt", "r") as file:
                lines = file.readlines()
                loaded_id, loaded_employee_record, loaded_fine_due = map(int, lines[0].strip().split(','))
                employee = Employee(loaded_id, loaded_employee_record)
                employee.fine_due = loaded_fine_due
                for line in lines[1:]:
                    car = Car(line.strip(), "Good")
                    employee.rented_cars.append(car)
                return employee
        except FileNotFoundError:
            return None

    @staticmethod
    def add_employee(employee_id, employee):
        Employee.employee_database[employee_id] = employee
        employee.save_to_file()

    @staticmethod
    def delete_employee(employee_id):
        if employee_id in Employee.employee_database:
            del Employee.employee_database[employee_id]
        try:
            os.remove(f"{employee_id}_employee.txt")
        except FileNotFoundError:
            pass

    @staticmethod
    def search_employee(employee_id):
        if employee_id in Employee.employee_database:
            return Employee.employee_database[employee_id]
        loaded_employee = Employee.load_from_file(employee_id)
        if loaded_employee:
            Employee.employee_database[employee_id] = loaded_employee
        return loaded_employee

    def calculate_bill(self):
        return self.current_bill

# Manager Class
class Manager(Employee):
    def __init__(self, employee_id, employee_record):
        super().__init__(employee_id, employee_record)

    def add_customer(self, customer_id, customer):
        Customer.add_customer(customer_id, customer)

    def update_customer(self, customer_id, customer):
        if customer_id in Customer.customer_database:
            Customer.customer_database[customer_id] = customer
            customer.save_to_file()
        else:
            print(f"Customer with ID {customer_id} not found.")

    def delete_customer(self, customer_id):
        Customer.delete_customer(customer_id)

    def add_employee(self, employee_id, employee):
        Employee.add_employee(employee_id, employee)

    def update_employee(self, employee_id, employee):
        if employee_id in Employee.employee_database:
            Employee.employee_database[employee_id] = employee
            employee.save_to_file()
        else:
            print(f"Employee with ID {employee_id} not found.")

    def delete_employee(self, employee_id):
        Employee.delete_employee(employee_id)

    def add_car(self, cars_set):
        model = input("Enter the model of the car: ")
        condition = input("Enter the condition of the car: ")
        new_car = Car(model, condition)
        cars_set.append(new_car)
        print("Car added successfully.")

    def update_car(self, model, cars_set):
        found = False
        for car in cars_set:
            if car.get_model() == model:
                new_condition = input("Enter the new condition of the car: ")
                car.set_condition(new_condition)
                print("Car updated successfully.")
                found = True
                break
        if not found:
            print("Car not found.")

    def delete_car(self, model, cars_set):
        found = False
        for car in cars_set:
            if car.get_model() == model:
                cars_set.remove(car)
                print("Car deleted successfully.")
                found = True
                break
        if not found:
            print("Car not found.")

    def view_all_cars(self):
        print("All Cars:")
        for model, car in Car.car_database.items():
            print(f"Model: {model}, Condition: {car.get_condition()}")

    def view_rented_cars(self):
        print("Cars Rented:")
        for customer_id, customer in Customer.customer_database.items():
            print(f"User ID: {customer.get_id()}")
            print("Cars rented:")
            for car in customer.get_rented_cars():
                print(f"Model: {car.get_model()}")

def main():
    masterkey = "A"
    cars_set = [
        Car("Toyota", "Good"),
        Car("Honda", "Average"),
        Car("BMW", "Excellent"),
        Car("Ford", "Average"),
        Car("Mercedes", "Good"),
        Car("Audi", "Excellent"),
        Car("Chevrolet", "Good"),
        Car("Lamborghini", "Excellent"),
        Car("Ferrari", "Excellent"),
        Car("Nissan", "Average"),
        Car("Hyundai", "Good"),
        Car("Kia", "Average"),
        Car("Volvo", "Good"),
        Car("Subaru", "Average"),
        Car("Mazda", "Good"),
        Car("Jeep", "Average"),
        Car("Chrysler", "Good"),
        Car("Dodge", "Average"),
        Car("Buick", "Good"),
        Car("Lincoln", "Average"),
        Car("Cadillac", "Good"),
        Car("Acura", "Average"),
        Car("Infiniti", "Good"),
        Car("Land Rover", "Average"),
        Car("Porsche", "Good")
    ]

    for car in cars_set:
        Car.car_database[car.get_model()] = car

    customer1 = Customer(1, 5)
    customer2 = Customer(2, 3)
    customer3 = Customer(3, 4)
    customer4 = Customer(4, 2)
    customer5 = Customer(5, 1)

    customer1.set_name("Aarav")
    customer2.set_name("Aisha")
    customer3.set_name("Dev")
    customer4.set_name("Isha")
    customer5.set_name("Kiran")

    customer1.set_pass("password1")
    customer2.set_pass("password2")
    customer3.set_pass("password3")
    customer4.set_pass("password4")
    customer5.set_pass("password5")

    Customer.add_customer(1, customer1)
    Customer.add_customer(2, customer2)
    Customer.add_customer(3, customer3)
    Customer.add_customer(4, customer4)
    Customer.add_customer(5, customer5)

    employee1 = Employee(101, 5)
    employee2 = Employee(102, 3)
    employee3 = Employee(103, 4)
    employee4 = Employee(104, 2)
    employee5 = Employee(105, 1)

    employee1.set_name("Vikram")
    employee2.set_name("Priya")
    employee3.set_name("Rahul")
    employee4.set_name("Neha")
    employee5.set_name("Amit")

    Employee.add_employee(101, employee1)
    Employee.add_employee(102, employee2)
    Employee.add_employee(103, employee3)
    Employee.add_employee(104, employee4)
    Employee.add_employee(105, employee5)

    employee1.set_pass("password101")
    employee2.set_pass("password102")
    employee3.set_pass("password103")
    employee4.set_pass("password104")
    employee5.set_pass("password105")

    exit_program = False
    while not exit_program:
        print("---------------------------------------------------------------------")
        print("\n\nWelcome to the Car Rental System!\n\n")
        print("1. Press 1 to log in:")
        print("X. Press X to exit and erase the system\n\n\n")
        print("---------------------------------------------------------------------")
        cinput1 = input()

        if cinput1 == '1':
            systemboot = 1
            while systemboot:
                print("---------------------------------------------------------------------")
                print("Login as User or Admin??\n\n")
                print("1. Press 1 to log in as USER:")
                print("2. Press 2 to log in as ADMIN / MANAGER:\n\n")
                print("B. Press B to go back to System Page")
                print("---------------------------------------------------------------------")
                cinput2 = input()

                if cinput2 == '1':
                    print("---------------------------------------------------------------------")
                    print("Enter your user type:\n")
                    print("1. Customer")
                    print("2. Employee")
                    print("Press any other number to go back to Main Menu")
                    print("---------------------------------------------------------------------")
                    usertype = input()

                    if usertype == '1':
                        customer_id = int(input("Dear Customer, Enter your id: "))
                        customer = Customer.search_customer(customer_id)
                        if customer:
                            trypassword = input("Please enter your password: ")
                            if trypassword == customer.get_pass():
                                userbreak = 1
                                while userbreak:
                                    print("---------------------------------------------------------------------")
                                    print("\nYou have been logged in as Customer\n")
                                    print("Press 1 to see all the cars\n")
                                    print("Press 2 to view cars and their due date issued by you\n")
                                    print("Press 3 to check if a car is available for issue or not\n")
                                    print("Press 4 to view bill (only after returning the car) the fine\n")
                                    print("Press 5 to issue a car\n")
                                    print("Press 6 to return a car\n")
                                    print("Press 7 to clear your fine\n")
                                    print("Press 8 to logout\n")
                                    print("---------------------------------------------------------------------")

                                    c = input()

                                    if c == '1':
                                        print("List of all cars:\n")
                                        for car in cars_set:
                                            print(f"Model: {car.get_model()}, Condition: {car.get_condition()}")
                                            if car.is_available():
                                                print(", Available: Yes\n")
                                            else:
                                                print(", Available: No, : ")
                                                car.show_due_date()
                                                print()
                                    elif c == '2':
                                        print("Cars issued by you:\n")
                                        for car in customer.get_rented_cars():
                                            print(f"Model: {car.get_model()}, Condition: {car.get_condition()}")
                                            car.show_due_date()
                                    elif c == '3':
                                        model = input("Enter the model of the car you want to check availability for: ")
                                        found = False
                                        for car in cars_set:
                                            if car.get_model() == model and car.is_available():
                                                found = True
                                                print("Car is available for issue.\n")
                                                break
                                        if not found:
                                            print("Car is not available for issue or does not exist.\n")
                                    elif c == '4':
                                        print(f"Your bill is: ${customer.calculate_bill()}")
                                        print(f"Your fine is: ${customer.get_fine_due()}")
                                    elif c == '5':
                                        chosen_model = input("Enter the model of the car you want to rent: ")
                                        found = False
                                        for car in cars_set:
                                            if car.get_model() == chosen_model and car.is_available():
                                                customer.rent_car(car)
                                                found = True
                                                break
                                        if not found:
                                            print("Sorry, the chosen car is not available for rent.")
                                    elif c == '6':
                                        print("List of cars rented by you:")
                                        for i, car in enumerate(customer.get_rented_cars()):
                                            print(f"{i + 1}. Model: {car.get_model()}, Condition: {car.get_condition()}")
                                        choice = input("Enter the number corresponding to the car you want to return (or 0 to cancel): ")
                                        if choice.isdigit() and 1 <= int(choice) <= len(customer.get_rented_cars()):
                                            chosen_car = customer.get_rented_cars()[int(choice) - 1]
                                            customer.return_car(chosen_car)
                                            print("Car returned successfully.")
                                        elif choice != '0':
                                            print("Invalid choice.")
                                    elif c == '7':
                                        print(f"Your current fine due is: ${customer.get_fine_due()}")
                                        print(f"Your current bill due is: ${customer.calculate_bill()}")
                                        choice = input("Do you want to clear your fine & bill? (1 for Yes, 2 for No): ")
                                        if choice == '1':
                                            customer.clear_due()
                                            customer.clear_bill()
                                            print("Fine cleared successfully.\n")
                                        elif choice == '2':
                                            print("Fine not cleared.\n")
                                        else:
                                            print("Invalid choice.\n")
                                    elif c == '8':
                                        print("---------------------------------------------------------------------")
                                        print("Logging Out\n")
                                        print("Thanks Customer\n")
                                        print("---------------------------------------------------------------------")
                                        userbreak = False
                                    else:
                                        print("---------------------------------------------------------------------")
                                        print("Invalid choice. Please try again.\n")
                                        print("---------------------------------------------------------------------")
                            else:
                                print("---------------------------------------------------------------------")
                                print("Wrong PASSWORD\n")
                                print("---------------------------------------------------------------------")
                                continue
                        else:
                            print("---------------------------------------------------------------------")
                            print("User ID doesn't exist\n")
                            print("---------------------------------------------------------------------")
                            continue

                    elif usertype == '2':
                        employee_id = int(input("Dear employee, Enter your id: "))
                        employee = Employee.search_employee(employee_id)
                        if employee:
                            trypassword = input("Please enter your password: ")
                            if trypassword == employee.get_pass():
                                print("---------------------------------------------------------------------")
                                print("CORRECT PASSWORD\n")
                                print("---------------------------------------------------------------------")
                                userbreak = 1
                                while userbreak:
                                    print("---------------------------------------------------------------------")
                                    print("\nYou have been logged in as employee\n")
                                    print("Press 1 to see all the cars\n")
                                    print("Press 2 to view cars and their due date issued by you\n")
                                    print("Press 3 to check if a car is available for issue or not\n")
                                    print("Press 4 to view the bill (only after returning the car) and fine\n")
                                    print("Press 5 to issue a car\n")
                                    print("Press 6 to return a car\n")
                                    print("Press 7 to clear your fine\n")
                                    print("Press 8 to logout\n")
                                    print("---------------------------------------------------------------------")

                                    c = input()

                                    if c == '1':
                                        print("List of all cars:\n")
                                        for car in cars_set:
                                            print(f"Model: {car.get_model()}, Condition: {car.get_condition()}")
                                            if car.is_available():
                                                print(", Available: Yes\n")
                                            else:
                                                print(", Available: No,: ")
                                                car.show_due_date()
                                                print()
                                    elif c == '2':
                                        print("Cars issued by you:\n")
                                        for car in employee.get_rented_cars():
                                            print(f"Model: {car.get_model()}, Condition: {car.get_condition()}")
                                            car.show_due_date()
                                    elif c == '3':
                                        model = input("Enter the model of the car you want to check availability for: ")
                                        found = False
                                        for car in cars_set:
                                            if car.get_model() == model and car.is_available():
                                                found = True
                                                print("Car is available for issue.\n")
                                                break
                                        if not found:
                                            print("Car is not available for issue or does not exist.\n")
                                    elif c == '4':
                                        print(f"Your bill is: ${employee.calculate_bill()}")
                                        print(f"Your fine is: ${employee.get_fine_due()}")
                                    elif c == '5':
                                        chosen_model = input("Enter the model of the car you want to rent: ")
                                        found = False
                                        for car in cars_set:
                                            if car.get_model() == chosen_model and car.is_available():
                                                employee.rent_car(car)
                                                found = True
                                                break
                                        if not found:
                                            print("Sorry, the chosen car is not available for rent.")
                                    elif c == '6':
                                        print("List of cars rented by you:")
                                        for i, car in enumerate(employee.get_rented_cars()):
                                            print(f"{i + 1}. Model: {car.get_model()}, Condition: {car.get_condition()}")
                                        choice = input("Enter the number corresponding to the car you want to return (or 0 to cancel): ")
                                        if choice.isdigit() and 1 <= int(choice) <= len(employee.get_rented_cars()):
                                            chosen_car = employee.get_rented_cars()[int(choice) - 1]
                                            employee.return_car(chosen_car)
                                            print("Car returned successfully.")
                                        elif choice != '0':
                                            print("Invalid choice.")
                                    elif c == '7':
                                        print(f"Your current fine due is: ${employee.get_fine_due()}")
                                        print(f"Your current bill due is: ${employee.calculate_bill()}")
                                        choice = input("Do you want to clear your fine & bill? (1 for Yes, 2 for No): ")
                                        if choice == '1':
                                            employee.clear_due()
                                            employee.clear_bill()
                                            print("Fine cleared successfully.\n")
                                        elif choice == '2':
                                            print("Fine not cleared.\n")
                                        else:
                                            print("Invalid choice.\n")
                                    elif c == '8':
                                        print("---------------------------------------------------------------------")
                                        print("Logging Out\n")
                                        print("Thanks employee\n")
                                        print("---------------------------------------------------------------------")
                                        userbreak = False
                                    else:
                                        print("Invalid choice. Please try again.\n")
                            else:
                                print("---------------------------------------------------------------------")
                                print("Wrong PASSWORD\n")
                                print("---------------------------------------------------------------------")
                                continue
                        else:
                            print("---------------------------------------------------------------------")
                            print("User ID doesn't exist\n")
                            print("---------------------------------------------------------------------")
                            continue

                    else:
                        print("---------------------------------------------------------------------")
                        print("\n\n Wrong Input ; Directing to Login Page\n\n")
                        print("---------------------------------------------------------------------")
                        continue

                elif cinput2 == '2':
                    master_attempt = input("Enter manager password: ")
                    if master_attempt == masterkey:
                        print("---------------------------------------------------------------------")
                        print(" WELCOME MANAGER ;)")
                        print("---------------------------------------------------------------------")
                        adminbreak = 1
                        while adminbreak:
                            print("*********************************************************************")
                            print("\nWelcome! You are logged in as manager.\n\n")
                            print("Press 1 to add a user\n")
                            print("Press 2 to update a user\n")
                            print("Press 3 to delete a user\n")
                            print("Press 4 to add a car\n")
                            print("Press 5 to update a car\n")
                            print("Press 6 to delete a car\n")
                            print("Press 7 to see all cars issued to a particular user\n")
                            print("Press 8 to see the entire LIST in which car is issued to which user\n")
                            print("Press 9 to VIEW all users , their id, name and their passwords\n")
                            print("Press 0 to VIEW all cars\n")
                            print("Press d to show due date of a car\n")
                            print("Press l to logout\n")
                            print("*********************************************************************")
                            c = input()

                            if c == '1':
                                user_type = input("Enter your user type:\n1. Customer\n2. Employee\n")
                                if user_type == '1':
                                    customer_id = int(input("Enter customer ID: "))
                                    if Customer.search_customer(customer_id) is not None:
                                        print(f"Customer with ID {customer_id} already exists.")
                                    else:
                                        customer_name = input("Enter customer Name: ")
                                        customer_record = int(input("Enter customer record: (Rating of User { Range : 0 - 5 } )"))
                                        new_customer = Customer(customer_id, customer_record)
                                        new_customer.set_name(customer_name)
                                        password = input("Enter password for the customer: ")
                                        new_customer.set_pass(password)
                                        Customer.add_customer(customer_id, new_customer)
                                        print("Customer added successfully.")
                                elif user_type == '2':
                                    employee_id = int(input("Enter Employee ID: "))
                                    if Employee.search_employee(employee_id) is not None:
                                        print(f"Employee with ID {employee_id} already exists.")
                                    else:
                                        employee_name = input("Enter Employee Name: ")
                                        employee_record = int(input("Enter Employee record: (Rating of User { Range : 0 - 5 } )"))
                                        new_employee = Employee(employee_id, employee_record)
                                        new_employee.set_name(employee_name)
                                        password = input("Enter password for the employee: ")
                                        new_employee.set_pass(password)
                                        Employee.add_employee(employee_id, new_employee)
                                        print("Employee added successfully.")
                                else:
                                    print("Invalid user type.")
                            elif c == '2':
                                user_type = input("Enter your user type:\n1. Customer\n2. Employee\n")
                                user_id = int(input("Enter the ID of the user you want to update: "))
                                if user_type == '1':
                                    customer = Customer.search_customer(user_id)
                                    if customer:
                                        change_break = 1
                                        while change_break:
                                            print("*********************************************************************")
                                            print("\nWhat Do you want to change/update ?.\n\n")
                                            print("1. Change Name\n")
                                            print("2. Change Customer Record / Rating\n")
                                            print("3. Change Customer Password\n")
                                            print("4. Nothing / Go Back \n")
                                            print("*********************************************************************")
                                            c1 = input()
                                            if c1 == '1':
                                                new_name = input("Enter new name: ")
                                                customer.set_name(new_name)
                                            elif c1 == '2':
                                                new_customer_record = int(input("Enter new customer record: "))
                                                customer.set_customer_record(new_customer_record)
                                            elif c1 == '3':
                                                new_password = input("Enter new password: ")
                                                customer.set_pass(new_password)
                                            elif c1 == '4':
                                                change_break = False
                                            else:
                                                print("Invalid choice. Please try again.")
                                        print("User details updated successfully.")
                                        customer.save_to_file()
                                    else:
                                        print(f"User with ID {user_id} not found.")
                                elif user_type == '2':
                                    employee = Employee.search_employee(user_id)
                                    if employee:
                                        change_break = 1
                                        while change_break:
                                            print("*********************************************************************")
                                            print("\nWhat Do you want to change/update ?.\n\n")
                                            print("1. Change Name\n")
                                            print("2. Change Employee Record / Rating\n")
                                            print("3. Change Employee Password\n")
                                            print("4. Nothing\n")
                                            print("*********************************************************************")
                                            c1 = input()
                                            if c1 == '1':
                                                new_name = input("Enter new name: ")
                                                employee.set_name(new_name)
                                            elif c1 == '2':
                                                new_employee_record = int(input("Enter new Employee record: "))
                                                employee.set_employee_record(new_employee_record)
                                            elif c1 == '3':
                                                new_password = input("Enter new password: ")
                                                employee.set_pass(new_password)
                                            elif c1 == '4':
                                                change_break = False
                                            else:
                                                print("Invalid choice. Please try again.")
                                        print("User details updated successfully.")
                                        employee.save_to_file()
                                    else:
                                        print(f"User with ID {user_id} not found.")
                                else:
                                    print("Invalid user type.")
                            elif c == '3':
                                user_type = input("Enter your delete user type:\n1. Customer\n2. Employee\n")
                                delete_id = int(input("Enter the ID of the user you want to delete: "))
                                if user_type == '1':
                                    customer = Customer.search_customer(delete_id)
                                    if customer:
                                        Customer.delete_customer(delete_id)
                                        print(f"Customer with ID {delete_id} deleted successfully.")
                                    else:
                                        print("Customer not found.")
                                elif user_type == '2':
                                    employee = Employee.search_employee(delete_id)
                                    if employee:
                                        Employee.delete_employee(delete_id)
                                        print(f"Employee with ID {delete_id} deleted successfully.")
                                    else:
                                        print("Employee not found.")
                                else:
                                    print("Invalid user type.")
                            elif c == '4':
                                model = input("Enter the model of the car: ")
                                condition = input("Enter the condition of the car: ")
                                new_car = Car(model, condition)
                                cars_set.append(new_car)
                                print("Car added successfully.")
                            elif c == '5':
                                model = input("Enter the model of the car to update: ")
                                found = False
                                for car in cars_set:
                                    if car.get_model() == model:
                                        new_condition = input("Enter the new condition of the car: ")
                                        car.set_condition(new_condition)
                                        print("Car updated successfully.")
                                        found = True
                                        break
                                if not found:
                                    print("Car not found.")
                            elif c == '6':
                                model = input("Enter the model of the car to delete: ")
                                found = False
                                for car in cars_set:
                                    if car.get_model() == model:
                                        cars_set.remove(car)
                                        print("Car deleted successfully.")
                                        found = True
                                        break
                                if not found:
                                    print("Car not found.")
                            elif c == '7':
                                user_type = input("Enter your user type:\n1. Customer\n2. Employee\n")
                                user_id = int(input("Enter your user ID: "))
                                if user_type == '1':
                                    customer = Customer.search_customer(user_id)
                                    if customer:
                                        customer.browse_rented_cars()
                                    else:
                                        print("Customer not found.")
                                elif user_type == '2':
                                    employee = Employee.search_employee(user_id)
                                    if employee:
                                        employee.browse_rented_cars()
                                    else:
                                        print("Employee not found.")
                                else:
                                    print("Invalid user type.")
                            elif c == '8':
                                print("Cars issued to users:")
                                for customer_id, customer in Customer.customer_database.items():
                                    print(f"User ID: {customer.get_id()}")
                                    print(f"User Name: {customer.get_name()}")
                                    print("Cars rented:")
                                    for car in customer.get_rented_cars():
                                        print(f"Model: {car.get_model()}")
                                    print()
                                for employee_id, employee in Employee.employee_database.items():
                                    print(f"User ID: {employee.get_id()}")
                                    print(f"User Name: {employee.get_name()}")
                                    print("Cars rented:")
                                    for car in employee.get_rented_cars():
                                        print(f"Model: {car.get_model()}")
                                    print()
                            elif c == '9':
                                print("List of all users with their information:")
                                for customer_id, customer in Customer.customer_database.items():
                                    print(f"User ID: {customer_id}, Name: {customer.get_name()}, Password: {customer.get_pass()}")
                                for employee_id, employee in Employee.employee_database.items():
                                    print(f"User ID: {employee_id}, Name: {employee.get_name()}, Password: {employee.get_pass()}")
                            elif c == '0':
                                print("List of all cars:")
                                for car in cars_set:
                                    print(f"Model: {car.get_model()}, Condition: {car.get_condition()}")
                                    if car.is_available():
                                        print(", Available: Yes\n")
                                    else:
                                        print(", Available: No : ")
                                        car.show_due_date()
                                        print()
                            elif c == 'd':
                                model = input("Enter the model of the car: ")
                                found = False
                                for car in cars_set:
                                    if car.get_model() == model:
                                        found = True
                                        print(f"Due date for car {model}: ")
                                        car.show_due_date()
                                        print()
                                        break
                                if not found:
                                    print("You have not rented a car with that model.")
                            elif c == 'l':
                                adminbreak = False
                            else:
                                print("Invalid choice. Please try again.")
                    else:
                        print("---------------------------------------------------------------------")
                        print("\n\n Wrong Password ; Directing to Login Page\n\n")
                        print("---------------------------------------------------------------------")
                        continue

                elif cinput2 == 'B':
                    print("\n\n Directing to System Page\n\n")
                    break
                else:
                    print("---------------------------------------------------------------------")
                    print("\n\n Wrong Input in Login Page\n\n")
                    print("---------------------------------------------------------------------")
                    continue

        elif cinput1 == 'X':
            print("---------------------------------------------------------------------")
            exit_program = True
            print("\n\nProgram Exited")
            print("Thanks :)\n\n")
            print("---------------------------------------------------------------------")
            break
        else:
            print("---------------------------------------------------------------------")
            print("\n\n Wrong Input in System Page\n\n")
            print("---------------------------------------------------------------------")
            continue

if __name__ == "__main__":
    main()
    
