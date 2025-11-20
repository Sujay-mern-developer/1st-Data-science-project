from pathlib import Path
import json
import random
import string

class Bank:
    database = "database.json"
    data = []    

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())

        else:
            print("sorry we are facing some issues") 

    except Exception as err:
        print(f"an error occured as {err}")
    
    @classmethod 
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod        
    def __accountno():
        alpha = random.choices(string.ascii_letters,k = 5)
        digits = random.choices(string.digits,k = 4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)

    def createaccount(self):
        d = {
            "name": input("please tell your name"),
            "email": input("please tell your email"),
            "phone no.": int(input("please tell your no.")),
            "pin": int(input("please tell your pin")),
            "Account no": Bank.__accountno(),
            "balance": 0
            }
        if len(str(d['pin'])) != 4:
            print("please tell your pin correctly")

        elif len(str(d["phone no."])) != 10:
            print("please tell your number correctly")

        else:
            Bank.data.append(d) 
            Bank.__update()   

    def deposite_money(self):
        accNo = input("tell your account number : ")
        pin = int(input("tell your pin : "))
        user_data = [i for i in Bank.data if i["Account no"] == accNo and i["pin"] == pin ]
        if not user_data:
            print("user not found")
        else:
            amount = int(input("enter amount to be deposited : "))
            if amount < 0:
                print("invalid amount")
            elif amount > 10000:
                print("greater than 10000")
            else:
                user_data[0]['balance'] += amount
                Bank.__update()
                print("amount credited")       

    def withdraw_money(self):
        accNo = input("tell your account number : ")
        pin = int(input("tell your pin : "))
        user_data = [i for i in Bank.data if i["Account no"] == accNo and i["pin"] == pin ]
        if not user_data:
            print("user not found")
        else:
            amount = int(input("enter amount to be deposited : "))
            if amount < 0:
                print("invalid amount")
            elif amount > 10000:
                print("greater than 10000")
            else:
                if user_data[0]['balance'] < amount:
                    print("insufficient balance")
                else:
                    user_data[0]['balance'] -= amount
                    Bank.__update()
                    print("amount debited") 


    def details_money(self):
        accNo = input("tell your account number : ")
        pin = int(input("tell your pin : "))
        user_data = [i for i in Bank.data if i["Account no"] == accNo and i["pin"] == pin ]
        if not user_data:
            print("user not found")
        else:
            for i in user_data[0]:
                print(f"{i} : {user_data[0][i]}")



    def update_details(self):
        accNo = input("tell your account number : ")
        pin = int(input("tell your pin : "))
        user_data = [i for i in Bank.data if i["Account no"] == accNo and i["pin"] == pin ]
        if not user_data:
            print("user not found")
        else:
            print("you can not change account number")
            print("now update your details and skip it if you don't want to skip")

            new_data = {
                "name": input("please tell your name"),
                "email": input("please tell your email"),
                "phone no.": int(input("please tell your no.")),
                "pin": int(input("please tell your pin")),
            }

            new_data["Account no."] = user_data[0]["Account no."]
            new_data["Balance"] = user_data[0]["Balance"]
            #Handle the skipped values:


            #We have to update new data to database:

            for i in user_data[0]:
                if user_data[0][i]==new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i]=int(new_data[i])

                    else:
                        user_data[0][i]=new_data[i]
            print(user_data)  
        Bank.__update  
        print("Details updated!")

    def deleting_account(self):
        accNo = input("tell your account number : ")
        pin = int(input("tell your pin : "))
        user_data = [i for i in Bank.data if i["Account no"] == accNo and i["pin"] == pin ]
        if not user_data:
            print("user not found")
        else:
          for i in Bank.data:
            if i['Account no'] == accNo and i['pin'] == pin:
                Bank.data.remove(i)
          Bank.__update()
          print("data deleted")      

   


user = Bank()

print("press 1 for creating an account")
print("press 2 to deposite money")
print("press 3 to withdraw money")
print("press 4 for details")
print("press 5 for update_details")
print("press 6 for deleting account")

check = int(input("tell your choice :- "))  

if check == 1:
    user.createaccount()

elif check == 2:
    user.deposite_money()

elif check == 3:
    user.withdraw_money()

elif check == 4:
    user.details_money()

elif check == 5:
    user.update_details()    