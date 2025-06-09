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


# --- Edycja pracownika ---
def edit_employee():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_employee = listbox_employees.curselection()
    if not idx_employee or idx_airport >= len(lotniska):
        return
    emp = lotniska[idx_airport].pracownicy[idx_employee[0]]
    entry_imie.delete(0, END)
    entry_imie.insert(0, emp.imie)
    entry_nazwisko.delete(0, END)
    entry_nazwisko.insert(0, emp.nazwisko)
    entry_rola.delete(0, END)
    entry_rola.insert(0, emp.rola)


def save_employee():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_employee = listbox_employees.curselection()
    if not idx_employee or idx_airport >= len(lotniska):
        return
    lotniska[idx_airport].pracownicy[idx_employee[0]] = Pracownik(
        entry_imie.get(), entry_nazwisko.get(), entry_rola.get()
    )
    show_employees_for_airport(idx_airport)

# --- Edycja klienta ---
def edit_client():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_client = listbox_clients.curselection()
    if not idx_client or idx_airport >= len(lotniska):
        return
    klient = lotniska[idx_airport].klienci[idx_client[0]]
    entry_client_imie.delete(0, END)
    entry_client_imie.insert(0, klient.imie)
    entry_client_nazwisko.delete(0, END)
    entry_client_nazwisko.insert(0, klient.nazwisko)
    entry_client_typ.delete(0, END)
    entry_client_typ.insert(0, klient.typ)

def save_client():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_client = listbox_clients.curselection()
    if not idx_client or idx_airport >= len(lotniska):
        return
    lotniska[idx_airport].klienci[idx_client[0]] = Klient(
        entry_client_imie.get(), entry_client_nazwisko.get(), entry_client_typ.get()
    )
    lotniska[idx_airport].klienci[idx_client[0]].coordinates = lotniska[idx_airport].coordinates
    show_clients_for_airport(idx_airport)


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

def save_airport():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]

    # Zmieniamy dane i odświeżamy marker
    lotnisko.name = entry_airport_name.get()
    lotnisko.kod = entry_airport_code.get()

    # Odśwież etykiety i listę
    lotnisko.marker.text = lotnisko.name
    label_name_val.config(text=lotnisko.name)
    label_code_val.config(text=lotnisko.kod)
    show_lotniska()



root = Tk()
root.title("System zarządzania lotniskami")
root.geometry("1200x900")

main_frame = Frame(root)
main_frame.pack()


# --- Lotniska ---
frame_list = Frame(main_frame)
frame_list.pack(side=LEFT, padx=10, pady=10)

Label(frame_list, text="Lista lotnisk").pack()
listbox_airports = Listbox(frame_list, width=40, height=15)
listbox_airports.pack()

# Najpierw pola tekstowe
Label(frame_list, text="Lotnisko").pack()
entry_airport_name = Entry(frame_list)
entry_airport_name.pack(pady=2)
Label(frame_list, text="Kod IATA").pack()
entry_airport_code = Entry(frame_list)
entry_airport_code.pack(pady=2)

# Następnie przyciski
Button(frame_list, text="Dodaj lotnisko", command=add_airport).pack(pady=2)
Button(frame_list, text="Pokaż szczegóły", command=airport_details).pack(pady=2)
Button(frame_list, text="Usuń lotnisko", command=delete_airport).pack(pady=2)
Button(frame_list, text="Mapa lotnisk", command=show_all_airports_map).pack(pady=2)
Button(frame_list, text="Edytuj lotnisko", command=edit_airport).pack(pady=2)
Button(frame_list, text="Zapisz zmiany", command=save_airport).pack(pady=2)


# --- Pracownicy ---
frame_employees = Frame(main_frame)
frame_employees.pack(side=LEFT, padx=10, pady=10)

Label(frame_employees, text="Pracownicy").pack()
listbox_employees = Listbox(frame_employees, width=40, height=15)
listbox_employees.pack()


Label(frame_employees, text="Imię").pack()
entry_imie = Entry(frame_employees)
entry_imie.pack(pady=2)
Label(frame_employees, text="Nazwisko").pack()
entry_nazwisko = Entry(frame_employees)
entry_nazwisko.pack(pady=2)
Label(frame_employees, text="Funkcja").pack()
entry_rola = Entry(frame_employees)
entry_rola.pack(pady=2)

Button(frame_employees, text="Dodaj pracownika", command=add_employee).pack(pady=2)
Button(frame_employees, text="Usuń pracownika", command=delete_employee).pack(pady=2)
Button(frame_employees, text="Mapa pracowników", command=show_employee_map_window).pack(pady=2)
Button(frame_employees, text="Edytuj pracownika", command=edit_employee).pack(pady=2)
Button(frame_employees, text="Zapisz zmiany", command=save_employee).pack(pady=2)


# --- Klienci ---
frame_clients = Frame(main_frame)
frame_clients.pack(side=LEFT, padx=10, pady=10)

Label(frame_clients, text="Klienci").pack()
listbox_clients = Listbox(frame_clients, width=40, height=15)
listbox_clients.pack()

Label(frame_clients, text="Imię").pack()
entry_client_imie = Entry(frame_clients)
entry_client_imie.pack(pady=2)
Label(frame_clients, text="Nazwisko").pack()
entry_client_nazwisko = Entry(frame_clients)
entry_client_nazwisko.pack(pady=2)
Label(frame_clients, text="Kierunek podróży").pack()
entry_client_typ = Entry(frame_clients)
entry_client_typ.pack(pady=2)

Button(frame_clients, text="Dodaj klienta", command=add_client).pack(pady=2)
Button(frame_clients, text="Usuń klienta", command=delete_client).pack(pady=2)
Button(frame_clients, text="Mapa klientów", command=show_clients_map).pack(pady=2)
Button(frame_clients, text="Edytuj klienta", command=edit_client).pack(pady=2)
Button(frame_clients, text="Zapisz zmiany", command=save_client).pack(pady=2)


# --- Szczegóły i mapa ---
details_frame = Frame(root)
details_frame.pack(pady=5)

label_name_val = Label(details_frame, text="...")
label_name_val.pack()
label_code_val = Label(details_frame, text="...")
label_code_val.pack()

map_widget = tkintermapview.TkinterMapView(root, width=1100, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.pack(pady=5)


root.mainloop()