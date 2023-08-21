from tkinter import *
from tkinter import messagebox
import random
import pyperclip
BLUE = "#ECF2FF"


# ---------------------------- CLEAR WINDOW ------------------------------- #
def clear_window():
    website_entry.delete(0, END)
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
    # check if all the fields are filled
    if len(website_entry.get()) == 0 or len(email_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        is_ok = messagebox.askokcancel(title=f"{website_entry.get()}", message=f"These are the details you "
                                                                               f"entered:\nEmail: {email_entry.get()} "
                                                                               f"\nPassword: {password_entry.get()} "
                                                                               f"\nDo you want to save?")
        if is_ok:
            with open("password.txt", "a") as file:
                file.write(f"{website_entry.get()} | {email_entry.get()} | {password_entry.get()}\n")
            # clear the fields
            clear_window()
            # create a window popup if successfully write to the file
            messagebox.showinfo("Password Saved", "Password Saved Successfully")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50, bg=BLUE)

# create a canvas
canvas = Canvas(width=200, height=200, bg=BLUE, highlightthickness=0)
logo_image = PhotoImage(file="./images/logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# create website label
website_label = Label(text="Website:", bg=BLUE)
website_label.grid(row=1, column=0)

# create website entry
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

# create email label
email_label = Label(text="Email/Username:", bg=BLUE)
email_label.grid(row=2, column=0)

# create email entry
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "your email address")

# create password label
password_label = Label(text="Password:", bg=BLUE)
password_label.grid(row=3, column=0)

# create password entry
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# create generate button
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)

# create save button
save_button = Button(text="Save Password", width=36, command=save_password)
save_button.grid(row=4, column=1, columnspan=2)
window.mainloop()
