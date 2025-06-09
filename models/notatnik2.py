from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

lotniska: list = []

class Pracownik:
    def __init__(self, imie, nazwisko, rola):
        self.imie = imie
        self.nazwisko = nazwisko
        self.rola = rola

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.rola})"

class Lotnisko:
    def __init__(self, name, kod, location):
        self.name = name
        self.kod = kod
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])
        self.pracownicy = []

    selected_airport_idx = None  # Zapamiętuje aktywne lotnisko

    def get_coordinates(self) -> list:
        address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]

def add_airport():
    nazwa = entry_airport_name.get()
    kod = entry_airport_code.get()
    location = entry_airport_name.get()
    lotnisko = Lotnisko(nazwa, kod, location)
    lotniska.append(lotnisko)
    clear_form()
    show_lotniska()

def show_lotniska():
    listbox_airports.delete(0, END)
    for idx, lotnisko in enumerate(lotniska):
        listbox_airports.insert(idx, f"{idx+1}. {lotnisko.name} | {lotnisko.kod}")

def delete_airport():
    idx = listbox_airports.index(ACTIVE)
    lotniska[idx].marker.delete()
    lotniska.pop(idx)
    show_lotniska()
    show_all_employees()

def airport_details():
    global selected_airport_idx
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    selected_airport_idx = idx  # zapamiętaj wybrane lotnisko

    lotnisko = lotniska[idx]
    label_name_val.config(text=lotnisko.name)
    label_code_val.config(text=lotnisko.kod)
    map_widget.set_position(lotnisko.coordinates[0], lotnisko.coordinates[1])
    map_widget.set_zoom(16)
    show_employees_for_airport(idx)


def edit_airport():
    idx = listbox_airports.index(ACTIVE)
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)

    entry_airport_name.insert(0, lotniska[idx].name)
    entry_airport_code.insert(0, lotniska[idx].kod)

    button_add_airport.configure(text="Zapisz", command=lambda: update_airport(idx))

def update_airport(idx):
    name = entry_airport_name.get()
    code = entry_airport_code.get()
    location = entry_airport_name.get()

    lotniska[idx].name = name
    lotniska[idx].kod = code
    lotniska[idx].location = location

    lotniska[idx].marker.delete()
    lotniska[idx].coordinates = lotniska[idx].get_coordinates()
    lotniska[idx].marker = map_widget.set_marker(*lotniska[idx].coordinates)

    button_add_airport.configure(text="Dodaj lotnisko", command=add_airport)
    show_lotniska()
    clear_form()

def clear_form():
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)
    entry_airport_name.focus()

# === Pracownicy ===
def add_employee():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    pracownik = Pracownik(entry_imie.get(), entry_nazwisko.get(), entry_rola.get())
    lotniska[idx].pracownicy.append(pracownik)
    show_employees_for_airport(idx)
    show_all_employees()
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_rola.delete(0, END)


def delete_employee():
    global selected_airport_idx
    idx_employee = listbox_employees.curselection()

    if selected_airport_idx is None or not idx_employee:
        messagebox.showwarning("Błąd", "Wybierz pracownika (i wcześniej lotnisko).")
        return

    idx_employee = idx_employee[0]
    lotniska[selected_airport_idx].pracownicy.pop(idx_employee)

    show_employees_for_airport(selected_airport_idx)
    show_all_employees()




def show_employees_for_airport(idx):
    listbox_employees.delete(0, END)
    for p in lotniska[idx].pracownicy:
        listbox_employees.insert(END, str(p))

def show_all_employees():
    listbox_all_employees.delete(0, END)
    for l in lotniska:
        for p in l.pracownicy:
            listbox_all_employees.insert(END, f"{p} - {l.name}")

def show_employee_map():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]
    map_widget.set_position(*lotnisko.coordinates)
    map_widget.set_zoom(10)
    # Mark employee location with labels (if applicable)
    for p in lotnisko.pracownicy:
        map_widget.set_marker(*lotnisko.coordinates, text=str(p))

from tkinter import messagebox

from tkinter import messagebox

def edit_employee():
    global selected_airport_idx
    idx_employee = listbox_employees.curselection()

    if selected_airport_idx is None or not idx_employee:
        messagebox.showwarning("Błąd", "Wybierz pracownika (i wcześniej lotnisko).")
        return

    idx_employee = idx_employee[0]
    pracownik = lotniska[selected_airport_idx].pracownicy[idx_employee]

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_rola.delete(0, END)

    entry_imie.insert(0, pracownik.imie)
    entry_nazwisko.insert(0, pracownik.nazwisko)
    entry_rola.insert(0, pracownik.rola)

    button_add_employee.config(
        text="Zapisz",
        command=lambda: update_employee(selected_airport_idx, idx_employee)
    )


def update_employee(idx_airport, idx_employee):
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    rola = entry_rola.get()

    pracownik = lotniska[idx_airport].pracownicy[idx_employee]
    pracownik.imie = imie
    pracownik.nazwisko = nazwisko
    pracownik.rola = rola

    show_employees_for_airport(idx_airport)
    show_all_employees()

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_rola.delete(0, END)

    button_add_employee.config(text="Dodaj pracownika", command=add_employee)





def update_employee(idx_airport, idx_employee):
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    rola = entry_rola.get()

    lotniska[idx_airport].pracownicy[idx_employee] = Pracownik(imie, nazwisko, rola)

    show_employees_for_airport(idx_airport)
    show_all_employees()

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_rola.delete(0, END)

    button_add_employee.config(text="Dodaj pracownika", command=add_employee)


def get_selected_airport_index():
    idx = listbox_airports.curselection()
    if not idx:
        return None
    return idx[0]





# === GUI ===
root = Tk()
root.title("System zarządzania siecią lotnisk")
root.geometry("1024x768")

frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)
frame_employees = Frame(root)

frame_list.grid(row=0, column=0, columnspan=2, sticky="nw")
frame_form.grid(row=0, column=2, columnspan=2, sticky="ne")
frame_details.grid(row=1, column=0, columnspan=4, sticky="nw")
frame_employees.grid(row=2, column=0, columnspan=2, sticky="nw")
frame_map.grid(row=3, column=0, columnspan=4)

Label(frame_list, text="Lista lotnisk:").grid(row=0, column=0, columnspan=3)
listbox_airports = Listbox(frame_list, width=50)
listbox_airports.grid(row=1, column=0, columnspan=3)
Button(frame_list, text="Pokaż szczegóły", command=airport_details).grid(row=2, column=0)
Button(frame_list, text="Usuń lotnisko", command=delete_airport).grid(row=2, column=1)
Button(frame_list, text="Edytuj lotnisko", command=edit_airport).grid(row=2, column=2)
Button(frame_employees, text="Edytuj pracownika", command=edit_employee).grid(row=6, column=1, pady=5, sticky=E)


Label(frame_form, text="Dodaj nowe lotnisko").grid(row=0, column=0, columnspan=2)
Label(frame_form, text="Nazwa:").grid(row=1, column=0, sticky=W)
Label(frame_form, text="Kod IATA:").grid(row=2, column=0, sticky=W)

entry_airport_name = Entry(frame_form)
entry_airport_name.grid(row=1, column=1)
entry_airport_code = Entry(frame_form)
entry_airport_code.grid(row=2, column=1)
button_add_airport = Button(frame_form, text="Dodaj lotnisko", command=add_airport)
button_add_airport.grid(row=3, column=1, pady=5)

Label(frame_details, text="Szczegóły lotniska:").grid(row=0, column=0, sticky=W, padx=5)
Label(frame_details, text="Nazwa:").grid(row=1, column=0, sticky=W, padx=5)
label_name_val = Label(frame_details, text="...")
label_name_val.grid(row=1, column=1, sticky=W)
Label(frame_details, text="Kod IATA:").grid(row=1, column=2, sticky=W, padx=5)
label_code_val = Label(frame_details, text="...")
label_code_val.grid(row=1, column=3, sticky=W)

Label(frame_employees, text="Pracownicy wybranego lotniska").grid(row=0, column=0, sticky=W)
listbox_employees = Listbox(frame_employees, width=50)
listbox_employees.grid(row=1, column=0)

Button(frame_employees, text="Usuń pracownika", command=delete_employee).grid(row=6, column=0, pady=5)
Button(frame_employees, text="Edytuj pracownika", command=edit_employee).grid(row=6, column=1, pady=5)

Label(frame_employees, text="Wszyscy pracownicy").grid(row=0, column=1, sticky=W)
listbox_all_employees = Listbox(frame_employees, width=50)
listbox_all_employees.grid(row=1, column=1)

Label(frame_employees, text="Imię:").grid(row=2, column=0, sticky=W)
entry_imie = Entry(frame_employees)
entry_imie.grid(row=2, column=1, sticky=W)

Label(frame_employees, text="Nazwisko:").grid(row=3, column=0, sticky=W)
entry_nazwisko = Entry(frame_employees)
entry_nazwisko.grid(row=3, column=1, sticky=W)

Label(frame_employees, text="Rola:").grid(row=4, column=0, sticky=W)
entry_rola = Entry(frame_employees)
entry_rola.grid(row=4, column=1, sticky=W)

button_add_employee = Button(frame_employees, text="Dodaj pracownika", command=add_employee)
button_add_employee.grid(row=5, column=1, sticky=E)

Button(frame_employees, text="Pokaż pracowników na mapie", command=show_employee_map).grid(row=5, column=0)

map_widget = tkintermapview.TkinterMapView(frame_map, width=1000, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
