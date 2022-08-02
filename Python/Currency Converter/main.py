import requests
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

URL = "https://api.exchangerate-api.com/v4/latest/USD"


# Classes

class Converter:
    def __init__(self):
        self.data = requests.get(URL).json()
        self.rates = self.data["rates"]

    def convert(self, base_currency, currency_to_convert, amount):
        return float(amount) * 1 / float(self.rates[base_currency]) * float(self.rates[currency_to_convert])

    def get_currencies(self) -> list:
        return [currency for currency in self.rates.keys()]

    def get_correct_time(self):
        epoch_time = self.data["time_last_updated"]
        date_time = datetime.fromtimestamp(epoch_time)
        return date_time


class ConversionData:
    def __init__(self):
        self.convert_from = base_currencies.get()
        self.convert_to = target_currencies.get()
        self.amount_to_convert = amount_input.get()


# Helper functions

def get_conversion_data():
    conv_data = ConversionData()
    return conv_data


def result():
    result_text.config(state="normal")
    if result_text.get("1.0", END):
        result_text.delete("0.0", END)
    data = get_conversion_data()
    try:
        if float(data.amount_to_convert) > 0:
            result_text.insert(END, str(converter.convert(data.convert_from, data.convert_to, data.amount_to_convert)))
        else:
            messagebox.showerror("Error", "Amount must be greater than 0")

    except ValueError:
        messagebox.showerror("Unexpected Error", "Amount must be numbers only")
    result_text.config(state="disabled")
    return


def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(result_text.get("1.0", END))
    window.update()  # now it stays on the clipboard after the window is closed
    return


# GUI

converter = Converter()
window = Tk()
window.geometry('580x250', )
window.title("Currency Converter")
window.resizable(False, False)

amount_label = Label(window, text="Amount to Convert")
amount_label.grid(row=0, column=1)
amount_input = Entry(window)
amount_input.grid(row=1, column=1)

base_label = Label(window, text="Base Currency")
base_label.grid(row=1, column=0)

target_currency_label = Label(window, text="Convert To")
target_currency_label.grid(row=1, column=2)

base_currency_var = StringVar(window)
target_currency = StringVar(window)

base_currencies = ttk.Combobox(window, textvariable=base_currency_var)
base_currencies["values"] = converter.get_currencies()
base_currencies["state"] = "readonly"
base_currencies.grid(row=2, column=0, padx=10)

target_currencies = ttk.Combobox(window, textvariable=target_currency)
target_currencies["values"] = converter.get_currencies()
target_currencies["state"] = "readonly"
target_currencies.grid(row=2, column=2)

result_label = Label(window, text="Result")
result_label.grid(row=4, column=1)

result_var = Variable()
result_text = Text(window, height=1, width=25, state="disabled")
result_text.grid(row=5, column=1)

btn = Button(window, text='Submit', command=result, width=20, bg='blue', fg='white')
btn.grid(row=3, column=1)

copy = Button(window, text="Copy to Clipboard", command=copy_to_clipboard, width=20, bg="white", fg="black")
copy.grid(row=7, column=1)

accurate_label = Label(window, text=f"Results are correct as of {converter.get_correct_time()} UTC")
accurate_label.grid(row=6, column=1)

if __name__ == "__main__":
    window.mainloop()
