from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

lotniska = []

class Pracownik:
    def __init__(self, imie, nazwisko, rola):
        self.imie = imie
        self.nazwisko = nazwisko
        self.rola = rola

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.rola})"

class Klient:
    def __init__(self, imie, nazwisko, typ):
        self.imie = imie
        self.nazwisko = nazwisko
        self.typ = typ
        self.coordinates = []

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.typ})"

class Lotnisko:
    def __init__(self, name, kod, location):
        self.name = name
        self.kod = kod
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])
        self.pracownicy = []
        self.klienci = []

    def get_coordinates(self):
        try:
            address_url = f"https://pl.wikipedia.org/wiki/{self.location}"
            response = requests.get(address_url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [52.0, 19.0]

def clear_form():
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)
    entry_airport_name.focus()

def add_airport():
    nazwa = entry_airport_name.get()
    kod = entry_airport_code.get()
    location = nazwa
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

def airport_details():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]
    label_name_val.config(text=lotnisko.name)
    label_code_val.config(text=lotnisko.kod)
    map_widget.set_position(lotnisko.coordinates[0], lotnisko.coordinates[1])
    map_widget.set_zoom(16)
    show_employees_for_airport(idx)
    show_clients_for_airport(idx)

def add_employee():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    pracownik = Pracownik(entry_imie.get(), entry_nazwisko.get(), entry_rola.get())
    lotniska[idx].pracownicy.append(pracownik)
    show_employees_for_airport(idx)

def show_employees_for_airport(idx):
    listbox_employees.delete(0, END)
    for p in lotniska[idx].pracownicy:
        listbox_employees.insert(END, str(p))

def delete_employee():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_employee = listbox_employees.index(ACTIVE)
    if idx_airport < len(lotniska) and idx_employee < len(lotniska[idx_airport].pracownicy):
        del lotniska[idx_airport].pracownicy[idx_employee]
        show_employees_for_airport(idx_airport)

def add_client():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    klient = Klient(entry_client_imie.get(), entry_client_nazwisko.get(), entry_client_typ.get())
    klient.coordinates = lotniska[idx].coordinates
    lotniska[idx].klienci.append(klient)
    show_clients_for_airport(idx)

def show_clients_for_airport(idx):
    listbox_clients.delete(0, END)
    for k in lotniska[idx].klienci:
        listbox_clients.insert(END, str(k))

def delete_client():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_client = listbox_clients.index(ACTIVE)
    if idx_airport < len(lotniska) and idx_client < len(lotniska[idx_airport].klienci):
        del lotniska[idx_airport].klienci[idx_client]
        show_clients_for_airport(idx_airport)

def show_map_with_markers(title, markers):
    new_window = Toplevel(root)
    new_window.title(title)
    map_view = tkintermapview.TkinterMapView(new_window, width=800, height=600)
    map_view.pack()
    map_view.set_zoom(5)
    for m in markers:
        map_view.set_marker(*m["coords"], text=m["label"])
    if markers:
        map_view.set_position(*markers[0]["coords"])

def show_all_airports_map():
    markers = [{"coords": l.coordinates, "label": l.name} for l in lotniska]
    show_map_with_markers("Mapa wszystkich lotnisk", markers)

def show_all_clients_map():
    markers = []
    for l in lotniska:
        for k in l.klienci:
            markers.append({"coords": k.coordinates, "label": str(k)})
    show_map_with_markers("Mapa wszystkich klientów", markers)

def show_clients_map():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    markers = [{"coords": k.coordinates, "label": str(k)} for k in lotniska[idx].klienci]
    show_map_with_markers("Klienci lotniska", markers)

def show_employee_map_window():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    markers = [{"coords": lotniska[idx].coordinates, "label": str(p)} for p in lotniska[idx].pracownicy]
    show_map_with_markers("Pracownicy lotniska", markers)

root = Tk()
root.title("System zarządzania lotniskami")
root.geometry("1024x900")

frame_list = Frame(root)
frame_list.pack()
Label(frame_list, text="Lista lotnisk").pack()
listbox_airports = Listbox(frame_list, width=50)
listbox_airports.pack()
Button(frame_list, text="Pokaż szczegóły", command=airport_details).pack()
Button(frame_list, text="Usuń lotnisko", command=delete_airport).pack()
Button(frame_list, text="Mapa lotnisk", command=show_all_airports_map).pack()
Button(frame_list, text="Mapa wszystkich klientów", command=show_all_clients_map).pack()

entry_airport_name = Entry(frame_list)
entry_airport_name.pack()
entry_airport_code = Entry(frame_list)
entry_airport_code.pack()
Button(frame_list, text="Dodaj lotnisko", command=add_airport).pack()

label_name_val = Label(root, text="...")
label_name_val.pack()
label_code_val = Label(root, text="...")
label_code_val.pack()

frame_employees = Frame(root)
frame_employees.grid(row=2, column=0, columnspan=4, pady=10)

Label(frame_employees, text="Pracownicy lotniska").grid(row=0, column=0, columnspan=2, sticky=W)
listbox_employees = Listbox(frame_employees, width=40, height=5)
listbox_employees.grid(row=1, column=0, columnspan=2)
Label(frame_employees, text="Imię:").grid(row=2, column=0, sticky=E)
entry_imie = Entry(frame_employees)
entry_imie.grid(row=2, column=1)
Label(frame_employees, text="Nazwisko:").grid(row=3, column=0, sticky=E)
entry_nazwisko = Entry(frame_employees)
entry_nazwisko.grid(row=3, column=1)
Label(frame_employees, text="Rola:").grid(row=4, column=0, sticky=E)
entry_rola = Entry(frame_employees)
entry_rola.grid(row=4, column=1)
Button(frame_employees, text="Dodaj", command=add_employee).grid(row=5, column=1, sticky=E)
Button(frame_employees, text="Usuń", command=delete_employee).grid(row=5, column=0, sticky=W)
Button(frame_employees, text="Mapa", command=show_employee_map_window).grid(row=6, column=0, columnspan=2)

Label(frame_employees, text="Klienci lotniska").grid(row=0, column=2, columnspan=2, sticky=W)
listbox_clients = Listbox(frame_employees, width=40, height=5)
listbox_clients.grid(row=1, column=2, columnspan=2)
Label(frame_employees, text="Imię:").grid(row=2, column=2, sticky=E)
entry_client_imie = Entry(frame_employees)
entry_client_imie.grid(row=2, column=3)
Label(frame_employees, text="Nazwisko:").grid(row=3, column=2, sticky=E)
entry_client_nazwisko = Entry(frame_employees)
entry_client_nazwisko.grid(row=3, column=3)
Label(frame_employees, text="Typ:").grid(row=4, column=2, sticky=E)
entry_client_typ = Entry(frame_employees)
entry_client_typ.grid(row=4, column=3)
Button(frame_employees, text="Dodaj", command=add_client).grid(row=5, column=3, sticky=E)
Button(frame_employees, text="Usuń", command=delete_client).grid(row=5, column=2, sticky=W)
Button(frame_employees, text="Mapa", command=show_clients_map).grid(row=6, column=2, columnspan=2)

map_widget = tkintermapview.TkinterMapView(root, width=1000, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()