import random
digit = int(input("How many digits would you like to play (4 ~ 10) :"))
number = []
if 4 <= digit <= 10:
    for i in range(10):
        number.append(str(i))
    while number[0] == "0":
        random.shuffle(number)
    while len(number) > digit:
        number.remove(number[-1])
else:
    print("The game is over")


print("All numbers (0 ~ 9) won't repeat")
guess = input(f"Guess a {digit}-digits number :")
Guess = list(guess)
if len(Guess) != digit:
    print("The game is over")


def function_a():
    a = 0
    for k in range(digit):
        if number[k] == Guess[k]:
            a +=1
    return str(a)

def function_b():
    b = 0
    for i in range(digit):
        for j in range(digit):
            if number[i] == Guess[j] and i != j:
                b += 1
    return str(b)


turn = 1
while Guess != number:
    function_a()
    function_b()
    print(function_a() + "a" + function_b() + "b")
    guess = input(f"Guess a {digit}-digits number :")
    Guess = list(guess)
    turn += 1
    

if Guess == number:
    print("You win!")
    if turn <= 5:
        print(f"You only use {turn} turns!")
    else:
        print(f"You use {turn} turns")
