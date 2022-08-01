import tkinter, json
from tkinter import messagebox
from tkinter import filedialog
import random
import os
import pandas

# --------- PASSWORD GENERATOR ---------- #
directory = os.getcwd()
global new_data

#Creates a random password with provided characters that have 8-10 letter, 2-4 symbols and 2-4 numbers
def generate_password():
    password_entry.delete(0, tkinter.END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password_generated = ""
    for char in password_list:
        password_generated += char
    password_entry.insert(0, password_generated)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_info():
    global new_data
    filename = "data"
    suffix = ".json"
    path = os.path.join(directory, filename + suffix)

    website = website_entry.get()
    email = user_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password
    }}


    if website == "" or password == "":
        messagebox.showerror(title="Field error", message="Some required fields are empty")
    else:
        try:
            with open(path, "r") as file:
                # reading old data
                json_data = json.load(file)

        except FileNotFoundError:
                with open(path, "w") as file:
                    json.dump(new_data, file, indent=4)

        else:
            # updating old data with new data
            json_data.update(new_data)
            messagebox.showinfo(message=f"Information saved for {website}")

            #saving updated data
            with open("data.json", "w") as file:
                json.dump(json_data, file, indent=4)

        finally:
            website_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)


def file_dialog():
    global directory
    directory = tkinter.filedialog.askdirectory()

#Show saved data for website if website exists
def search_for_website():
    website = website_entry.get()
    pandas_data = pandas.read_json("data.json")
    df = pandas.DataFrame(pandas_data)
    try:
        email = df.at["email", website]
        password = df.at["password", website]
    except KeyError:
        messagebox.showerror(message="Please type website name!")

    messagebox.showinfo(message=f"Website:{website}\nEmail:{email}\nPassword:{password}")

# ------- UI SETUP ------- #
window = tkinter.Tk()
window.title("Password manager")
window.config(padx=44, pady=44)


canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
padlock_img = tkinter.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0)

# ------------Labels
website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)

user_label = tkinter.Label(text="Email/Username:")
user_label.grid(row=2, column=0)

password_label = tkinter.Label(text="Password:")
password_label.grid(row=3, column=0)

# ------------Entries

website_entry = tkinter.Entry(width=38)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus() ##focused on start

user_entry = tkinter.Entry(width=38)
user_entry.insert(0, "dobretheo@gmail.com") ##field already inserted
user_entry.grid(column=1, row=2, columnspan=2)

password_entry = tkinter.Entry(width=38)
password_entry.grid(column=1, row=3, columnspan=2)

# -----------Buttons
generate_button = tkinter.Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = tkinter.Button(text="Add", width=33, command=add_info)
add_button.grid(column=1, row=4, columnspan=2)

browse_button = tkinter.Button(text="Browse file location", command=file_dialog, width=33)
browse_button.grid(column=1, row=5, columnspan=2)

search_button = tkinter.Button(text="Search", command=search_for_website, width=10)
search_button.grid(column=2, row=1)

window.mainloop()