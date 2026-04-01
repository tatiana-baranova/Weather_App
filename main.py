from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from config import API_KEY

root = Tk()
root['bg'] = '#fafafa'
root.title('Weather')
root.geometry('300x250')
root.resizable(width=False, height=False)

# Поле для міста
cityField = Entry(root, bg='white', font=('Arial', 14))
cityField.pack(pady=10)

# додати placeholder
placeholder = "Enter city name"
cityField.insert(0, placeholder)

def on_entry_click(event):
    if cityField.get() == placeholder:
        cityField.delete(0, "end")
        cityField.config(fg='black')

def on_focusout(event):
    if cityField.get() == '':
        cityField.insert(0, placeholder)
        cityField.config(fg='grey')

cityField.bind('<FocusIn>', on_entry_click)
cityField.bind('<FocusOut>', on_focusout)
# Підпис і іконка погоди
weather_label = Label(root, text="", font=('Arial', 12), bg='#fafafa')
weather_label.pack()

icon_label = Label(root, bg='#fafafa')
icon_label.pack(pady=5)

# Функція отримання погоди
def get_weather():
    city = cityField.get()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city")
        return

    url = 'http://api.weatherapi.com/v1/current.json'
    params = {'key': API_KEY, 'q': city, 'lang': 'en'}

    try:
        data = requests.get(url, params=params).json()
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]

        weather_label.config(text=f"{city}: {temp}°C\n{condition}")

        # іконка
        icon_url = "http:" + data["current"]["condition"]["icon"]
        img_data = requests.get(icon_url).content
        img = Image.open(BytesIO(img_data)).resize((64, 64))
        photo = ImageTk.PhotoImage(img)

        icon_label.config(image=photo)
        icon_label.image = photo

    except:
        messagebox.showerror("Помилка", "Не вдалося отримати погоду")

Button(root, text="Update Weather", command=get_weather, bg='yellow').pack(pady=10)

root.mainloop()