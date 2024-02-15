from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from db import Finance

engine = create_engine('sqlite:///finansai.db')
Session = sessionmaker(bind=engine)
session = Session()

hello = """_________________________________________
Sveiki, kokius veiksmus norėsite atlikti:
1. Įrašyti įplaukas
2. Įrašyti išlaidas.
3. Gauti Balancą
4. Gauti visas įplaukas
5. Gauti visas išlaidas
6. Ištriti įplaukas arba išlaidas
7. Atnaujint/ Pakeisti įrašą.
8. Išeiti iš programos
_________________________________________
"""
def Action():
    while True:
        try:
            do_what = int(input(hello))
            if do_what > 8:
                print("Prašome vesti skaičiu (Nuo 1 iki 8)")
                continue
            break
        except ValueError:
            print("Prašome vesti tik skaičius")
    return do_what

def Start():
    number = Action()
    if (number == 1):
        Enter_income_expenses(1)
        Start()
    elif (number == 2):
        Enter_income_expenses(2)
        Start()
    elif (number == 3):
        Get_Balance()
        Start()
    elif (number == 4):
        Get_All_Income_Expenses(1)
        Start()
    elif (number == 5):
        Get_All_Income_Expenses(2)
        Start()
    elif (number == 6):
        Deleting()
        Start()
    elif (number == 7):
        Update_Income_expense()
        Start()
    elif (number == 8):
        exit()
        
def Enter_income_expenses(number):
    if (number == 1):
        type_to_db = "Income"
        text = "Iš kur gavote pajamas?\n"
    elif (number == 2):
        type_to_db = "Expences"
        text = "Kur išleidote pajamas?\n"
    expense_category = input(text)
    while True:
        try:
            expense_ammount = int(input("Kokią sumą?\n"))
            break
        except ValueError:
            print("Veskite tik skaičius")
    if (number == 2):
        expense_to_db = 0 - expense_ammount
    else:
        expense_to_db = expense_ammount
    write_to_db = Finance(type_to_db,expense_to_db,expense_category)
    session.add(write_to_db)
    session.commit()

def Get_Balance():
    balance = session.query(Finance.amount).all()
    total_balance = []
    for record in balance:
        ammount = int(record[0])
        total_balance.append(ammount)
    print(f"Jūsų balansas {sum(total_balance)}")
    
def Get_All_Income_Expenses(number):
    if (number == 1):
        search_type = "Income"
        text1 = "gavote"
        text2 = "iš"
    elif (number ==2):
        search_type = "Expences"
        text1 = "išleidote"
        text2 = "ant"
     
    income_list = session.query(Finance).filter_by(type=search_type).all()
    i = 1
    for record in income_list:
        value = record.amount
        category = record.category
        print(f"{i}. Jūs {text1} {value} {text2} {category}")
        i += 1

def record_lookup():
    index = []
    income_list = session.query(Finance).all()
    for record in income_list:
        if (record.amount >0):
            text1 = "gavote"
            text2 = "iš"
            value = record.amount
        elif (record.amount <0):
            text1 = "išleidote"
            text2 = "ant"
            value = record.amount
        category = record.category
        index_to_list = record.id
        index.append(index_to_list)
        print(f"{index_to_list}. Jūs {text1} {value} {text2} {category}")
    try:
        return index
    except UnboundLocalError:
        print("Įrašų nėra")
        Start()
  
def Deleting():
    i = record_lookup()
    while True:
        try:
            select_me = int(input("Prašome pasirinkti kurį irašą norite ištrinti. Įvesdami skaičių\n"))
            if (select_me in i):
                break
            elif(select_me is not i):
                print(f"Prašome vesti tik šiuos skaičius {i}")
        except ValueError:
            print(f"Prašome vesti skaičius nuo 0 iki {i}")
    delete_me = session.query(Finance).filter_by(id=int(select_me)).first()
    session.delete(delete_me)
    session.commit()
    print("Įrašas ištrintas")

def Update_Income_expense():
    i = record_lookup()
    while True:
        try:
            select_me = int(input("Prašome pasirinkti kurį irašą kurį norite pakeisti\n"))
            if (select_me in i):
                replace = session.query(Finance).filter_by(id=select_me).first()
                while True:
                    try:
                        replace_type = int(input("Ar tai 1.Įplaukos 2.Išlaidos? (Įveskite skaičių)\n"))
                    except ValueError:
                        print("Prašome vesti tik skaičius 1 arb 2")
                    if (replace_type == 1 or replace_type == 2):
                        break
                replace_category = input("Įveskite kategoriją (kur išleidote arba gavote) \n")
                replace_ammount = int(input("Įveskite sumą\n"))
                replace.category = replace_category
                if (replace_type == 1):
                    replace.type = "Income"
                    replace.amount = replace_ammount
                elif (replace.type == 2):
                    replace.type = "Expences"
                    replace.amount = 0 - replace_ammount
                session.commit()
                break
            else:
                print(f"Prašome vesti skaičius nuo 0 iki {i}")
        except ValueError:
            print(f"Prašome vesti skaičius nuo 0 iki {i}")
    

Start()