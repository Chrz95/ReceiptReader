import os
from decimal import *
import decimal
import time
import re

class ReceiptException(Exception):

    message = "The receipt is incorrect"

    def __init__(self,message):
        self.message = message

    def __str__(self):
        return self.message

menu = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program)"
ProdDict = {}
AFMDict = {}
regex = "^-+-+$"

while True:
    print(menu)

    try:
        choice = int(input())
    except:
        continue

    if (choice == 1):
        filename = input()

        if (not os.path.exists(filename)): # File does not exist, so return to menu
            continue

        f = open(filename, "r", encoding='utf-8')

        while(True): # Reads lines until it finds a separator
            line = f.readline()
            if (re.search(regex,line)): # If this line is a separator
                break

        receipt = []

        for line in f: # Read line-line

            if (not re.search(regex,line)): # This is not a separator line
                ##print(line)
                receipt.append(line.strip())
            else: # We have reached a new receipt (read new separator), time to process the old one

                ##print(receipt)

                AFM = ""
                Products = []
                add_to_AFM = 0
                totalSum = Decimal('0')

                try:
                    for idx,row in enumerate(receipt):

                         try:
                            substrings = row.split(': ') # If delimiter does not exist, it will throw ValueError
                         except:
                            raise ReceiptException("Delimiter :  does not exist")

                         if (idx == 0): # AFM Line
                            if (substrings[0].upper() != 'ΑΦΜ'):
                                #print(substrings[0].upper())
                                raise ReceiptException("AFM is missing")
                            elif (len(substrings) != 2):
                                raise ReceiptException("AFM line must have two elements")
                            else:
                                try:
                                    AFM = substrings[1].strip()
                                except:
                                    raise ReceiptException("Not enough elements")

                                if (len(AFM) != 10): # Wrong length of AFM
                                    raise ReceiptException("Wrong length of AFM")

                                try:
                                    x = int(AFM)
                                except ValueError :
                                    raise ReceiptException("AFM is not an integer")

                         elif (idx > 0) and (idx < len(receipt) - 1): # Receipt lines except the last one

                            if (len(substrings) != 2):
                               raise ReceiptException("Wrong amount of info for product (1)")

                            if (len(substrings[0]) == 0):
                                raise ReceiptException("Missing product name")

                            if (substrings[0].upper() == 'ΑΦΜ') or (substrings[0].upper() == 'ΣΥΝΟΛΟ') or (re.search(regex,substrings[0])):
                                raise ReceiptException("Products do not exist (" + substrings[0] + ')')
                            else:
                                Product = substrings[0].upper().strip()
                                newstring = " ".join(substrings[1].split()) # Get rid of redundant whitespaces
                                substrings = newstring.split(' ') # If delimiter does not exist, it will throw ValueError

                                if (len(substrings) != 3):
                                   raise ReceiptException("Wrong amount of info for product (2)")

                                try:
                                    d = decimal.Decimal(substrings[0])
                                except:
                                    raise ReceiptException("Product quantity must be an integer (1)")

                                decimals = abs(d.as_tuple().exponent)

                                if (decimals != 0):
                                    raise ReceiptException("Product quantity must be an integer (2)")

                                try:
                                    if (Decimal(substrings[2]) != Decimal(substrings[1]) * Decimal(substrings[0])): # The total cost of each product must be correct
                                        ##print(decimal.Decimal(substrings[2]))
                                        ##print(Decimal(substrings[1]) * Decimal(substrings[0]))
                                        raise ReceiptException("Incorrect product cost")

                                    totalSum = Decimal(substrings[2]) + totalSum
                                except ValueError:
                                    raise ReceiptException("Cannot convert to float (1)")
                                except decimal.InvalidOperation:
                                    raise ReceiptException("Product info must be in numbers")

                                if (len(substrings) != 3):
                                    raise ReceiptException("Not enough info for product")
                                else:
                                    Products.append((Product,float(substrings[2])))

                         else: # Last line

                             substrings = row.split(': ') # If delimiter does not exist, it will throw ValueError

                             if (substrings[0].upper() != 'ΣΥΝΟΛΟ'):
                                raise ReceiptException("ΣΥΝΟΛΟ is missing")
                             elif (len(substrings) != 2):
                                raise ReceiptException("Not enough info for totalsum")

                             try:
                                 if (float(substrings[1].strip()) != float(totalSum)):
                                    ##print(float(substrings[1].strip()))
                                    ##print(float(totalSum))
                                    raise ReceiptException("Wrong total sum")
                             except ValueError:
                                raise ReceiptException("Cannot convert to float (2)")

                except ReceiptException as e:
                    #print(e)
                    receipt = []
                    continue
                else:
                    receipt = []
                    for Product in Products:

                        # Testing if the AFM and Product were registered before. If not initialize them, else update them

                        try:
                            x = ProdDict[Product[0]]
                        except KeyError as e:
                            ProdDict[Product[0]] = {}

                        try:
                            x = AFMDict[AFM]
                        except KeyError as e:
                            AFMDict[AFM] = {}

                        try:
                            x = ProdDict[Product[0]][AFM]
                        except KeyError as e:
                            ProdDict[Product[0]][AFM] = round(Product[1],2)
                        else:
                            ProdDict[Product[0]][AFM] = round(ProdDict[Product[0]][AFM] + Product[1],2)

                        try: # Testing if the AFM and Product
                            x = AFMDict[AFM][Product[0]]
                        except KeyError as e:
                            AFMDict[AFM][Product[0]] = round(Product[1],2)
                        else:
                            AFMDict[AFM][Product[0]] = round(AFMDict[AFM][Product[0]] + Product[1],2)

        ##print(time.time()-start)
        f.close()

        #print (AFMDict)
        #print (ProdDict)

    elif (choice == 2): # {Product : {AFM: Συνολικό κοστος} }
        try:
            prodname = input()
            #start = time.time()
            prodname = prodname.upper()

            for AFM in sorted(ProdDict[prodname].keys()):
                print(AFM,"{0:.2f}".format(ProdDict[prodname][AFM]))
            #print(time.time() - start," sec")
        except:
            continue
    elif (choice == 3): # {AFM : {Product: Συνολικό κοστος} }
        try:
            AFMNum = input()
            #start = time.time()

            for Prod in sorted(AFMDict[AFMNum].keys()):
                print(Prod,"{0:.2f}".format(AFMDict[AFMNum][Prod]))

            #print(time.time() - start," sec")
        except:
            continue
    elif (choice == 4):
        exit(0)
    else:
        continue
