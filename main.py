from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup


lotniska = []

class Pracownik:
    def __init__(self, imie, nazwisko, funkcja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.funkcja = funkcja

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.funkcja})"

class Klient:
    def __init__(self, imie, nazwisko, kierunek_podrozy):
        self.imie = imie
        self.nazwisko = nazwisko
        self.kierunek_podrozy = kierunek_podrozy
        self.coordinates = []

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.kierunek_podrozy})"

class Lotnisko:
    def __init__(self, name, kod, location):
        self.name = name
        self.kod = kod
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)
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
        except Exception:
            return None  # brak lokalizacji = brak markera


# FUNKCJE DLA LOTNISK

def add_airport():
    nazwa = entry_airport_name.get()
    kod = entry_airport_code.get()
    location = nazwa
    lotnisko = Lotnisko(nazwa, kod, location)
    lotniska.append(lotnisko)
    clear_form()
    show_lotniska()


def clear_form():
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)
    entry_airport_name.focus()


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

def show_all_airports_map():
    markers = [{"coords": l.coordinates, "label": l.name} for l in lotniska]
    show_map_with_markers("Mapa wszystkich lotnisk", markers)


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

    lotnisko.name = entry_airport_name.get()
    lotnisko.kod = entry_airport_code.get()

    lotnisko.marker.text = lotnisko.name
    label_name_val.config(text=lotnisko.name)
    label_code_val.config(text=lotnisko.kod)
    show_lotniska()


#FUNKCJE DLA PRACOWNIKÓW

def add_employee():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    pracownik = Pracownik(entry_imie.get(), entry_nazwisko.get(), entry_rola.get())
    lotniska[idx].pracownicy.append(pracownik)
    show_employees_for_airport(idx)


def delete_employee():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_employee = listbox_employees.index(ACTIVE)
    if idx_airport < len(lotniska) and idx_employee < len(lotniska[idx_airport].pracownicy):
        del lotniska[idx_airport].pracownicy[idx_employee]
        show_employees_for_airport(idx_airport)


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

    label_details_imie.config(text=emp.imie)
    label_details_nazwisko.config(text=emp.nazwisko)
    label_details_rola.config(text=emp.rola)


def save_employee():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_employee = listbox_employees.curselection()
    if not idx_employee or idx_airport >= len(lotniska):
        return
    lotniska[idx_airport].pracownicy[idx_employee[0]] = Pracownik(entry_imie.get(), entry_nazwisko.get(),
                                                                  entry_rola.get())
    show_employees_for_airport(idx_airport)


def show_employees_filtered():
    listbox_employees.delete(0, END)
    if var_filter.get() == 1:  # Wszyscy pracownicy
        for lotnisko in lotniska:
            for p in lotnisko.pracownicy:
                listbox_employees.insert(END, str(p))
    elif var_filter.get() == 2:  # Pracownicy z danego lotniska
        if listbox_airports.curselection():
            idx = listbox_airports.curselection()[0]
            show_employees_for_airport(idx)


def show_employees_for_airport(idx):
    listbox_employees.delete(0, END)
    for p in lotniska[idx].pracownicy:
        listbox_employees.insert(END, str(p))


def show_employee_map_window():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]
    if not lotnisko.pracownicy:
        return
    label = "\n".join(str(p) for p in lotnisko.pracownicy)
    markers = [{"coords": lotnisko.coordinates, "label": label}]
    show_map_with_markers("Pracownicy lotniska", markers)


def show_all_employees_map():
    markers = []
    for lotnisko in lotniska:
        if not lotnisko.pracownicy:
            continue
        label = "\n".join(str(pracownik) for pracownik in lotnisko.pracownicy)
        markers.append({"coords": lotnisko.coordinates, "label": label})
    if markers:
        show_map_with_markers("Mapa wszystkich pracowników", markers)


# FUNKCJE DLA KLIENTÓW

def add_client():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    klient = Klient(entry_client_imie.get(), entry_client_nazwisko.get(), entry_client_typ.get())
    klient.coordinates = lotniska[idx].coordinates
    lotniska[idx].klienci.append(klient)
    show_clients_for_airport(idx)


def delete_client():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_client = listbox_clients.index(ACTIVE)
    if idx_airport < len(lotniska) and idx_client < len(lotniska[idx_airport].klienci):
        del lotniska[idx_airport].klienci[idx_client]
        show_clients_for_airport(idx_airport)


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

    label_client_imie.config(text=klient.imie)
    label_client_nazwisko.config(text=klient.nazwisko)
    label_client_typ.config(text=klient.typ)


def save_client():
    idx_airport = listbox_airports.index(ACTIVE)
    idx_client = listbox_clients.curselection()
    if not idx_client or idx_airport >= len(lotniska):
        return
    lotniska[idx_airport].klienci[idx_client[0]] = Klient(entry_client_imie.get(), entry_client_nazwisko.get(),
                                                          entry_client_typ.get())
    lotniska[idx_airport].klienci[idx_client[0]].coordinates = lotniska[idx_airport].coordinates
    show_clients_for_airport(idx_airport)


def show_clients_filtered():
    listbox_clients.delete(0, END)
    if var_client_filter.get() == 1:  # Wszyscy klienci
        for lotnisko in lotniska:
            for k in lotnisko.klienci:
                listbox_clients.insert(END, str(k))
    elif var_client_filter.get() == 2:  # Klienci z danego lotniska
        if listbox_airports.curselection():
            idx = listbox_airports.curselection()[0]
            show_clients_for_airport(idx)


def show_clients_for_airport(idx):
    listbox_clients.delete(0, END)
    for k in lotniska[idx].klienci:
        listbox_clients.insert(END, str(k))


def show_clients_map():
    idx = listbox_airports.curselection()
    if not idx:
        return
    idx = idx[0]
    lotnisko = lotniska[idx]
    if not lotnisko.klienci:
        return
    label = "\n".join(str(k) for k in lotnisko.klienci)
    markers = [{"coords": lotnisko.coordinates, "label": label}]
    show_map_with_markers("Klienci lotniska", markers)


def show_all_clients_map():
    markers = []
    for lotnisko in lotniska:
        if not lotnisko.klienci:
            continue
        label = "\n".join(str(klient) for klient in lotnisko.klienci)
        markers.append({"coords": lotnisko.coordinates, "label": label})
    if markers:
        show_map_with_markers("Mapa wszystkich klientów", markers)


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



root = Tk()
root.title("System zarządzania lotniskami")
root.geometry("1200x900")

main_frame = Frame(root)
main_frame.pack()

# --- LOTNISKA  ---
frame_list = Frame(main_frame)
frame_list.pack(side=LEFT, padx=10, pady=10)

Label(frame_list, text="Lista lotnisk", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")

listbox_airports = Listbox(frame_list, width=40, height=10)
listbox_airports.grid(row=1, column=0, rowspan=4)

# Przyciski pod listą
Button(frame_list, text="Pokaż szczegóły", command=airport_details).grid(row=5, column=0, sticky="w", pady=2)
Button(frame_list, text="Usuń lotnisko", command=delete_airport).grid(row=5, column=0, sticky="e", pady=2)
Button(frame_list, text="Edytuj lotnisko", command=edit_airport).grid(row=6, column=0, pady=2)

# Formularz edycji i dodawania
Label(frame_list, text="Formularz edycji i dodawania:").grid(row=1, column=1, sticky="w")

Label(frame_list, text="Nazwa lotniska").grid(row=2, column=1, sticky="w")
entry_airport_name = Entry(frame_list)
entry_airport_name.grid(row=3, column=1, padx=5, pady=2)

Label(frame_list, text="Kod IATA").grid(row=4, column=1, sticky="w")
entry_airport_code = Entry(frame_list)
entry_airport_code.grid(row=5, column=1, padx=5, pady=2)

Button(frame_list, text="Dodaj lotnisko", command=add_airport).grid(row=6, column=1, pady=2)
Button(frame_list, text="Zapisz zmiany", command=save_airport).grid(row=7, column=1, pady=2)

# Szczegóły lotniska
Label(frame_list, text="Szczegóły lotniska:", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=2, pady=(10, 0))
Label(frame_list, text="Nazwa:").grid(row=9, column=0, sticky="w")
label_name_val = Label(frame_list, text="---")
label_name_val.grid(row=9, column=1, sticky="w")
Label(frame_list, text="Kod IATA:").grid(row=10, column=0, sticky="w")
label_code_val = Label(frame_list, text="---")
label_code_val.grid(row=10, column=1, sticky="w")


# --- PRACOWNICY  ---
frame_employees = Frame(main_frame)
frame_employees.pack(side=LEFT, padx=10, pady=10)

Label(frame_employees, text="Lista pracowników lotnisk", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", columnspan=2)

Label(frame_employees, text="Wybierz formułę wyświetlania pracowników").grid(row=1, column=0, columnspan=3)

var_filter = IntVar()
Radiobutton(frame_employees, text="Wszyscy pracownicy", variable=var_filter, value=1).grid(row=2, column=0, columnspan=3, sticky="w")
Radiobutton(frame_employees, text="Pracownicy z danego lotniska", variable=var_filter, value=2).grid(row=3, column=0, columnspan=3, sticky="w")

Button(frame_employees, text="Pokaż zaznaczone", command=show_employees_filtered).grid(row=4, column=0, columnspan=3, pady=(0, 5))

listbox_employees = Listbox(frame_employees, width=40, height=10)
listbox_employees.grid(row=5, column=0, columnspan=3)

Button(frame_employees, text="Pokaż dane pracownika", command=edit_employee).grid(row=6, column=0, pady=2)
Button(frame_employees, text="Usuń pracownika", command=delete_employee).grid(row=6, column=1, pady=2)
Button(frame_employees, text="Edytuj pracownika", command=edit_employee).grid(row=6, column=2, pady=2)

# Mapy pracowników
Button(frame_employees, text="Mapa pracowników", command=show_employee_map_window).grid(row=7, column=0, pady=2, sticky="w")
Button(frame_employees, text="Mapa wszystkich pracowników", command=show_all_employees_map).grid(row=7, column=1, pady=2, sticky="e")


# Formularz edycji
Label(frame_employees, text="Formularz edycji i dodawania:").grid(row=8, column=0, columnspan=3, sticky="w")

Label(frame_employees, text="Imię").grid(row=9, column=0, sticky="w")
entry_imie = Entry(frame_employees)
entry_imie.grid(row=9, column=1, columnspan=2, pady=2, sticky="we")

Label(frame_employees, text="Nazwisko").grid(row=10, column=0, sticky="w")
entry_nazwisko = Entry(frame_employees)
entry_nazwisko.grid(row=10, column=1, columnspan=2, pady=2, sticky="we")

Label(frame_employees, text="Funkcja").grid(row=11, column=0, sticky="w")
label_details_imie = Label(frame_employees, text="---")
label_details_imie.grid(row=16, column=0)

label_details_nazwisko = Label(frame_employees, text="---")
label_details_nazwisko.grid(row=16, column=1)

label_details_rola = Label(frame_employees, text="---")
label_details_rola.grid(row=16, column=2)

entry_rola = Entry(frame_employees)
entry_rola.grid(row=11, column=1, columnspan=2, pady=2, sticky="we")

Button(frame_employees, text="Dodaj pracownika", command=add_employee).grid(row=12, column=0, columnspan=3, pady=5)
Button(frame_employees, text="Zapisz zmiany", command=save_employee).grid(row=13, column=0, columnspan=3, pady=5)

# Szczegóły pracownika
Label(frame_employees, text="Szczegóły pracowników:", font=("Arial", 10, "bold")).grid(row=14, column=0, columnspan=3)
Label(frame_employees, text="Imię").grid(row=15, column=0)
Label(frame_employees, text="Nazwisko").grid(row=15, column=1)
Label(frame_employees, text="Funkcja").grid(row=15, column=2)


# --- KLIENCI ---
frame_clients = Frame(main_frame)
frame_clients.pack(side=LEFT, padx=10, pady=10)

Label(frame_clients, text="Lista klientów lotnisk", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", columnspan=2)

Label(frame_clients, text="Wybierz formułę wyświetlania klientów").grid(row=1, column=0, columnspan=3)

var_client_filter = IntVar()
Radiobutton(frame_clients, text="Wszyscy klienci", variable=var_client_filter, value=1).grid(row=2, column=0, columnspan=3, sticky="w")
Radiobutton(frame_clients, text="Klienci z danego lotniska", variable=var_client_filter, value=2).grid(row=3, column=0, columnspan=3, sticky="w")

Button(frame_clients, text="Pokaż zaznaczone", command=show_clients_filtered).grid(row=4, column=0, columnspan=3, pady=(0, 5))

listbox_clients = Listbox(frame_clients, width=40, height=10)
listbox_clients.grid(row=5, column=0, columnspan=3)

Button(frame_clients, text="Pokaż dane klienta", command=edit_client).grid(row=6, column=0, pady=2)
Button(frame_clients, text="Usuń klienta", command=delete_client).grid(row=6, column=1, pady=2)
Button(frame_clients, text="Edytuj klienta", command=edit_client).grid(row=6, column=2, pady=2)

# Mapy klientów
Button(frame_clients, text="Mapa klientów", command=show_clients_map).grid(row=7, column=0, pady=2, sticky="w")
Button(frame_clients, text="Mapa wszystkich klientów", command=show_all_clients_map).grid(row=7, column=1, pady=2, sticky="e")


# Formularz edycji
Label(frame_clients, text="Formularz edycji i dodawania:").grid(row=8, column=0, columnspan=3, sticky="w")

Label(frame_clients, text="Imię").grid(row=9, column=0, sticky="w")
entry_client_imie = Entry(frame_clients)
entry_client_imie.grid(row=9, column=1, columnspan=2, pady=2, sticky="we")

Label(frame_clients, text="Nazwisko").grid(row=10, column=0, sticky="w")
entry_client_nazwisko = Entry(frame_clients)
entry_client_nazwisko.grid(row=10, column=1, columnspan=2, pady=2, sticky="we")

Label(frame_clients, text="Kierunek podróży").grid(row=11, column=0, sticky="w")
entry_client_typ = Entry(frame_clients)
entry_client_typ.grid(row=11, column=1, columnspan=2, pady=2, sticky="we")
label_client_imie = Label(frame_clients, text="---")
label_client_imie.grid(row=16, column=0)

label_client_nazwisko = Label(frame_clients, text="---")
label_client_nazwisko.grid(row=16, column=1)

label_client_typ = Label(frame_clients, text="---")
label_client_typ.grid(row=16, column=2)


Button(frame_clients, text="Dodaj klienta", command=add_client).grid(row=12, column=0, columnspan=3, pady=5)
Button(frame_clients, text="Zapisz zmiany", command=save_client).grid(row=13, column=0, columnspan=3, pady=5)

# Szczegóły klienta
Label(frame_clients, text="Szczegóły klientów:", font=("Arial", 10, "bold")).grid(row=14, column=0, columnspan=3)
Label(frame_clients, text="Imię").grid(row=15, column=0)
Label(frame_clients, text="Nazwisko").grid(row=15, column=1)
Label(frame_clients, text="Kierunek").grid(row=15, column=2)

# --- MAPA ---

map_widget = tkintermapview.TkinterMapView(root, width=1100, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.pack(pady=5)

root.mainloop()