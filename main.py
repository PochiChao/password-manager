from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pass_let = [random.choice(letters) for _ in range(nr_letters)]
    pass_sym = [random.choice(symbols) for _ in range(nr_symbols)]
    pass_num = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = pass_let + pass_sym + pass_num

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title='Warning', message='Please enter a website name to search for its password.')
    else:
        try:
            with open('data.json', mode='r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title='No Data File Found', message='There are no saved passwords yet.')
        else:
            if website in data:
                emailuser = data[website]['email']
                password = data[website]['password']
                messagebox.showinfo(title='Result Found', message=f'email/user:\n {emailuser}\npassword:\n{password}')
            else:
                messagebox.showinfo(title='No Website Password Found', message='Website password not found.')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_to_bank():
    website = website_entry.get()
    emailuser = emailuser_entry.get()
    password = password_entry.get()
    new_data = {website:
                    {'email': emailuser,
                     'password': password}
                }

    any_empty = len(website) == 0 or len(password) == 0
    if any_empty:
        messagebox.showinfo(title='Warning', message='Please do not leave any fields empty!')
    else:
        try:
            with open('data.json', mode='r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', mode='w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open('data.json', mode='w') as data_file:
                json.dump(data, data_file, indent=4)
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
bg_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=bg_img)
canvas.grid(row=0, column=1)

website_text = Label(text='Website:')
website_text.grid(row=1, column=0, sticky='EW')
emailuser_text = Label(text='Email/Username:')
emailuser_text.grid(row=2, column=0, sticky='EW')
password_text = Label(text='Password:')
password_text.grid(row=3, column=0, sticky='EW')

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky='EW')
emailuser_entry = Entry(width=35)
emailuser_entry.grid(row=2, column=1, columnspan=2, sticky='EW')
emailuser_entry.insert(END, '19pochi94@gmail.com')
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky='EW')

search_button = Button(width=10, text='Search', command=search)
search_button.grid(column=2, row=1)
gen_button = Button(width=10, text='Generate', command=generate)
gen_button.grid(row=3, column=2)

add_button = Button(width=36, text='Add', command=add_to_bank)
add_button.grid(row=4, column=1, columnspan=2, sticky='EW')

window.mainloop()
