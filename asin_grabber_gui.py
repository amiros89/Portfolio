from selenium import webdriver, common
from selenium.webdriver.firefox.options import Options
import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
import csv
from datetime import datetime

NUM_OF_PAGES = 5
global prods

def grab(url, text_box):
    if "https://www.amazon.com/" not in url and "https://www.amzn.com/" not in url:
        mb.showerror(title="Invalid URL", message="Provided URL is not from Amazon. Please try again")
        return
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile(
        "C:\\Users\\Amir\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ojg7rjfs.default-release")
    driver = webdriver.Firefox(executable_path="D:\Automation\geckodriver.exe", firefox_profile=profile,options=options)
    counter = 0
    hrefs = []
    products = []
    asins = []
    global prods
    prods = {}
    for i in range(1, NUM_OF_PAGES+1):
        url = f"{url}&page={i}"
        driver.get(url)
        links = driver.find_elements_by_tag_name("a")
        for link in links:
            href = str(link.get_attribute("href"))
            index = href.find("/dp/")
            review = href.find("customerReviews")
            from_query = href.find("qid")
            if index != -1 and review == -1 and from_query != -1:
                hrefs.append(href)
                asin = href[index + 4:index + 14]
                if asin not in asins:
                    if "https://www.amzn.com/" in href:
                        prefix = 21
                    else:
                        prefix = 23
                    productName = href[prefix:index].replace('-', ' ')
                    products.append(productName)
                    asins.append(asin)
                    counter += 1
    text_box.configure(state="normal")
    for i in range(len(asins)):
        text_box.insert("0.0", asins[i] + "\n")
    for i in range(len(products)):
        prods[products[i]] = asins[i]
    mb.showinfo(title="Run Completed",message=f"Found {counter} unique ASINs")
    text_box.configure(state="disabled")
    return prods

def copy_to_clipboard(window, results):
    window.clipboard_append(results.get("0.0", "end"))

def clear(results, url):
    url.delete(0, 'end')
    results.configure(state="normal")
    results.delete("0.0", "end")
    results.configure(state="disabled")

def export_to_csv():
    global prods
    time = datetime.now()
    try:
        if prods:
            with open(f'{time.strftime("asins-%m-%d-%Y-%H-%M-%S")}.csv', 'w') as f:
                for key in prods.keys():
                    f.write("%s,%s\n" % (key, prods[key]))
        mb.showinfo(title="Export to CSV",
                    message=f"Export Succeeded! file is: {time.strftime('asins-%m-%d-%Y-%H-%M-%S')}")
    except:
        mb.showerror(title="No results to export",
                     message="There are no results to export! Run first or try a different URL")

def main():
    window = tk.Tk(className=" Amazon ASIN Grabber © amiros89")
    # bg = tk.PhotoImage(file = "amazon-logo.gif")
    window.geometry("800x600")
    window.maxsize(800,600)
    window.minsize(800,600)
    greeting = tk.Label(text="ASIN Grabber", font=("Arial Bold",20))
    greeting.pack()
    url = tk.Entry()
    url.pack()
    url.place(x=200, y=125, height=30, width=400)

    button_run = tk.Button(
        text="Run",
        height="2",
        width="15",
        font= "Arial",
        command=lambda: grab(url=url.get(), text_box=results)

    )
    button_copy_to_clipboard = tk.Button(
        text="Copy to Clipboard",
        height="2",
        width="15",
        font="Arial",
        command=lambda: copy_to_clipboard(window, results)
    )

    button_run.pack()
    button_run.place(x=100, y=500)

    button_copy_to_clipboard.pack()
    button_copy_to_clipboard.place(x=250, y=500)

    button_export_to_csv = tk.Button(
        text="Export to CSV",
        height="2",
        width="15",
        font="Arial",
        command=lambda: export_to_csv()
    )
    button_export_to_csv.pack()
    button_export_to_csv.place(x=400, y=500)

    button_clear = tk.Button(
        text="Clear",
        height="2",
        width="15",
        font="Arial",
        command=lambda: clear(results, url)
    )
    button_clear.pack()
    button_clear.place(x=550, y=500)

    label = tk.Label(text="Enter URL here:", font= "Arial")
    label.pack()
    label.place(x=200, y=100, height=30, width=400)

    results_label = tk.Label(text="Results",font=("Arial"))
    results_label.pack()
    results_label.place(x=200, y=170, height=30, width=400)

    results = st.ScrolledText(window, wrap=tk.WORD, state="disabled")
    results.pack()
    results.place(x=200, y=200, height=275, width=400)

    window.mainloop()


if __name__ == "__main__":
    main()
