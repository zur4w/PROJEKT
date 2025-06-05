from tkinter import *
import tkintermapview

lotniska: list = []

class Lotnisko:
    def __init__(self, name, kod, location):
        self.name = name
        self.kod = kod
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
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
    location = entry_airport_name.get()  # assuming location comes from the name again

    lotniska[idx].name = name
    lotniska[idx].kod = code
    lotniska[idx].location = location

    # Update coordinates and marker
    lotniska[idx].marker.delete()
    lotniska[idx].coordinates = lotniska[idx].get_coordinates()
    lotniska[idx].marker = map_widget.set_marker(
        lotniska[idx].coordinates[0], lotniska[idx].coordinates[1]
    )

    button_add_airport.configure(text="Dodaj lotnisko", command=add_airport)
    show_lotniska()
    clear_form()




def clear_form():
    entry_airport_name.delete(0, END)
    entry_airport_code.delete(0, END)
    entry_airport_name.focus()


# === GUI ===
root = Tk()
root.title("System zarządzania siecią lotnisk")
root.geometry("1024x768")

# Ramki
frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)

frame_list.grid(row=0, column=0, columnspan=2)
frame_form.grid(row=0, column=2, columnspan=2)
frame_details.grid(row=1, column=0, columnspan=4)
frame_map.grid(row=2, column=0, columnspan=4)

# RAMKA LISTA LOTNISK
Label(frame_list, text="Lista lotnisk:").grid(row=0, column=0, columnspan=3)
listbox_airports = Listbox(frame_list, width=50)
listbox_airports.grid(row=1, column=0, columnspan=3)
Button(frame_list, text="Pokaż szczegóły", command=airport_details).grid(row=2, column=0)
Button(frame_list, text="Usuń lotnisko", command=delete_airport).grid(row=2, column=1)
Button(frame_list, text="Edytuj lotnisko", command=edit_airport).grid(row=2, column=2)

# RAMKA FORMULARZ
Label(frame_form, text="Dodaj nowe lotnisko").grid(row=0, column=0, columnspan=2)
Label(frame_form, text="Nazwa:").grid(row=1, column=0, sticky=W)
Label(frame_form, text="Kod IATA:").grid(row=2, column=0, sticky=W)

entry_airport_name = Entry(frame_form)
entry_airport_name.grid(row=1, column=1)
entry_airport_code = Entry(frame_form)
entry_airport_code.grid(row=2, column=1)


button_add_airport = Button(frame_form, text="Dodaj lotnisko", command=add_airport)
button_add_airport.grid(row=3, column=1, pady=5)

# RAMKA SZCZEGÓŁY
Label(frame_details, text="Szczegóły lotniska:").grid(row=0, column=0, sticky=W, padx=5)

Label(frame_details, text="Nazwa:").grid(row=1, column=0, sticky=W, padx=5)
label_name_val = Label(frame_details, text="...")
label_name_val.grid(row=1, column=1, sticky=W)

Label(frame_details, text="Kod IATA:").grid(row=1, column=2, sticky=W, padx=5)
label_code_val = Label(frame_details, text="...")
label_code_val.grid(row=1, column=3, sticky=W)

# RAMKA MAPA
map_widget = tkintermapview.TkinterMapView(frame_map, width=1000, height=400)
map_widget.set_position(52.0, 19.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()