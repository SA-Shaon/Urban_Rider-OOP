import hashlib
from brta import Brta
from vehicles import Car, Cng, Bike
from rider_manager import uber
from random import choice, random, randint
import threading

license_authority = Brta()


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        pwd_encrypted = hashlib.md5(password.encode()).hexdigest()
        already_exists = False
        with open('users.txt', 'r') as file:
            if email in file.read():
                already_exists = True
        file.close()
        if already_exists == False:
            with open('users.txt', 'a') as file:
                file.write(f'{email} {pwd_encrypted}\n')
            file.close()
            # print(self.name, 'user created')

    @staticmethod
    def log_in(email, password):
        stored_password = ''
        with open('users.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if email in line:
                    stored_password = line.split(" ")[1]
        file.close()
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if hashed_password == stored_password:
            print("Valid User")
            return True
        else:
            print("Invalid User")
            return False


class Rider(User):
    def __init__(self, name, email, password, location, balance):
        self.location = location
        self.balance = balance
        self.__trip_history = []
        super().__init__(name, email, password)

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def request_trip(self, destination):
        pass

    def get_trip_history(self):
        return self.__trip_history

    def start_a_trip(self, fare, trip_info):
        print(f"A trip is started for {self.name}")
        self.balance -= fare
        self.__trip_history.append(trip_info)


class Driver(User):
    def __init__(self, name, email, password, location, license):
        self.location = location
        self.license = license_authority.validate_license(email, license)
        self.earning = 0
        self.__trip_history = []
        self.valid_driver = False
        self.vehicle = None
        super().__init__(name, email, password)

    def start_a_trip(self, start, destination, fare, trip_info):
        self.earning += fare
        self.location = destination
        # Start threading
        trip_thread = threading.Thread(
            target=self.vehicle.start_driving, args=(start, destination))
        trip_thread.start()
        # self.vehicle.start_driving(start, destination)
        self.__trip_history.append(trip_info)

    def take_driving_test(self):
        result = license_authority.take_driving_test(self.email)
        if result == False:
            # print("Sorry you failed, try again")
            pass
        else:
            self.license = result
            self.valid_driver = True

    def register_a_vehicle(self, vehicle_type, license_plate, rate):
        if self.valid_driver is True:
            if vehicle_type == 'car':
                self.vehicle = Car(vehicle_type, license_plate, rate, self)
                uber.add_a_vehcile(vehicle_type, self.vehicle)
            elif vehicle_type == 'bike':
                self.vehicle = Bike(
                    vehicle_type, license_plate, rate, self)
                uber.add_a_vehcile(vehicle_type, self.vehicle)
            else:
                self.vehicle = Cng(vehicle_type, license_plate, rate, self)
                uber.add_a_vehcile(vehicle_type, self.vehicle)
        else:
            # print("You are not a valid driver.")
            pass


rider1 = Rider('rider1', 'rider@1.com', '1234', randint(0, 30), 25000)
rider2 = Rider('rider2', 'rider@2.com', '1234', randint(0, 30), 5000)
rider3 = Rider('rider3', 'rider@3.com', '1234', randint(0, 30), 5000)
rider4 = Rider('rider4', 'rider@4.com', '1234', randint(0, 30), 5000)
rider5 = Rider('rider5', 'rider@5.com', '1234', randint(0, 30), 5000)
vehicle_types = ['car', 'bike', 'cng']
for i in range(0, 100):
    driver = Driver(f'driver{i}', f'driver@{i}.com',
                    '1234', randint(0, 30), 5468)
    driver.take_driving_test()
    driver.register_a_vehicle(
        choice(vehicle_types), randint(100, 9999), 90)
uber.find_a_vehicle(rider1, choice(vehicle_types), randint(30, 100))
uber.find_a_vehicle(rider2, choice(vehicle_types), randint(30, 100))
uber.find_a_vehicle(rider3, choice(vehicle_types), randint(30, 100))
uber.find_a_vehicle(rider4, choice(vehicle_types), randint(30, 100))
uber.find_a_vehicle(rider5, choice(vehicle_types), randint(30, 100))
print(rider1.get_trip_history())
print(uber.total_income())
