from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# Lista lotnisk
lotniska = []

class Pracownik:
    def __init__(self, imie, nazwisko):
        self.imie = imie
        self.nazwisko = nazwisko
    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Lotnisko:
    def __init__(self, name, kod, wiki_location):
        self.name = name
        self.kod = kod
        self.wiki_location = wiki_location
        self.coordinates = self.get_coordinates()
        self.marker = None
        self.pracownicy = []

    def get_coordinates(self):
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.wiki_location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            # Pobranie drugiego wystąpienia współrzędnych
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except Exception as e:
            print("Błąd pobierania współrzędnych:", e)
            # Domyślne współrzędne (Warszawa)
            return [52.2297, 21.0122]

# --- FUNKCJE LOTNISKA ---
def add_airport():
    name = entry_airport_name.get().strip()
    kod = entry_airport_code.get().strip()
    wiki_location = entry_airport_location.get().strip()

    if not name or not kod or not wiki_location:
        return

    lotnisko = Lotnisko(name, kod, wiki_location)
    # Dodaj marker na mapie
    lotnisko.marker = map_widget.set_marker(lotnisko.coordinates[0], lotnisko.coordinates[1], text=f"{lotnisko.name} ({lotnisko.kod})")
    lotniska.append(lotnisko)

    clear_airport_form()
    show_lotniska()

def show_lotniska():
    listbox_airports.delete(0, END)
    for idx, lotnisko in enumerate(lotniska):
        listbox_airports.insert(END, f"{idx+1}. {lotnisko.name} | {lotnisko.kod}")

def delete_airport():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    # Usuń marker z mapy
    if lotniska[idx].marker:
        lotniska[idx].marker.delete()
    lotniska.pop(idx)
    show_lotniska()
    clear_employees_list()
    clear_airport_details()

def edit_airport():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]
    entry_airport_name.delete(0, END)
    entry_airport_name.insert(0, lotnisko.name)
    entry_airport_code.delete(0, END)
    entry_airport_code.insert(0, lotnisko.kod)
    entry_airport_location.delete(0, END)
    entry_airport_location.insert(0, lotnisko.wiki_location)
    button_add_airport.config(text="Zapisz zmiany", command=lambda: update_airport(idx))

def update_airport(idx):
    name = entry_airport_name.get().strip()
    kod = entry_airport_code.get().strip()
    wiki_location = entry_airport_location.get().strip()

    if not name or not kod or not wiki_location:
        return

    lotnisko = lotniska[idx]

    # Usuń stary marker
    if lotnisko.marker:
        lotnisko.marker.delete()

    lotnisko.name = name
    lotnisko.kod = kod
    lotnisko.wiki_location = wiki_location
    lotnisko.coordinates = lotnisko.get_coordinates()
    lotnisko.marker = map_widget.set_marker(lotnisko.coordinates[0], lotnisko.coordinates[1], text=f"{lotnisko.name} ({lotnisko.kod})")

    button_add_airport.config(text="Dodaj lotnisko", command=add_airport)
    clear_airport_form()
    show_lotniska()

def clear_airport_form():
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)
    entry_airport_location.delete(0, END)

def airport_details(event=None):
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]

    label_name_val.config(text=lotnisko.name)
    label_code_val.config(text=lotnisko.kod)
    label_location_val.config(text=lotnisko.wiki_location)

    map_widget.set_position(lotnisko.coordinates[0], lotnisko.coordinates[1])
    map_widget.set_zoom(13)

    show_employees(lotnisko)

# --- FUNKCJE PRACOWNICY ---
def add_employee():
    idx = listbox_airports.curselection()
    if not idx:
        from tkinter import messagebox
        messagebox.showwarning("Brak lotniska", "Wybierz lotnisko, aby dodać pracownika.")
        return
    idx = idx[0]
    lotnisko = lotniska[idx]

    imie = entry_name.get().strip()
    nazwisko = entry_surname.get().strip()

    if not imie or not nazwisko:
        messagebox.showwarning("Niepełne dane", "Wpisz imię i nazwisko pracownika.")
        return

    pracownik = Pracownik(imie, nazwisko)
    lotnisko.pracownicy.append(pracownik)
    show_employees(lotnisko)
    clear_employee_form()

def show_employees(lotnisko):
    listbox_employees.delete(0, END)
    for p in lotnisko.pracownicy:
        listbox_employees.insert(END, f"{p.imie} {p.nazwisko}")

def clear_employees_list():
    listbox_employees.delete(0, END)

def clear_employee_form():
    entry_name.delete(0, END)
    entry_surname.delete(0, END)

def delete_employee():
    airport_idx = listbox_airports.curselection()
    emp_idx = listbox_employees.curselection()
    if not airport_idx or not emp_idx:
        return
    airport_idx = airport_idx[0]
    emp_idx = emp_idx[0]
    lotnisko = lotniska[airport_idx]
    lotnisko.pracownicy.pop(emp_idx)
    show_employees(lotnisko)

def edit_employee():
    airport_idx = listbox_airports.curselection()
    emp_idx = listbox_employees.curselection()
    if not airport_idx or not emp_idx:
        return
    airport_idx = airport_idx[0]
    emp_idx = emp_idx[0]
    lotnisko = lotniska[airport_idx]
    pracownik = lotnisko.pracownicy[emp_idx]

    entry_name.delete(0, END)
    entry_name.insert(0, pracownik.imie)
    entry_surname.delete(0, END)
    entry_surname.insert(0, pracownik.nazwisko)

    button_add_employee.config(text="Zapisz zmiany", command=lambda: update_employee(airport_idx, emp_idx))

def update_employee(airport_idx, emp_idx):
    lotnisko = lotniska[airport_idx]

    imie = entry_name.get().strip()
    nazwisko = entry_surname.get().strip()

    if not imie or not nazwisko:
        return

    lotnisko.pracownicy[emp_idx].imie = imie
    lotnisko.pracownicy[emp_idx].nazwisko = nazwisko

    show_employees(lotnisko)
    clear_employee_form()
    button_add_employee.config(text="Dodaj pracownika", command=add_employee)

def show_employees_on_map():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]

    map_widget.set_position(lotnisko.coordinates[0], lotnisko.coordinates[1])
    map_widget.set_zoom(13)

    # Usuń wszystkie markery oprócz lotniska
    map_widget.delete_all_marker()
    lotnisko.marker = map_widget.set_marker(lotnisko.coordinates[0], lotnisko.coordinates[1], text=f"{lotnisko.name} ({lotnisko.kod})")

    # Dodaj markery pracowników (z lekkim przesunięciem)
    offset = 0.001
    for i, pracownik in enumerate(lotnisko.pracownicy):
        lat = lotnisko.coordinates[0] + (offset * (i + 1))
        lon = lotnisko.coordinates[1] + (offset * (i + 1))
        map_widget.set_marker(lat, lon, text=f"{pracownik.imie} {pracownik.nazwisko}")

# --- UI ---

root = Tk()
root.title("Zarządzanie lotniskami i pracownikami")
root.geometry("1024x900")

# Ramki
frame_list = Frame(root)
frame_form_airport = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)
frame_form_employee = Frame(root)

frame_list.grid(row=0, column=0, columnspan=2, pady=10)
frame_form_airport.grid(row=0, column=2, columnspan=2, padx=10)
frame_details.grid(row=1, column=0, columnspan=4, sticky=W, pady=10)
frame_map.grid(row=2, column=0, columnspan=4)
frame_form_employee.grid(row=3, column=0, columnspan=4, pady=10)

# Lista lotnisk
Label(frame_list, text="Lista lotnisk:").grid(row=0, column=0, columnspan=3)
listbox_airports = Listbox(frame_list, width=50, height=10)
listbox_airports.grid(row=1, column=0, columnspan=3)
listbox_airports.bind("<<ListboxSelect>>", airport_details)

Button(frame_list, text="Pokaż szczegóły", command=airport_details).grid(row=2, column=0)
Button(frame_list, text="Usuń lotnisko", command=delete_airport).grid(row=2, column=1)
Button(frame_list, text="Edytuj lotnisko", command=edit_airport).grid(row=2, column=2)

# Formularz lotnisko
Label(frame_form_airport, text="Dodaj / Edytuj lotnisko").grid(row=0, column=0, columnspan=2)

Label(frame_form_airport, text="Nazwa:").grid(row=1, column=0, sticky=E)
entry_airport_name = Entry(frame_form_airport, width=30)
entry_airport_name.grid(row=1, column=1)

Label(frame_form_airport, text="Kod IATA:").grid(row=2, column=0, sticky=E)
entry_airport_code = Entry(frame_form_airport, width=30)
entry_airport_code.grid(row=2, column=1)

Label(frame_form_airport, text="Nazwa do Wikipedii:").grid(row=3, column=0, sticky=E)
entry_airport_location = Entry(frame_form_airport, width=30)
entry_airport_location.grid(row=3, column=1)

button_add_airport = Button(frame_form_airport, text="Dodaj lotnisko", command=add_airport)
button_add_airport.grid(row=4, column=1, pady=10)

# Szczegóły lotniska
Label(frame_details, text="Szczegóły lotniska:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W, padx=5, pady=5)

Label(frame_details, text="Nazwa:").grid(row=1, column=0, sticky=W, padx=5)
label_name_val = Label(frame_details, text="...")
label_name_val.grid(row=1, column=1, sticky=W)

Label(frame_details, text="Kod IATA:").grid(row=1, column=2, sticky=W, padx=5)
label_code_val = Label(frame_details, text="...")
label_code_val.grid(row=1, column=3, sticky=W)

Label(frame_details, text="Nazwa Wikipedii:").grid(row=1, column=4, sticky=W, padx=5)
label_location_val = Label(frame_details, text="...")
label_location_val.grid(row=1, column=5, sticky=W)

# Lista pracowników
Label(frame_details, text="Pracownicy lotniska:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=W, padx=5, pady=5)

listbox_employees = Listbox(frame_details, width=50, height=8)
listbox_employees.grid(row=3, column=0, columnspan=3, padx=5)

Button(frame_details, text="Usuń pracownika", command=delete_employee).grid(row=4, column=0, pady=5)
Button(frame_details, text="Edytuj pracownika", command=edit_employee).grid(row=4, column=1, pady=5)
Button(frame_details, text="Pokaż pracowników na mapie", command=show_employees_on_map).grid(row=4, column=2, pady=5)

# Formularz pracownika
Label(frame_form_employee, text="Dodaj / Edytuj pracownika").grid(row=0, column=0, columnspan=4)

Label(frame_form_employee, text="Imię:").grid(row=1, column=0, sticky=E)
entry_name = Entry(frame_form_employee, width=30)
entry_name.grid(row=1, column=1)

Label(frame_form_employee, text="Nazwisko:").grid(row=1, column=2, sticky=E)
entry_surname = Entry(frame_form_employee, width=30)
entry_surname.grid(row=1, column=3)

button_add_employee = Button(frame_form_employee, text="Dodaj pracownika", command=add_employee)
button_add_employee.grid(row=2, column=3, pady=10)

# Mapa
map_widget = tkintermapview.TkinterMapView(frame_map, width=1000, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
