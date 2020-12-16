from bot_token import TOKEN

from discord.ext import commands
from discord.ext import buttons


class MyPaginator(buttons.Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @buttons.button(emoji='\u23FA')
    async def record_button(self, ctx, member):
        await ctx.send('This button sends a silly message! But could be programmed to do much more.')

    @buttons.button(emoji='\u27A1')
    async def silly_button(self, ctx, member):
        await ctx.send('Beep boop...')


bot = commands.Bot(command_prefix='??')


@bot.command()
async def test(ctx):
    pagey = MyPaginator(title='Silly Paginator', colour=0xc67862, embed=True, timeout=90, use_defaults=True, entries=[1, 2, 3], length=1, format='**')

    await pagey.start(ctx)


@bot.event
async def on_ready():
    print('Ready!')


bot.run(TOKEN())