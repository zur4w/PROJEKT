import folium


def show_airport(airports_list: list[dict]) -> None:
    for airports in airports_list:
        print(
            f"nazwa: {airports['name']},"
            f"miejscowosc: {airports['location']}, "
            f"szerokosc geograficzna: {airports['latitude']}, {airports['longitude']}")


def show_customer(customers_list: list[dict]) -> None:
    for customer in customers_list:
        print(
            f"Imie kilenta {customer['name']}, "
            f"nazwisko klienta {customer['surname']},"
            f"miejscowosc: {customer['location']}, "
            f"szerokosc geograficzna: {customer['latitude']}, {customer['longitude']}")


def show_employee(employees_list: list[dict]) -> None:
    for employee in employees_list:
        print(
            f"Imie pracownika {employee['name']}, "
            f"nazwisko pracownika {employee['surname']},"
            f"miejscowosc: {employee['location']}, "
            f"szerokosc geograficzna: {employee['latitude']}, {employee['longitude']}")











def add_new_airport(airports: list[dict]) -> None:
    new_name = new_airport = input("Nazwa nowego lotniska: ")
    add_new_location = input("Podaj miejscowość: ")
    coordinates = get_coordinates(add_new_location)

    if coordinates:
        new_latitude, new_longitude = coordinates

    new_airport: dict = {"name": new_name, "location": add_new_location, "latitude": new_latitude,
                         "longitude": new_longitude, "airport": new_airport}
    airports.append(new_airport)


def add_new_customer(customers: list[dict]) -> None:
    new_name: str = input("Nowe imie klienta: ")
    new_surname: str = input("Nowe nazwisko klienta: ")
    add_new_location = input("Podaj miejscowosc: ")
    new_my_airport = input("Wpisz lotnisko, z ktorego uslug korzystasz")


    coordinates = get_coordinates(add_new_location)

    if coordinates:
        new_latitude, new_longitude = coordinates

    new_customer: dict = {"name": new_name, "location": add_new_location, "latitude": new_latitude,
                          "longitude": new_longitude, "surname": new_surname, "airport": new_my_airport}
    customers.append(new_customer)


def add_new_employee(employees_list) -> None:
    new_name: str = input("Nowe imie pracownika: ")
    new_surname: str = input("Nowe nazwisko pracownika: ")
    add_new_location: str = input("Podaj miejscowosc: ")
    new_workplace = input("Wpisz lotnisko, na ktorym pracujesz ")
    coordinates = get_coordinates(add_new_location)


    if coordinates:
        new_latitude, new_longitude = coordinates

    new_employee = {"name": new_name, "location": add_new_location, "latitude": new_latitude,
                    "longitude": new_longitude, "surname": new_surname, "airport": new_workplace}
    employees_list.append(new_employee)




def remove_airport(airports) -> None:
    Jakiego_lotniska_szukasz = input("Jakiego lotniska szukasz: ")
    for airport in airports:
        if airport['name'] == Jakiego_lotniska_szukasz:
            airports.remove(airport)


def remove_customer(customers) -> None:
    Jakiego_klienta_szukasz = input("Jakiego klienta szukasz: ")
    for customer in customers:
        if customer['name'] == Jakiego_klienta_szukasz:
            customers.remove(customer)


def remove_employee(employees) -> None:
    Jakiego_pracownika_szukasz = input("Jakiego pracownika szukasz: ")
    for employee in employees:
        if employee['name'] == Jakiego_pracownika_szukasz:
            employees.remove(employee)
















import requests
from bs4 import BeautifulSoup


def get_coordinates(location):

    url: str = f"https://pl.wikipedia.org/wiki/{location}"
    response = requests.get(url)
    response_html = BeautifulSoup(response.text, "html.parser")
    latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
    longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
    return [latitude, longitude]




