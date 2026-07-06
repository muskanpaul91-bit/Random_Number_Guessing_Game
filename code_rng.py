import numpy as np
name=input("Enter your name:").title()
print(f'Hello!! {name} welcome!! to world of Guessing.')

def easy():
    num=np.random.randint(1,31)
    attempt=1
    while attempt<=8:
        try:
            guess=int(input('Enter the number:'))
            if guess<1 or guess>30:
                print("Invalid range please select between 1-30")
                continue
        except ValueError:
            print("Please choose a whole number")
            continue
        
        if guess == num:
            if attempt==1:
                print(f"🎉 Amazing, {name}! You guessed the number on your first try!")
                break
            else:
                print(f"🎉 Congratulations, {name}! You guessed the number in {attempt} attempts.")
                break
        elif guess<num:
            print('📈 Too low! Try a bigger number.')
        else:
            print("📉 Too high! Try a smaller number.")
        attempt+=1
        if attempt<=8:
            print(f"Attempts left {9-attempt}")
        
        if attempt==6:
            print(f"You have only {9-attempt}  attempts left! Would you like to use your hint? (yes/no)")
            choice=input("Enter your choice:").lower()
            if choice=="yes":
                print("💡.........Hints.........💡")
                print("Divisible by 2",end=' & ') if num%2==0 else print("Not divisible by 2",end=" & ")
                print("Divisible by 3.") if num%3==0 else print("Not divisible by 3.")
                
                if num>=1 and num<=10:
                    print("The Number is between 1-10")
                elif num>=11 and num<=20:
                    print("The Number is between 11-20")
                else:
                    print("The Number is between 21-30")
            elif choice=='no':
                print("Bold choice! Good luck! 😄")
            else:
                print("Please Choose a valid option.") 
        
        
    else:
       print(f"😔 Game Over!{name} The correct number was {num}.")
                
   
       
def medium():
    num=np.random.randint(1,71)
    attempt=1
    
    while attempt<=6:
        try:
            guess=int(input('Enter the number:'))
            if guess<1 or guess>70:
                print("Invalid range please select between 1-70")
                continue
        except ValueError:
            print("please choose a whole number.")
            continue
        if guess==num:
            if attempt==1:
                print(f"🎉 Amazing, {name}! You guessed the number on your first try!")
                break
            else:
                print(f"🎉 Congratulations, {name}! You guessed the number in {attempt} attempts.")
                break
        elif guess<num:
            print("📉 Too low! Try a bigger number.")
        else:
            print('📉 Too high! Try a smaller number.')
            
        attempt+=1
        if attempt<=6:
            print(f"Attempts left {7-attempt}")
            
        if attempt==5:
            print(f"You have only {7-attempt}  attempts left! Would you like to use your hint? (yes/no)")
            choice=input("Enter your choice:").lower()
            
        
            if choice=="yes":
                print("💡.........Hints.........💡")
                print("Divisible by 2",end=', ') if num%2==0 else print("Not divisible by 2",end=", ")
                print("Divisible by 3",end=' & ') if num%3==0 else print("Not divisible by 3",end=' & ')
                print("Divisible by 5.") if num%5==0 else print("Not divisible by 5.")
                
                if num>=1 and num<=25:
                    print("The Number is between 1-25")
                elif num>=26 and num<=50:
                    print("The Number is between 26-50")
                else:
                    print("The Number is between 51-70")
            elif choice=="no":
                print("Bold choice! Good luck! 😄")
            else:
                print("Please choose a vaild option.")
            
    else:
        print(f'Game over!! {name} the number was {num}')
    
  
def hard():
    num=np.random.randint(1,101)
    attempt=1
    
    while attempt<=5:
        try:
            guess=int(input('Enter the number:'))
            if guess<1 or guess>100:
                print('Invalid range please select between 1-100.')
                continue
        except ValueError:
            print("Please choose a whole number.")   
            continue         
        
        if guess==num:
            if attempt==1:
                print(f"🎉 Amazing, {name}! You guessed the number on your first try!")
                break
            else:
                print(f"🎉 Congratulations, {name}! You guessed the number in {attempt} attempts.")
                break
        elif guess<num:
            print("📉 Too low! Try a bigger number.")
        else:
            print('📉 Too high! Try a smaller number.')
            
        attempt+=1
        if attempt<=5:
            print(f"Attempts left {6-attempt}")
        
        if attempt ==5:
            print(f"You have only {6-attempt}  attempts left! Would you like to use your hint? (yes/no)")
            choice=input("Enter your choice:").lower()
            if choice=="yes":
                print("💡.........Hints.........💡")
                print("Divisible by 2",end=', ') if num%2==0 else print("Not divisible by 2",end=", ")
                print("Divisible by 3",end=' & ') if num%3==0 else print("Not divisible by 3",end=' & ')
                print("Divisible by 5.") if num%5==0 else print("Not divisible by 5.")
                
                if num>=1 and num<=25:
                    print('The Number is between 1-25')
                elif num>=26 and num<=50:
                    print("The Number is between 26-50")
                elif num>=51 and num<=75:
                    print("The Number is between 51-75")
                else:
                    print("The Number is between 76-100")
                    
            elif choice=='no':
                print("Bold choice! Good luck! 😄")
            else:
                print("Please choose a valid option.")
        
    else:
        print(f'Game over!! {name} the number was {num}')
    
  
        
    
def select():               
                
    while True:
        print("Choose a Difficulty Level:-")
        print('1.Easy {Range: 1 to 30, 8 chances}.')
        print('2.Medium {Range: 1 to 70, 6 chances}.')
        print('3.Hard {Range: 1 to 100, 5 chances}.')
        print("0.Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue


        if choice==1:
            easy()
        elif choice==2:
            medium()
        elif choice==3:
            hard()
        elif choice==0:
            print("Thanks!! for playing.")
            break
        else:
            print("Invalid choice!!!")

select()