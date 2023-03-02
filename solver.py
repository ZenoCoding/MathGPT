from enum import Enum

import sympy as sp

import utils

class Solver(Enum):

    # Simple Method to evaluate an expression:
    @staticmethod
    def evaluate(parameters: list) -> sp.Expr:
        expression = parameters[0]
        # Convert it to a sympy expression
        utils.convert_expression(expression)
        # Evaluate it
        return expression.evalf()

    # Factor an expression:
    @staticmethod
    def factor(parameters: list) -> sp.Expr:
        expression = parameters[0]
        # Convert it to a sympy expression
        utils.convert_expression(expression)
        # Factor it
        return sp.factor(expression)

    # Expand an expression:
    @staticmethod
    def expand(parameters: list) -> sp.Expr:
        expression = parameters[0]
        # Convert it to a sympy expression
        utils.convert_expression(expression)
        # Expand it
        return sp.expand(expression)

    # Simplify an expression:
    @staticmethod
    def simplify(parameters: list) -> sp.Expr:
        expression = parameters[0]
        # Convert it to a sympy expression
        utils.convert_expression(expression)
        # Simplify it
        return sp.simplify(expression)

    # Find roots of an expression:
    @staticmethod
    def roots(parameters: list) -> sp.Set:
        expression = parameters[0]
        # Convert it to a sympy expression
        utils.convert_expression(expression)
        # Find the roots
        return sp.roots(expression, set=True)

    # Solve for a variable in an expression:
    @staticmethod
    def solve(parameters: list) -> sp.Set:
        equation = parameters[0]

        # Find both sides of the equation
        if "=" not in equation:
            left = equation
            right = 0
        else:
            left, right = equation.split("=")

        # Convert both sides to sympy expressions
        left, right = utils.convert_expression(left), utils.convert_expression(right)
        # Solve it
        return sp.solve(sp.Eq(left, right), set=True)
