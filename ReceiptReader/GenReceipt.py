import random

NumOfFiles = 2
NumOfProducts = 50
Products = ["Product_" + str(i) for i in range (0,NumOfProducts)]
Separator = "-------------------------------\n"

for file in range(0,NumOfFiles):
    NumOfReceipts = random.randint(100,100000)
    f = open(str(file),"w")
    f.write(Separator)
    
    for receipt in range(0,NumOfReceipts):
        AFM = "1234567" + str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)) + "\n"
        #NumOfProducts = random.randint(1,10)
        f.write("ΑΦΜ: " + AFM)

        total_cost = 0

        for product in range(0,NumOfProducts):
            f.write(Products[random.randint(0,len(Products) - 1)] + ": ")
            amount = random.randint(1,10)
            f.write(str(amount) + "  ")
            cost = round(random.uniform(1,50),2)
            f.write(str(cost) + "  ")
            prod_cost = round(amount*cost,2)
            f.write(str(prod_cost) + "\n")
            total_cost = total_cost + prod_cost

        f.write("ΣΥΝΟΛΟ: " + str(round(total_cost,2)) + "\n")
        f.write(Separator)

    f.close()





