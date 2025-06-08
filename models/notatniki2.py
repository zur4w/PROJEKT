from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

lotniska: list = []

class Pracownik:
    def __init__(self, imie, nazwisko, lat, lon):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lat = lat
        self.lon = lon
        self.marker = None

class Klient:
    def __init__(self, imie, nazwisko, lat, lon):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lat = lat
        self.lon = lon
        self.marker = None

class Lotnisko:
    def __init__(self, name, kod, location):
        self.name = name
        self.kod = kod
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])
        self.pracownicy = []
        self.klienci = []

    def get_coordinates(self) -> list:
        address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]

# Airport functions
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
    show_pracownicy(lotnisko)
    show_klienci(lotnisko)

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
    lotniska[idx].marker = map_widget.set_marker(lotniska[idx].coordinates[0], lotniska[idx].coordinates[1])
    button_add_airport.configure(text="Dodaj lotnisko", command=add_airport)
    show_lotniska()
    clear_form()

def clear_form():
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)
    entry_airport_name.focus()

# Employee functions
def add_pracownik():
    idx = listbox_airports.curselection()
    if not idx:
        return
    lotnisko = lotniska[idx[0]]
    imie = entry_emp_imie.get()
    nazwisko = entry_emp_nazwisko.get()
    lat = float(entry_emp_lat.get())
    lon = float(entry_emp_lon.get())
    p = Pracownik(imie, nazwisko, lat, lon)
    p.marker = map_widget.set_marker(lat, lon, text=f"{imie} {nazwisko}")
    lotnisko.pracownicy.append(p)
    show_pracownicy(lotnisko)

def show_pracownicy(lotnisko):
    listbox_emp.delete(0, END)
    for p in lotnisko.pracownicy:
        listbox_emp.insert(END, f"{p.imie} {p.nazwisko} ({p.lat},{p.lon})")

def delete_pracownik():
    idx = listbox_airports.curselection()
    if not idx:
        return
    lotnisko = lotniska[idx[0]]
    idx_p = listbox_emp.curselection()
    if not idx_p:
        return
    pracownik = lotnisko.pracownicy.pop(idx_p[0])
    if pracownik.marker:
        pracownik.marker.delete()
    show_pracownicy(lotnisko)

def add_klient():
    idx = listbox_airports.curselection()
    if not idx:
        return
    lotnisko = lotniska[idx[0]]
    imie = entry_kl_imie.get()
    nazwisko = entry_kl_nazwisko.get()
    lat = float(entry_kl_lat.get())
    lon = float(entry_kl_lon.get())
    k = Klient(imie, nazwisko, lat, lon)
    k.marker = map_widget.set_marker(lat, lon, text=f"{imie} {nazwisko}")
    lotnisko.klienci.append(k)
    show_klienci(lotnisko)

def show_klienci(lotnisko):
    listbox_kl.delete(0, END)
    for k in lotnisko.klienci:
        listbox_kl.insert(END, f"{k.imie} {k.nazwisko} ({k.lat},{k.lon})")

def delete_klient():
    idx = listbox_airports.curselection()
    if not idx:
        return
    lotnisko = lotniska[idx[0]]
    idx_k = listbox_kl.curselection()
    if not idx_k:
        return
    klient = lotnisko.klienci.pop(idx_k[0])
    if klient.marker:
        klient.marker.delete()
    show_klienci(lotnisko)

def mapa_klienci_wszystkich():
    map_widget.set_zoom(6)
    for lotnisko in lotniska:
        for k in lotnisko.klienci:
            if k.marker:
                k.marker.delete()
            k.marker = map_widget.set_marker(k.lat, k.lon, text=f"{k.imie} {k.nazwisko}")

def mapa_pracownicy_lotniska():
    idx = listbox_airports.curselection()
    if not idx:
        return
    lotnisko = lotniska[idx[0]]
    for p in lotnisko.pracownicy:
        if p.marker:
            p.marker.delete()
        p.marker = map_widget.set_marker(p.lat, p.lon, text=f"{p.imie} {p.nazwisko}")

def mapa_klienci_lotniska():
    idx = listbox_airports.curselection()
    if not idx:
        return
    lotnisko = lotniska[idx[0]]
    for k in lotnisko.klienci:
        if k.marker:
            k.marker.delete()
        k.marker = map_widget.set_marker(k.lat, k.lon, text=f"{k.imie} {k.nazwisko}")

# === GUI ===
root = Tk()
root.title("System zarządzania siecią lotnisk")
root.geometry("1024x900")

frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)
frame_emp = Frame(root)
frame_kl = Frame(root)
frame_map_controls = Frame(root)

frame_list.grid(row=0, column=0, columnspan=2)
frame_form.grid(row=0, column=2, columnspan=2)
frame_details.grid(row=1, column=0, columnspan=4)
frame_map.grid(row=2, column=0, columnspan=4)
frame_emp.grid(row=3, column=0, columnspan=2)
frame_kl.grid(row=3, column=2, columnspan=2)
frame_map_controls.grid(row=4, column=0, columnspan=4)

Label(frame_list, text="Lista lotnisk:").grid(row=0, column=0, columnspan=3)
listbox_airports = Listbox(frame_list, width=50)
listbox_airports.grid(row=1, column=0, columnspan=3)
Button(frame_list, text="Pokaż szczegóły", command=airport_details).grid(row=2, column=0)
Button(frame_list, text="Usuń lotnisko", command=delete_airport).grid(row=2, column=1)
Button(frame_list, text="Edytuj lotnisko", command=edit_airport).grid(row=2, column=2)

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

map_widget = tkintermapview.TkinterMapView(frame_map, width=1000, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

Label(frame_emp, text="Pracownicy:").grid(row=0, column=0)
listbox_emp = Listbox(frame_emp, width=50)
listbox_emp.grid(row=1, column=0, columnspan=4)
entry_emp_imie = Entry(frame_emp)
entry_emp_nazwisko = Entry(frame_emp)
entry_emp_lat = Entry(frame_emp)
entry_emp_lon = Entry(frame_emp)
entry_emp_imie.grid(row=2, column=0)
entry_emp_nazwisko.grid(row=2, column=1)
entry_emp_lat.grid(row=2, column=2)
entry_emp_lon.grid(row=2, column=3)
Button(frame_emp, text="Dodaj pracownika", command=add_pracownik).grid(row=3, column=1)
Button(frame_emp, text="Usuń pracownika", command=delete_pracownik).grid(row=3, column=2)

Label(frame_kl, text="Klienci:").grid(row=0, column=0)
listbox_kl = Listbox(frame_kl, width=50)
listbox_kl.grid(row=1, column=0, columnspan=4)
entry_kl_imie = Entry(frame_kl)
entry_kl_nazwisko = Entry(frame_kl)
entry_kl_lat = Entry(frame_kl)
entry_kl_lon = Entry(frame_kl)
entry_kl_imie.grid(row=2, column=0)
entry_kl_nazwisko.grid(row=2, column=1)
entry_kl_lat.grid(row=2, column=2)
entry_kl_lon.grid(row=2, column=3)
Button(frame_kl, text="Dodaj klienta", command=add_klient).grid(row=3, column=1)
Button(frame_kl, text="Usuń klienta", command=delete_klient).grid(row=3, column=2)

Button(frame_map_controls, text="Mapa KL wszystkich", command=mapa_klienci_wszystkich).grid(row=0, column=0)
Button(frame_map_controls, text="Mapa PR wybranego", command=mapa_pracownicy_lotniska).grid(row=0, column=1)
Button(frame_map_controls, text="Mapa KL wybranego", command=mapa_klienci_lotniska).grid(row=0, column=2)

root.mainloop()