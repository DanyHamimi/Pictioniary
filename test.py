import random
import string

def RandomWord():
    result = random.randint(0, 9)

    operator = random.choice(["+", "-", "*", "//"])

    if operator == "+":
        num1 = random.randint(0, result)
        num2 = result - num1
    elif operator == "-":
        num1 = random.randint(result, 1000)
        num2 = num1 - result
    elif operator == "*":
        num1 = random.choice([i for i in range(1, 10) if result % i == 0])
        num2 = result // num1
    else: # operator == "//"
        num1 = random.randint(1, 9)
        num2 = num1 * result

    math_problem = f"{num1} {operator} {num2}"
    print("Calcul à résoudre : " + math_problem)
    return result
    
print(RandomWord())