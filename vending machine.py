
print(""" 
▀█░█▀ █▀▀ █▀▀▄ █▀▀▄ ░▀░ █▀▀▄ █▀▀▀ 　 █▀▄▀█ █▀▀█ █▀▀ █░░█ ░▀░ █▀▀▄ █▀▀ 
░█▄█░ █▀▀ █░░█ █░░█ ▀█▀ █░░█ █░▀█ 　 █░▀░█ █▄▄█ █░░ █▀▀█ ▀█▀ █░░█ █▀▀ 
░░▀░░ ▀▀▀ ▀░░▀ ▀▀▀░ ▀▀▀ ▀░░▀ ▀▀▀▀ 　 ▀░░░▀ ▀░░▀ ▀▀▀ ▀░░▀ ▀▀▀ ▀░░▀ ▀▀▀
""")

#Function to color text based on ANSI escape codes
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


#Functions for specific colors
def color_text_yellow(text):
    return f"\033[33m{text}\033[0m"
  
def color_text_pink(text):
  return f"\033[95m{text}\033[0m"

#Function to Display items in a tabular format
def display_items(items):
    #print Table header
    print("+-------+-------------+---------------+--------+")
    print("| Code  |   Category  |    Name       | Price  |")
    print("+-------+-------------+---------------+--------+")
    
#Iterate through items and print details in a formatted table
    for item_number,item_details in items.items():
        code = item_details['Code'] 
        category=item_details['Category']
        name=item_details['Name']
        price = item_details['price']
        print(f"| {code:<5} | {category:<11} | {name:<13} | {price:<6} |")
    print("+-----+-----------+-------------+--------------+")
    
#Function to suggest items based on selected items    
def suggest_items(selected_items,suggestions,vending_machine):
    used_suggestions=[]
    selsected_categories=set()
    drink_selected=False
    suggestion_asked={}
    
#check if drinks are already selected
    for item_code in selected_items:
        item_details=vending_machine.get(item_code)
        if item_details:
            selsected_categories.add(item_details['Category'])
            if item_details['Category']=='Drinks':
                drink_selected=True
                
#provide suggestions based on selected items
    for item_code in selected_items:
        if item_code in suggestions and item_code not in used_suggestions:
           suggestion_codes=suggestions[item_code]
           for suggestion_code in suggestion_codes:
               suggestion_details=vending_machine.get(suggestion_code)
               if suggestion_details:
                 suggestion_Category=suggestion_details['Category']
                 if suggestion_Category=='Drinks' and not drink_selected:
                     if item_code not in suggestion_asked:
                         suggestion_name=suggestion_details['Name']
                         suggestion_price=suggestion_details['price']
                         suggestion_prompt=input(color_text(f"Would you like {suggestion_name} with it? (yes/no): ",'31'))
                         suggestion_asked[item_code] = True
                    
                         if suggestion_prompt.lower() =='yes':
                              selected_items.append(suggestion_code)
                              used_suggestions.append(item_code)
                              drink_selected=True
                              print(f"Added {suggestion_name} to your selection.")
                              return selected_items,vending_machine[suggestion_code]['price']
                         elif suggestion_prompt.lower() == 'no':
                             break
                     else:
                         break
    return selected_items,0
                      
 #Function to select items and calculate total amount                     
def select_items(vending_machine):
    selected_items=[]
    total_amount=0
    
#Select items and calculate total amount 
    while True:
        selected_item = input(color_text("Enter the code(s) of the item(s) you want to purchase (separated by commas) or 'done' to finish: " , '32'))

        if selected_item.lower() =='done':
            break
     
        items = selected_item.split(',')
        for item in items:
            if item.strip() in vending_machine:
                selected_items.append(item.strip())
                total_amount += vending_machine[item.strip()]['price']
            else:
                print(f"Invalid item code '{item.strip()}'. please select a valid item or enter 'done' to finish")
                
    return selected_items,total_amount
        
        
#Vending machine items and suggestions  
vending_machine= {
    "F1": {"Code": "F1", "Category":"snacks", "Name":"lays","price":1},
    "F2": {"Code": "F2", "Category":"snacks", "Name":"cheetos","price":1},
    "F3": {"Code": "F3", "Category":"snacks", "Name":"Doritos","price":1.5},
    "F4": {"Code": "F4", "Category":"snacks", "Name":"popcorn","price":2},
    "A5": {"Code": "A5", "Category":"chocolate","Name":"Dairy milk","price":1.5},
    "A6": {"Code": "A6", "Category":"chocolate","Name":"Mars","price":1.5},
    "A7": {"Code": "A7", "Category":"chocolate","Name":"Adore","price":1.5},
    "D8": {"Code": "D8", "Category":"Drinks","Name":"7up","price":2},
    "D9": {"Code": "D9", "Category":"Drinks","Name":"Cola","price":2},
    "D10":{"Code": "D10", "Category":"Drinks","Name":"water","price":2},

}  
  
  
suggestions={
    "F1":["D8"],
    "F2":["D9"],
    "F3":["D10"],
    "F4":["D9"],
}

selected_items_details=[]
#List of different categories
snacks=["F1","F2","F3","F4"]
chocolates=["A5","A6","A7"]
drinks=["D8","D9","D10"]
#Display available items
display_items(vending_machine)

#payement process
cash_inserted=float(input(color_text("Please insert cash: ", '\033[93')))
selected_items, total_amount = select_items(vending_machine)
#Process selected items
if selected_items:
    selected_items,suggested_price = suggest_items(selected_items, suggestions, vending_machine)
    total_amount += suggested_price


if selected_items:
    suggest_items(selected_items,suggestions,vending_machine)
    print(color_text("\nSelected items:",'33'))
    
    
    for item_code in selected_items:
        items_details=vending_machine.get(item_code)
        if items_details:
            item_name=items_details['Name']
            item_category = items_details['Category']
            item_price=items_details['price']
            selected_items_details.append(f"{item_name} ({item_category}) - {item_price}$")
            
#Display selected items        
    if selected_items_details:
        for item in selected_items_details:
            print("-",color_text_yellow(item))
    else:
        print("No items selected")
        
#Process of payement and additional cash    
    while cash_inserted < total_amount:
        print("Insufficient cash. current amount:", cash_inserted)
        choice=input(color_text("Would you like to insert more money or quit?(insert/quit): ",'91'))
        if choice.lower()=='insert':
            extra_cash=input("please insert additional cash:")
            try:
                extra_cash=float(extra_cash)
                cash_inserted += extra_cash
            except ValueError:
                print("Invalid amount. please enter a valid cash amount.")
        elif choice.lower() == 'quit':
            print("Transaction canceled.Returning cash:",cash_inserted)
            break
        else:
            print("Invalid choice.please enter 'insert to add more money or 'quit' to cancel transaction.")

 #Dispense items if payement is sufficient           
if cash_inserted >= total_amount:
    for item_code in selected_items:     #Dispense items and calculate change
        items_details = vending_machine.get(item_code)
        if items_details:
            item_name = items_details['Name']
            item_Category = items_details['Category']
            item_price = items_details['price']
            colored_item_name=color_text_pink(item_name)
            print(f"\nDispensing {item_name} for {item_price}$. {color_text_pink('Enjoy your')} {colored_item_name}")#Applying pink color to the item name.
            
    change= cash_inserted - total_amount
    if change > 0:
        print(color_text("\nHere's your change: ",'34') + str(change) +  "$" )
        print(color_text("\nThank you for using my vending machine🖤\n" , '95'))
else:
    
      print("Insufficient cash. Returning cash:" , cash_inserted)