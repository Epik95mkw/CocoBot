import discord


class Paginator(discord.ui.View):
    current_page: int = 1

    def __init__(self, pages: list[dict]):
        super(Paginator, self).__init__(timeout=None)
        self.message = None
        self.pages = pages

    async def send(self, channel: discord.TextChannel):
        self.message = await channel.send(view=self)
        await self.update_message()

    async def update_message(self, message=None):
        if message is not None:
            self.message = message
        self.update_buttons()
        embed = discord.Embed.from_dict(self.pages[self.current_page - 1])
        await self.message.edit(embed=embed, view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == len(self.pages):
            self.next_button.disabled = True
            # self.last_page_button.disabled = True
            # self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            # self.last_page_button.disabled = False
            # self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    @discord.ui.button(label="Current", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction, _):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message()

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction, _):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message()

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction, _):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message()

    # @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    # async def last_page_button(self, interaction, _):
    #     await interaction.response.defer()
    #     self.current_page = len(self.pages)
    #     await self.update_message()
