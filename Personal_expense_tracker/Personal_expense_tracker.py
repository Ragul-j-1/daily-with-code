from datetime import date
def record_date():
    return date.today()

def p_e_t():
    print("+++++++++++ PERSONAL EXPENSES TRACKER+++++++++++")
    date=record_date()
    print(" Category    Amount")
    for category,anmount in expenses.items():
        print(f"      {category} : {anmount}")
        
    total=sum(expenses.values())
    print(f"TOTAL AMOUNT = {total}")
    high=max(expenses.values())
    print(f"HIGHEST AMOUNT={high}")
    

personal_expenses=[]

expenses={}

num_category=int(input("enter the number of category:"))

for _ in range(num_category):
        
    category=input("enter the category:")
    amount=float(input("enter the amount:"))
    expenses[category]=amount
        
    personal_expenses.append(expenses)
p_e_t()
    
    

        
    








