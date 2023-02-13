import discord
import datetime
import re

from solver import Solver

import sympy as sp

from enum import Enum, StrEnum


class Images(Enum):
    # Images used in the bot
    HELP = "https://cdn.discordapp.com/attachments/945903743319293995/945903745260603422/unknown.png"
    AVATAR = "https://cdn.discordapp.com/attachments/1064327068923482193/1064731434042011668/mathgpt.png"


# Function that creates an embed message
def create_embed(title="Title",
                 description="", color=discord.Color.blue(),
                 author: discord.User = None) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="MathGPT", icon_url=Images.AVATAR)
    if author is not None:
        embed.set_author(url=author.display_avatar.url, name=author.name)
    embed.timestamp = datetime.datetime.now()
    return embed


def rewrite_implicit_multiplication(s: str) -> str:
    # Use regular expressions to find all instances of implicit multiplication
    implicit_multiplication_pattern = r"(?<=[0-9a-zA-Z\)])(?=[\(a-zA-Z])|(?<=[a-zA-Z])(?=[0-9a-zA-Z\(])|(?<=[" \
                                      r"0-9a-zA-Z])[ ]*(?=[0-9a-zA-Z]) "
    matches = re.finditer(implicit_multiplication_pattern, s)

    # Create a list to store the start and end indices of each implicit multiplication
    implicit_multiplication_indices = []
    for match in matches:
        implicit_multiplication_indices.append((match.start(), match.end()))

    # Iterate through the implicit multiplication indices in reverse order
    for start, end in reversed(implicit_multiplication_indices):
        # Insert the explicit multiplication symbol at the appropriate position
        s = s[:start] + "*" + s[end:]

    return s


# Converts a text expression to a SymPy expression
def convert_expression(expression: str) -> sp.Expr:
    expression = rewrite_implicit_multiplication(expression)
    return sp.sympify(expression, convert_xor=True)


class ProblemType(StrEnum):
    # Degree of two or less
    FACTOR_SIMPLE_POLYNOMIAL = "factor_simple_polynomial" # x^2 + 3x + 1
    FACTOR_SIMPLE_NONONE_POLYNOMIAL = "factor_nonone_polynomial" # 3x^2 + 3x + 1
    # Degree more than two
    FACTOR_HIGH_DEGREE_POLYNOMIAL = "factor_high_degree_polynomial" # 2x^3 + 3x^2 + 1
    # Lower than 1 degree polynomial
    FACTOR_SIMPLE = "factor_simple" # 2x+2

    QUADRATIC_POLYNOMIAL_ROOT_FACTOR = "polynomial_roots" # x^2 + 2x + 1
    QUADRATIC_POLYNOMIAL_ROOT_QUADRATIC_EQUATION = "quadratic_equation" # x^2 + 2x + 1 = 0

    def solve(self, expression: str):
        return types[self](expression)


types = {
    ProblemType.FACTOR_SIMPLE_POLYNOMIAL: Solver.factor,
    ProblemType.FACTOR_SIMPLE_NONONE_POLYNOMIAL: Solver.factor,
    ProblemType.FACTOR_HIGH_DEGREE_POLYNOMIAL: Solver.factor,
    ProblemType.FACTOR_SIMPLE: Solver.factor,

    ProblemType.QUADRATIC_POLYNOMIAL_ROOT_FACTOR: Solver.factor,
    ProblemType.QUADRATIC_POLYNOMIAL_ROOT_QUADRATIC_EQUATION: Solver.roots
}
