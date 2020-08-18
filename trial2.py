import filestore2
import time, datetime, pickle
articleBase = filestore2.articles

# This is the function that is called at the beginning of the program                                                                        
def postcard():                                                                     
    print ("Welcome to Best - Buy, Hustle and Heart set us apart.\n")               
                                                                                        
    prompt=raw_input("""To apply for a new store card, Press 1.\n"""+                                    
                        """To access your existing account, Press 2.\n--> """)      
                                                                                        
    if prompt == '1':                                                               
        cus=CardAccount()                                                           
        # Creates a new customer profile                                            
                                                                                    
    elif prompt == '2':                                                             
        cus=ReturnCustomer()                                                        
        # Checks for existing customer                                              
                                                                                    
    else:                                                                           
        print "You have Pressed the Wrong Key, Please try again."                   
        postcard()                                                                  
                                                                                    
# Class for creating an instance of a new back account and other default bank functions
class CardAccount:
    # Class for a Card Account
    type="Normal Account"

    def __init__(self):
        # Calls functions in the module filestore2
        self.username, self.userpassword, self.balance=filestore2.cusaccountcheck()
        print ("\nThank you %s, Your account is set up and ready to use.\nRs. 100 has been credited to your account." %self.username)
        time.sleep(4)
        self.userfunctions()

    # This function shows the choices to the user
    def userfunctions(self):
        print("\n\nTo access any function below, Enter the corresponding key:")
        print ("""To
Check Balance,  Press B.
Deposit Cash,   Press D.
Buy Products,   Press P.
View Cart,      Press V.
Delete Account, Press X.
Exit Service,   Press E.
-->"""),
        ans=raw_input("").lower()

        if ans == 'b':
            # Passcheck function confirms stored password with user input
            self.passcheck()
            self.checkbalance()

        elif ans == 'd':
            # Passcheck function confirms stored password with user input
            self.passcheck()
            self.depositcash()

        elif ans == 'p':
            # Passcheck function confirms stored password with user input
            self.passcheck()
            self.buyproducts()

        elif ans == 'v':
            # Passcheck function confirms stored password with user input
            self.passcheck()
            self.viewcart()

        elif ans == 'x':
            print ("%s, Your Account is being Deleted..."%self.username)
            print ""            
            time.sleep(2)
            filestore2.deleteaccount(self.username)
            print ("Your Account has been successfuly Deleted.\nThank You for using our Services.")

        elif ans == 'e':
            print ("Thank you for using Best - Buy Services.")
            time.sleep(1)
            print ("Goodbye... %s" %self.username)
            exit()

        else:
            print "No function assigned to this key, Please try again."
            self.userfunctions()

    # This function returns the current balance of the account holder
    def checkbalance(self):
        date=datetime.date.today()
        date=date.strftime('%d-%B-%Y')
        
        self.working()
        print ("\nYour Account Balance as on {} is {}").format(date, self.balance)
        self.transact_again()
        

    #This function shows the choice of products for buying
    def buyproducts(self):
        #Pick department
        print("Choose a Department: ")
        departments = articleBase['departments']
        
        for departmentID in range(len(departments)):
            print departmentID+1,"\b.",departments[departmentID]['name'],"\b."
        choice = int(raw_input("\nPick a Department between 1 and " + str(len(departments)) + ".\n--> "))

        if choice <= len(departments):
           chosenDepartment = departments[choice-1]
        else:
            print "Wrong Choice !!! Try Again..."
            self.buyproducts()
            print ""
            
        #Pick category
        print ""
        print("Choose a Category: ")
        categories = chosenDepartment['categories']
        
        for categoryID in range(len(categories)):
            print categoryID+1,"\b.",categories[categoryID]['name'],"\b."
        choice = int(raw_input("\nPick a Category between 1 and " + str(len(categories)) + ".\n--> "))

        if choice <= len(categories):
            chosenCategory = categories[choice-1]
        else:
            print "Wrong Choice !!! Try Again..."
            self.buyproducts()
            print ""
        
        #Pick article
        print ""
        print("Choose an Article: ")
        articles = chosenCategory['articles']        
        for articleID in range(len(articles)):
            print articleID+1,"\b.",articles[articleID]['name'],"\b....... Rs.",articles[articleID]['price']
        choice = int(raw_input("\nPick an Article between 1 and " + str(len(articles)) + ".\n--> "))

        if choice <= len(articles):
            chosenArticle = articles[choice-1]            
            cArticle = articles[choice-1]['name']
            cRate = articles[choice -1]['price']
            cQty = input("Enter Quantity Required. \n--> ")
            cPrice = cRate * cQty

            a = self.checkoverlap(cArticle, cQty, cPrice)
            if a == True:
                self.overlap(cArticle, cQty, cPrice)
            elif a == False:
                filestore2.additem(cArticle, cQty, cPrice, cRate)
                    
        else:
            print "Wrong Choice !!! Try Again..."
            self.buyproducts()
            print ""
        
        time.sleep(0.50)
        print("The Item's Price is Rs. " + str(cQty*chosenArticle['price']))        
        self.working()
        self.transact_again()

    # This function shows the selected items
    def viewcart(self):
        cartitem=open("Cart Database/cusitemfile.txt", "r")
        cartqty=open("Cart Database/cusqtyfile.txt", "r")
        cartprice=open("Cart Database/cuspricefile.txt", "r")
        cartrate=open("Cart Database/cusratefile.txt", "r")

        with cartitem as i:
            items = [line.strip() for line in i]            
        with cartqty as i:
            qtys = [line.strip() for line in i]            
        with cartprice as i:
            prices = [line.strip() for line in i]
        with cartrate as i:
            rates = [line.strip() for line in i]
        
        for ID in range(len(items)):
            print ID+1,"\b.",items[ID],"\b............... Rs.",rates[ID]
            print "   x",qtys[ID],"         --> Rs.",prices[ID],"\n"
            
        time.sleep(1.5)
        self.paycart()

    # This function checks for any overlapping items
    def checkoverlap(self, item, qty, price):
        I = item+"\n"
        Q = qty
        P = price

        Item = []
        Quantity = []
        Price = []
        Rate = []

        with open("Cart Database/cusitemfile.txt") as sourcefile1:
            Item = sourcefile1.readlines()
            
        with open("Cart Database/cusqtyfile.txt") as sourcefile2:
            Quantity = sourcefile2.readlines()
            
        with open("Cart Database/cuspricefile.txt") as sourcefile3:
            Price = sourcefile3.readlines()
            
        with open("Cart Database/cusratefile.txt") as sourcefile4:
            Rate = sourcefile4.readlines()

        try :
            if I in Item:
                return True
            else:
                return False
                
        except ValueError:
            pass
        
    # This function adds the quantity of the overlapped items
    def overlap(self, item, qty, price):
        I = item+"\n"
        Q = qty
        P = price
        
        Item = []
        Quantity = []
        Price = []
        Rate = []

        with open("Cart Database/cusitemfile.txt") as sourcefile1:
            Item = sourcefile1.readlines()
            
        with open("Cart Database/cusqtyfile.txt") as sourcefile2:
            Quantity = sourcefile2.readlines()
            
        with open("Cart Database/cuspricefile.txt") as sourcefile3:
            Price = sourcefile3.readlines()
            
        with open("Cart Database/cusratefile.txt") as sourcefile4:
            Rate = sourcefile4.readlines()

        try :
            if I in Item:
                a = Item.index(I)
                Quantity[a] = int(Quantity[a])
                Rate[a] = int(Rate[a])
                Price[a] = int(Price[a])
                
                Quantity[a] = Quantity[a] + Q
                Price[a] = Rate[a]*Quantity[a]

                Quantity[a] = str(Quantity[a])
                Rate[a] = str(Rate[a])
                Price[a] = str(Price[a])
                
        except ValueError:
            pass
        
        with open("Cart Database/cusitemfile.txt", "a") as cartfile1:
            cartfile1.seek(0)
            cartfile1.truncate()
            for line in Item:
                cartfile1.write(line)
        cartfile1.close()
        
        with open("Cart Database/cusqtyfile.txt", "a") as cartfile2:
            cartfile2.seek(0)
            cartfile2.truncate()
            for line in Quantity:
                cartfile2.write(line)
        cartfile2.close()
        
        with open("Cart Database/cuspricefile.txt", "a") as cartfile3:
            cartfile3.seek(0)
            cartfile3.truncate()
            for line in Price:
                cartfile3.write(line)
        cartfile3.close()
        
        with open("Cart Database/cusratefile.txt", "a") as cartfile4:
            cartfile4.seek(0)
            cartfile4.truncate()
            for line in Rate:
                cartfile4.write(line)
        cartfile4.close()    
                
    # This function pays for the item in the cart, reducing your balance       
    def paycart(self):
        cart = open("Cart Database/cuspricefile.txt", "r")
        sub = cart.readlines()
        total = 0

        for i in sub:
            printnum=0
        
            try:
                printnum += float(i)
                total += printnum
            
            except ValueError:
                print "Invalid Literal for int() with Base 10: ",ValueError
                
        print "The Total Amount to be Paid is Rs.",total,"\n"
        if total!=0:
            choice = raw_input("Do You want to Remove any items from the Cart? (Y/N)\n--> ").lower()
            if choice == 'y':
                removeitem = raw_input("Enter the Item to be Removed \n--> ")
                self.removecart(removeitem)
            else:
                pay = raw_input("Do You want to Pay for the Items in the Cart now? (Y/N)\n--> ").lower()
                self.working()

                if pay == 'y':            
                    if self.balance >= total:
                        self.balance -= total

                        totalbal = total - 2*total
                        print ("\nYour new Account Balance is Rs. %.2f" %self.balance)
                        filestore2.balupdate(self.username, totalbal)
                        filestore2.cleancart()

                    else:
                        print "Insufficient Funds !!!"
                        print "Deposit Cash and Try Again later..."
                        
                elif pay == 'n':
                    print "\nItems Remain in the Cart Till you Check-out..."
                    time.sleep(1)
                    
                else:
                    print "Wrong Choice !!! Try Again..."
                    self.paycart()
                    print ""

        elif total==0:
            print "Your Cart is Empty..."
            choose = raw_input("Do You want to Buy Products, now? (Y/N)\n--> ").lower()
            if choose == 'y':
                self.passcheck()
                self.buyproducts()
            else:
                print "Leading to Home Page."
                self.working()
        
        self.transact_again()

    # This function removes the items from the cart
    def removecart(self, item):
        I = item+"\n"

        Item = []
        Quantity = []
        Price = []
        Rate = []

        with open("Cart Database/cusitemfile.txt") as sourcefile1:
            Item = sourcefile1.readlines()
            
        with open("Cart Database/cusqtyfile.txt") as sourcefile2:
            Quantity = sourcefile2.readlines()
            
        with open("Cart Database/cuspricefile.txt") as sourcefile3:
            Price = sourcefile3.readlines()
            
        with open("Cart Database/cusratefile.txt") as sourcefile4:
            Rate = sourcefile4.readlines()

        try:
            if I in Item:
                a = Item.index(I)
                del Item[a]
                del Quantity[a]
                del Price[a]
                del Rate[a]

        except ValueError:
            pass

        with open("Cart Database/cusitemfile.txt", "a") as cartfile1:
            cartfile1.seek(0)
            cartfile1.truncate()
            for line in Item:
                cartfile1.write(line)
        cartfile1.close()
        
        with open("Cart Database/cusqtyfile.txt", "a") as cartfile2:
            cartfile2.seek(0)
            cartfile2.truncate()
            for line in Quantity:
                cartfile2.write(line)
        cartfile2.close()
        
        with open("Cart Database/cuspricefile.txt", "a") as cartfile3:
            cartfile3.seek(0)
            cartfile3.truncate()
            for line in Price:
                cartfile3.write(line)
        cartfile3.close()
        
        with open("Cart Database/cusratefile.txt", "a") as cartfile4:
            cartfile4.seek(0)
            cartfile4.truncate()
            for line in Rate:
                cartfile4.write(line)
        cartfile4.close()    
        self.viewcart()
        
    # This function increases your balance        
    def depositcash(self):
        amount=float(raw_input("Please Enter Amount to be Deposited to Card. \n--> "))
        self.balance += amount
        self.working()
        
        print ("\nYour new Account Balance is Rs. %.2f" %self.balance)     
        filestore2.balupdate(self.username, amount)
        self.transact_again()

    # This function lets the user transact again
    def transact_again(self):
        print ""
        ans=raw_input("Do You want to do any other Transaction? (Y/N)\n--> ").lower()
        self.working()
        
        if ans=='y':
            print ""
            self.userfunctions()
            
        elif ans=='n':
            print ("\nThank you for using Best - Buy, we value you. Have a good day.")
            time.sleep(1)
            print ("Goodbye, {}.").format(self.username)
            exit()
            
        elif ans!='y' and ans!='n':
            print "Unknown key pressed, Please choose either 'N' or 'Y'\n"
            self.transact_again()


    def working(self):        
        print("working"),
        time.sleep(0.75)
        
        print ("..."),
        time.sleep(0.75)
        
        print("..."),
        time.sleep(0.75)
        
        print ("..."),
        time.sleep(0.75)
        
        print("..."),
        time.sleep(1)
        
    # This function checks the password entered
    def passcheck(self):
        # Prompts user for password for each function and counterchecks it with stored passwords.
        b=3
        while b>0:
            ans = raw_input("Please Type in your Password to Continue with the function.\n--> ")
            if ans == self.userpassword:
                return True

            else:
                print "That is the Wrong Password."
                b-=1
                print ("%d more Attempt(s) Remaining." %b)

        print ("Smart Card Account has been freezed due to three wrong password attempts.\nContact our reception for help.")
        
        time.sleep(1)
        print ("...")
        
        time.sleep(1)
        print("...")
        
        time.sleep(1)
        exit()
                
class ReturnCustomer(CardAccount):
    type="Normal Account"
    def __init__(self):
        self.username, self.userpassword, self.balance=filestore2.oldcuscheck()
        self.userfunctions()

postcard() # calling the function to run the program
