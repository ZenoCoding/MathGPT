import discord
from discord.ext import commands

import openai
import main
from main import logger
import views

import utils
import datetime

import sympy as sp


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='math', description='Solve math problems using CAS!')
    @discord.option("prompt", description="Enter a prompt.")
    @discord.option("imaginary", description="Allow imaginary numbers?", choices=[True, False])
    async def math_command(self, interaction: discord.Interaction,
                           prompt: str,
                           imaginary: bool = False):
        await interaction.response.defer()
        start_time = datetime.datetime.now()

        response = "Invalid equation"
        if prompt.__contains__('='):
            left, right = prompt.split("=")
            left, right = utils.rewrite_implicit_multiplication(left), utils.rewrite_implicit_multiplication(right)
            try:
                left, right = sp.sympify(left, evaluate=True, convert_xor=True), sp.sympify(right, evaluate=True,
                                                                                            convert_xor=True)
                solution = sp.solve(sp.Eq(left, right), set=True)
                response = ""
                logger.info(solution)
                logger.info(f"Solution Vars: {solution[0]} | Sets: {solution[1]}")
                for i in range(len(solution[0])):
                    response += str(solution[0][i]) + "="
                    for j in solution[1]:
                        for k in j:
                            # Check if k is a real number
                            if k.is_real or imaginary:
                                response += str(k) + ", "
                    response += "\n"
            except sp.SympifyError as e:
                response = "Invalid equation - " + str(e)
        else:
            solution = sp.sympify(utils.rewrite_implicit_multiplication(prompt), evaluate=True, convert_xor=True)
            response = solution

        embed = utils.create_embed(title="CAS Response", description=f"`{response}`")
        embed.add_field(name="Prompt", value=f"`{prompt}`")
        embed.set_footer(text=f"MathGPT • {(datetime.datetime.now() - start_time).total_seconds().__round__(2)}s",
                         icon_url=self.bot.user.display_avatar.url)

        await interaction.followup.send(embed=embed, view=views.MathView())

    @discord.slash_command(name='math-gpt', description='Solve math problems using GPT-3 and CAS')
    @discord.option("prompt", description="Enter a prompt.")
    @discord.option("imaginary", description="Allow imaginary numbers?", choices=[True, False])
    async def math_gpt_command(self, interaction: discord.Interaction,
                               prompt: str,
                               imaginary: bool = False):
        await interaction.response.defer()
        start_time = datetime.datetime.now()

        # run the prompt through the recognition model
        completion = openai.Completion.create(engine="babbage:ft-personal:recognition-2023-01-19-06-09-11", prompt=prompt + "\n\n###\n\n", max_tokens=20, temperature=0.0, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=["###"])
        # remove the "###" from the end of the response and split it into two variables with the "|" indice
        completion = completion["choices"][0]["text"].replace("###", "")
        print(completion)
        problem, type = completion.split("|")

        type = type.strip()

        # identify the type as a ProblemType (StrEnum)
        type = utils.ProblemType(type)

        # solve the problem
        try:
            solution = type.solve(problem)
        except sp.SympifyError as e:
            response = "Invalid equation - " + str(e)
        else:
            # depending on the type of solution, produce a different output
            if isinstance(solution, sp.Expr):
                response = str(solution)
            elif isinstance(solution, list):
                response = ", ".join(solution)
            elif isinstance(solution, sp.Set):
                for i in range(len(solution[0])):
                    response += str(solution[0][i]) + "="
                    for j in solution[1]:
                        for k in j:
                            # Check if k is a real number
                            if k.is_real or imaginary:
                                response += str(k) + ", "
                    response += "\n"

        embed = utils.create_embed(title="CAS Response", description=f"`{response}`")
        embed.add_field(name="Prompt", value=f"`{prompt}`")
        embed.add_field(name="Type", value=f"`{type}`")
        embed.set_footer(text=f"MathGPT • {(datetime.datetime.now() - start_time).total_seconds().__round__(2)}s",
                         icon_url=self.bot.user.display_avatar.url)

        await interaction.followup.send(embed=embed, view=views.MathView())


def setup(bot):
    bot.add_cog(Math(bot))
    main.logger.info("Loaded Math cog")