import discord
import sympy as sp
import utils
import datetime

import main
from main import logger


class MathView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Graph", custom_id="graphing-button", style=discord.ButtonStyle.green, emoji="📈")
    async def btn_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()

        start_time = datetime.datetime.now()

        # Graph the equation
        equation = utils.rewrite_implicit_multiplication(interaction.message.embeds[0].description[1:-1])
        equation = sp.sympify(equation, convert_xor=True)
        sp.plot(equation, show=False).save("output/graph.png")

        # Embed with graph
        embed = main.utils.create_embed(title="Graph", description=equation)
        file = discord.File("output/graph.png", filename="graph.png")
        embed.set_image(url="attachment://graph.png")
        embed.set_footer(text=f"MathGPT • {(datetime.datetime.now() - start_time).total_seconds().__round__(2)}s",
                         icon_url=main.bot.user.display_avatar.url)

        await interaction.followup.send(embed=embed, file=file)
