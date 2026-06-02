price = 1000000
good_credit = False
if good_credit :
    down = 0.1*float(price)
else:
    down = 0.2*float(price)

print("Down payment is $" + str(down))