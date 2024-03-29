import discord
import sympy as sp
import utils
import datetime

import main
from main import logger

import openai # Import OpenAI API
openai.api_key = "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" # Set OpenAI API key


class MathView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Graph", custom_id="graphing-button", style=discord.ButtonStyle.green, emoji="📈")
    async def btn_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()

        start_time = datetime.datetime.now()

        # re-recognize the equation
        equation = interaction.message.embeds[0].fields[0].value[1:-1]

        equation = openai.Completion.create()

        # Graph the equation
        equation = utils.rewrite_implicit_multiplication()
        equation = sp.sympify(equation, convert_xor=True)
        sp.plot(equation, show=False).save("output/graph.png")

        # Embed with graph
        embed = main.utils.create_embed(title="Graph", description=equation)
        file = discord.File("output/graph.png", filename="graph.png")
        embed.set_image(url="attachment://graph.png")
        embed.set_footer(text=f"MathGPT • {(datetime.datetime.now() - start_time).total_seconds().__round__(2)}s",
                         icon_url=main.bot.user.display_avatar.url)

        await interaction.followup.send(embed=embed, file=file)
