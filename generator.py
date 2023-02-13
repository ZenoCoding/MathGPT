import jsonlines
import utils
from utils import ProblemType
import random
from enum import Enum

from solver import Solver

import openai

import sympy as sp

openai.api_key = "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"


# Function that generates simple binomials with variable x
def generate_binomial(leading_is_one: bool = True) -> str:
    return f"({random.Random().randint(-10, 10) if not leading_is_one else ''}x {random.Random().choice(['+', '-'])} {random.Random().randint(1, 10)})"


# Function that generates simple factor able polynomials with variable x by multiplying two binomials
def generate_factorable_polynomial(degree: int = 1, leading_is_one: bool = True) -> sp.Expr:
    polynomial = utils.convert_expression(generate_binomial(leading_is_one))
    x = random.Random().randint(0, 5)
    for i in range(degree-1):
        # generate a binomial
        binomial = utils.convert_expression(generate_binomial(leading_is_one))
        polynomial = polynomial * binomial
        # On the last iteration, occasionally add a partially factored portion to the polynomial
        if i == degree - 2 or i == degree - 3:
            if x == 0:
                pass
            elif x == 1 and not leading_is_one:
                polynomial *= random.randint(1, 10)
            else:
                polynomial = sp.expand(polynomial)
        else:
            polynomial = sp.expand(polynomial)

    return str(polynomial)


prompts = {
    "factor_polynomial": [
        f"Factor the polynomial %s.",
        f"Find the factors of the polynomial %s.",
        f"Find the factorization of the polynomial %s.",
        f"%s Factor.",
        f"Factor %s",
        f"Factor the polynomial %s",
        f"Please factor the polynomial %s"
    ],
    
    "solve_quadratic": [
        f"Solve for x. %s.",
        f"Find the roots of %s.",
        f"Use the quadratic equation to solve for x %s.",
        f"Solve. %s.",
        f"%s Solve.",
        f"equate to 0 and solve %s",
        f"Factor the polynomial %s",
        f"Please factor the polynomial %s",
    ],

}


class ProblemType(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, prompts: list, expression_generator, solver):
        # Name of the problem type (id)

        # List of prompts to choose from, should contain placeholders for the expression - %s
        self.prompts = prompts

        # Function that generates an sp.Expr expression
        self.expression_generator = expression_generator

        # Function that solves an expression
        self.solver = solver

    def generate_problem(self, amount: int = 1) -> list[tuple[str]]:
        result = []
        for _ in range(amount):
            # Choose a random prompt
            prompt = random.Random().choice(self.prompts)
            # Generate an expression
            expression = self.expression_generator()
            # Replace the placeholder with the expression
            prompt = prompt.replace("%s", expression)
            # Return the prompt and the expression
            result.append(prompt, f"{expression} | {self.name}")
        return result

    def solve(self, expression: str):
        return self.solver(expression)


    # Degree of two or less
    FACTOR_SIMPLE_POLYNOMIAL = prompts["factor_polynomial"], lambda: generate_factorable_polynomial(2, True), Solver.factor  # x^2 + 3x + 1
    FACTOR_SIMPLE_NONONE_POLYNOMIAL = prompts["factor_polynomial"], lambda: generate_factorable_polynomial(2, False), Solver.factor # 3x^2 + 3x + 1

    # Degree more than two
    FACTOR_HIGH_DEGREE_POLYNOMIAL = prompts["factor_polynomial"], lambda: generate_factorable_polynomial(random.Random().randint(3, 10), True), Solver.factor  # x^3 + 3x + 1

    # Lower than 1 degree polynomial
    #FACTOR_SIMPLE =   # 2x+2

    #QUADRATIC_POLYNOMIAL_ROOT_FACTOR =   # x^2 + 2x + 1
    #QUADRATIC_POLYNOMIAL_ROOT_QUADRATIC_EQUATION =   # x^2 + 2x + 1 = 0



AMOUNT = 100


def generate_prompts():
    for i in range(AMOUNT):
        leading_is_one = random.Random().randint(0, 1) == 1
        polynomial = generate_factorable_polynomial(leading_is_one)
        prompt = create_prompt(polynomial)
        with jsonlines.open("output/prompts.jsonl", mode="a") as writer:
            writer.write({"prompt": prompt + "\n\n###\n\n",
                          "completion": f"{polynomial} | {ProblemType.FACTOR_SIMPLE_POLYNOMIAL if leading_is_one else ProblemType.FACTOR_SIMPLE_NONONE_POLYNOMIAL}###"})
        print(f"Generating prompt | Type: | ...  {i + 1}/{AMOUNT} {round((i + 1) / AMOUNT * 100, 2)}%")


# function that takes the prompts and "randomizes" them, converting some "**" to ^ and removing some cases of
# explicit multiplication and spaces
def randomize_prompts():
    with jsonlines.open("output/prompts.jsonl", mode="r") as reader:
        new_prompts = []
        for prompt in reader:
            result = ""
            r = random.Random()
            for c in range(len(prompt["prompt"])):
                if r.randint(0, 1) == 1:
                    if prompt["prompt"][c] == '*' and prompt["prompt"][c + 1] == "*":
                        result += "^"
                    elif prompt["prompt"][c] == "*" and prompt["prompt"][c - 1] != "*":
                        result += ""
                    else:
                        result += prompt["prompt"][c]
                else:
                    result += prompt["prompt"][c]
            new_prompts.append({"prompt": result, "completion": prompt["completion"]})

        for prompt in new_prompts:
            with jsonlines.open("output/prompts.jsonl", mode="a") as writer:
                writer.write({"prompt": prompt["prompt"], "completion": prompt["completion"]})


print("Factorable quadratic: ", generate_factorable_polynomial(2, True))
print("Factorable quadratic: ", generate_factorable_polynomial(3, True))
print("Factorable quadratic: ", generate_factorable_polynomial(4, True))
print("Factorable quadratic: ", generate_factorable_polynomial(5, True))
print("Factorable quadratic: ", generate_factorable_polynomial(2, True))
print("Factorable quadratic: ", generate_factorable_polynomial(3, True))
print("Factorable quadratic: ", generate_factorable_polynomial(4, True))
print("Factorable quadratic: ", generate_factorable_polynomial(5, True))

# openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
# openai api fine_tunes.create -t formatted_prompts.jsonl -m babbage --suffix "recognition"
