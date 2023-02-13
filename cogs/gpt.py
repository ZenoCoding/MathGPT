import discord
from discord.ext import commands

import openai
import main
import datetime

import utils


class GPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='gpt', description='Generate text using GPT-3!',
                       guilds=[discord.Object(id=945903743319293992)])
    @discord.option("prompt", description="Enter a prompt.")
    @discord.option("model", description="Select a model.",
                    choices=["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"])
    @discord.option("response_tokens", description="Select the number of tokens to generate.")
    async def gpt_command(self, interaction: discord.Interaction,
                          prompt: str,
                          model: str = "text-curie-001",
                          response_tokens: int = 100):
        await interaction.response.defer()
        start_time = datetime.datetime.now()
        response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=response_tokens)

        embed = utils.create_embed(title="GPT-3 Response", description=response["choices"][0]["text"])
        embed.add_field(name="Model", value=model)
        embed.add_field(name="Tokens", value=response["usage"]["total_tokens"])
        embed.add_field(name="Prompt", value=prompt)
        embed.set_footer(text=f"MathGPT • {(datetime.datetime.now() - start_time).total_seconds().__round__(2)}s",
                         icon_url=self.bot.user.display_avatar.url)

        await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(GPT(bot))
    main.logger.info("Loaded GPT cog")