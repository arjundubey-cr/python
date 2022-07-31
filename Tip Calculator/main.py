print('Welcome to tip calculator')

print(6 + 4 / 2 - (1 * 2))
bill_amount = float(input('What was the total bill amount? '))
percentage_tip = float(input("What percentage tip would you like to give? "))
total_persons = float(input("How many people to split the bill? "))

total_bill_amount = bill_amount + (percentage_tip / 100) * bill_amount
splited_amount = total_bill_amount / total_persons
print("Each person should pay: " + str(splited_amount))
