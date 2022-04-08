import os, pywinauto, time
import pandas as pd


def get_prod(amt:int, age:int, health_class:int, prod_num:int):
    # amt: integer for amount of death benefit
    # age: integer for age
    # health class: 0, 1, or 2 corresponding to three potential health classes
        # health_class = 0: preferred plus
        # health_class = 1: preferred
        # health_class = 2: regular
    # prod_num: integer for product number 1-36
    # get_prod manipulates gowin.exe to save the specified product's data as a csv file 
    os.startfile("gowin.exe")
    time.sleep(5)
    pywinauto.keyboard.send_keys("~"
                                 "~"
                                )
    pywinauto.keyboard.send_keys(str(amt))
    pywinauto.keyboard.send_keys("{TAB}"
                                 "{TAB}"
                                 "{TAB}"
                                )
    pywinauto.keyboard.send_keys(str(age))
    pywinauto.keyboard.send_keys("{TAB}"
                                 "{TAB}"
                                 "{TAB}"
                                )
    if health_class == 0:
        pywinauto.keyboard.send_keys("P"
                                     "{VK_F3}"
        )
    elif health_class == 1:
        pywinauto.keyboard.send_keys("P"
                                     "{RIGHT}"
                                     "{VK_F3}"
        )
    else:
        pywinauto.keyboard.send_keys("R"
                                     "{RIGHT}"
                                     "{VK_F3}"
                                    )
    time.sleep(2)
    pywinauto.keyboard.send_keys("%f"
                                 "{DOWN}"
                                 "{DOWN}"
                                 "{DOWN}"
                                 "{DOWN}"
                                 "~"
                                )
    pywinauto.keyboard.send_keys("Product" + str(prod_num))
    pywinauto.keyboard.send_keys("~"
                                 "%{F4}"
                                )
    time.sleep(5)



amts = [250000, 500000]
ages = [30, 40, 50, 60, 70, 80]
tracker = []


# The following for-loops iterate over the 36 products using get_prod to create csv data files for each product
c = 0
for i in range(6):
    get_prod(amts[i % 2], ages[i % 6], i % 3, c + 1)
    tracker.append((amts[i % 2], ages[i % 6], i % 3, c + 1))
    c += 1
for i in range(6):
    get_prod(amts[i % 2], ages[i % 6], (i + 1) % 3, c + 1)
    tracker.append((amts[i % 2], ages[i % 6], (i + 1) % 3, c + 1))
    c += 1
for i in range(6):
    get_prod(amts[i % 2], ages[i % 6], (i + 2) % 3, c + 1)
    tracker.append((amts[i % 2], ages[i % 6], (i + 2) % 3, c + 1))
    c += 1
for i in range(6):
    get_prod(amts[(i + 1) % 2], ages[i % 6], i % 3, c + 1)
    tracker.append((amts[(i + 1) % 2], ages[i % 6], i % 3, c + 1))
    c += 1
for i in range(6):
    get_prod(amts[(i + 1) % 2], ages[i % 6], (i + 1) % 3, c + 1)
    tracker.append((amts[(i + 1) % 2], ages[i % 6], (i + 1) % 3, c + 1))
    c += 1
for i in range(6):
    get_prod(amts[(i + 1) % 2], ages[i % 6], (i + 2) % 3, c + 1)
    tracker.append((amts[(i + 1) % 2], ages[i % 6], (i + 2) % 3, c + 1))
    c += 1

dat = pd.DataFrame(columns = ['Company Name', 'Product Name', 'Annual', 'Health Class',
                              'Death Benefit', 'Age', 'Product #'])
# The following for-loops combines the 36 individual csv files into one compiled output csv file
for t in tracker:
    df = pd.read_csv("Product" + str(t[3]) + ".csv")
    df = df.rename(columns = {"Company Name (Click to sort V)": "Company Name",
                              "Product Name (Click to sort V)": "Product Name",
                              " Annual": "Annual",
                              "Unnamed: 3": "Health Class"
                             })
    # Remove observations with Health Classes that don't match the specified product
    if t[2] == 0:
        df = df[df["Health Class"] == "P+"]
    elif t[2] == 1:
        df = df[df["Health Class"] == "Pf"]
    else:
        df = df[df["Health Class"] == "Rg"]
    # Remove observations with non-numeric entries in the "Annual" column
    df['Annual'] = df['Annual'].replace(',','', regex = True)
    df = df[pd.to_numeric(df["Annual"], errors = 'coerce').notnull()]
    df["Death Benefit"] = t[0]
    df["Age"] = t[1]
    df["Product #"] = t[3]
    dat = dat.append(df)
dat = dat.reset_index(drop=True)

dat.to_csv('Dec 2022 Output.csv', index = False)