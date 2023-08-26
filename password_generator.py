from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# Constants
BLUE = "#ECF2FF"
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#E0E0E0"
HEIGHT = 5
FONT = ("Arial", 10,)


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search_website():
    website = website_entry.get().lower()
    try:
        with open("./data/password.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No website found.")
    else:
        matching_websites = []

        # Find matching websites
        for key in data.keys():
            if website in key.lower():
                matching_websites.append(key)

        if matching_websites:
            listbox = Listbox(window, selectmode=SINGLE)
            for website in matching_websites:
                listbox.insert(END, website)
            listbox.grid(row=2, column=1, padx=10, pady=10)

            def on_select(event):
                selected_index = listbox.curselection()
                if selected_index:
                    selected_website = listbox.get(selected_index)
                    listbox.grid_forget()
                    show_website_credentials(selected_website)

            listbox.bind("<<ListboxSelect>>", on_select)

        else:
            messagebox.showinfo(title="Oops", message="No matching websites found.")


# ---------------------------- SHOW CREDENTIALS ------------------------------- #
def show_website_credentials(selected_website):
    try:
        with open("./data/password.json", "r") as data_file:
            data = json.load(data_file)
            website_data = data[selected_website]
            username = website_data.get("username", "")
            email = website_data.get("email", "")
            password = website_data["password"]
            messagebox.showinfo(
                title=selected_website,
                message=f"Username: {username}\nEmail: {email}\nPassword: {password}"
            )
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e))


# ---------------------------- CLEAR WINDOW ------------------------------- #
def clear_window():
    website_entry.delete(0, END)
    username_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    symbols_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    numbers_list = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = letters_list + symbols_list + numbers_list
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().lower()
    email = email_entry.get().lower()
    password = password_entry.get()
    username = username_entry.get().lower()
    new_data = {
        website: {
            "email": email,
            "password": password,
            "username": username
        }
    }

    # check if all the fields are filled
    if len(website) == 0 and len(password) == 0:
        messagebox.showerror(title="Oops", message="The website and password fields cannot be empty.")
    elif len(username) == 0 and len(email) == 0:
        messagebox.showerror(title="Oops", message="The username and email fields cannot be empty at the same time.")
    else:
        is_ok = messagebox.askokcancel(title=f"{website}", message=f"These are the details you have enter: "
                                                                   f"\nUsername: {username} "
                                                                   f"\nEmail: {email} "
                                                                   f"\nPassword: {password} "
                                                                   f"\nDo you want to save?")
        if is_ok:
            try:
                with open("./data/password.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("./data/password.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                if website in data:
                    current_username = data[website]["username"]
                    current_email = data[website]["email"]
                    current_password = data[website]["password"]
                    update_data = messagebox.showwarning(title=f"{website}", message=f"Website already exists. Do you "
                                                                                     f"want "f"to update the "
                                                                                     f"credentials?\nCurrent "
                                                                                     f""f"credentials are: "
                                                                                     f"\nUsername: {current_username} "
                                                                                     f"\nEmail: {current_email} "
                                                                                     f""f"\nPassword: "
                                                                                     f"{current_password}")
                    if update_data:
                        data[website]["username"] = username
                        data[website]["email"] = email
                        data[website]["password"] = password
                        with open("./data/password.json", "w") as file:
                            json.dump(data, file, indent=4)
                        messagebox.showinfo(title=f"{website}", message="Password Updated Successfully")
                    else:
                        messagebox.showinfo(title=f"{website}", message="Not Saved")
                else:
                    data.update(new_data)
                    with open("./data/password.json", "w") as file:
                        json.dump(data, file, indent=4)
                        messagebox.showinfo(title=f"'{website}", message="Password Saved Successfully")
            finally:
                # clear the fields
                clear_window()
        else:
            messagebox.showinfo(title=f"{website}", message="Not Saved")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

# Logo
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
logo_image = PhotoImage(file="./images/logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Labels and Entry Fields
website_label = Label(text="Website:", bg=WHITE, font=FONT)
website_label.grid(row=1, column=0)
website_entry = Entry(width=30, bg=GRAY, font=FONT)
website_entry.grid(row=1, column=1, padx=10, pady=10)
website_entry.focus()

username_label = Label(text="Username:", bg=WHITE, font=FONT)
username_label.grid(row=2, column=0)
username_entry = Entry(width=30, bg=GRAY, font=FONT, )
username_entry.grid(row=2, column=1, padx=10, pady=10)

email_label = Label(text="Email:", bg=WHITE, font=FONT)
email_label.grid(row=3, column=0)
email_entry = Entry(width=30, bg=GRAY, font=FONT, )
email_entry.grid(row=3, column=1, padx=10, pady=10)
email_entry.insert(0, "")

password_label = Label(text="Password:", bg=WHITE, font=FONT)
password_label.grid(row=4, column=0)
password_entry = Entry(width=20, bg=GRAY, font=FONT)
password_entry.grid(row=4, column=1, padx=10, pady=10)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password, font=FONT)
generate_button.grid(row=4, column=2, padx=10, pady=10)

save_button = Button(text="Save Password", command=save_password, font=FONT)
save_button.grid(row=5, column=1, padx=10, pady=10)

search_button = Button(text="Search", command=search_website, font=FONT)
search_button.grid(row=1, column=2, padx=10, pady=10)
clear_button = Button(text="Clear Window", command=clear_window, font=FONT)
clear_button.grid(row=5, column=2, padx=10, pady=10)

window.mainloop()
