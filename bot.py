import json
import re
import interactions
from interactions import CommandContext
import dotenv
import os
from magnaindextools import *
from interactions import Embed
import re
dotenv.load_dotenv()
bot = interactions.Client(token=os.getenv("BOT_TOKEN"))
index_file = open("indexs/BEASTARS.index.json", 'r')
index = json.load(index_file)
index_file.close()



async def sendpage(ctx: interactions.CommandContext,info, url , edit = False):
    chapter = info[0]
    page = info[1]
    language = info[2]
    scanlation = info[3]
    embed= interactions.Embed(
        title=f"Chapter {chapter}, page {page}:",
        url=url,
        image= interactions.EmbedImageStruct(
            url= url,
        )
    )
    embed.set_footer(f"{language} by \"{scanlation}\"")
    if url and not edit:
        await ctx.send(components=seek_buttons,embeds=[embed])
    elif url:
        await ctx.edit(components=seek_buttons,embeds=[embed])
    else:
        await ctx.send("page not found",ephemeral=True)


frist_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="frist",
    custom_id="frist"
)
prev_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="prev",
    custom_id="prev"
)

next_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="next",
    custom_id="next"
)

last_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="last",
    custom_id="last"
)

seek_buttons = interactions.ActionRow.new(frist_button,prev_button,next_button,last_button)


def getembedinfo(embed:Embed):
    top_match = re.findall(r"[0-9.]+",embed.title)
    chapter = top_match[0]
    page = top_match[1]
    footer = embed.footer.text
    language = footer.split(" ")[0]
    scanlation = re.search(r"\"([\w ]+)\"",footer).group(1)
    return chapter, page,language,scanlation


@bot.command(
    name="getpage",
    description="get page of magna",
    scope=831951877158731797,
    options = [
        interactions.Option(
            name="chapter",
            description="chapter to get",
            type=interactions.OptionType.STRING,
            required=True,
        ),        interactions.Option(
            name="page",
            description="page to get",
            type=interactions.OptionType.STRING,
            required=True,
        ),        interactions.Option(
            name="language",
            description="language to get",
            type=interactions.OptionType.STRING,
            required=False,
        ),        interactions.Option(
            name="scanlation",
            description="scanlation to get",
            type=interactions.OptionType.STRING,
            required=False,
        )
    ],
)




async def execgetpage(
    ctx: interactions.CommandContext,
    chapter: str,
    page: str,
    language = os.getenv("DEFAULT_LANG"),
    scanlation = os.getenv("DEFAULT_TRASNLATION"),
):
    info, url = getpage(index,[chapter,page,language,scanlation])
    await sendpage(ctx,info,url)

@bot.component("frist")
async def execNext(ctx : interactions.CommandContext):
    if ctx.member.id._snowflake != ctx.message.interaction.user.id._snowflake:
        await ctx.send("",ephemeral=True)
    info, nextpage = getfristpage(index,getembedinfo(ctx.message.embeds[0]))
    await sendpage(ctx,info,nextpage,edit=True)

@bot.component("prev")
async def execNext(ctx : interactions.CommandContext):
    if ctx.member.id._snowflake != ctx.message.interaction.user.id._snowflake:
        await ctx.send("",ephemeral=True)
    info, nextpage = getprevpage(index,getembedinfo(ctx.message.embeds[0]))
    await sendpage(ctx,info,nextpage,edit=True)

@bot.component("next")
async def execNext(ctx : interactions.CommandContext):
    if ctx.member.id._snowflake != ctx.message.interaction.user.id._snowflake:
        await ctx.send("",ephemeral=True)
    info, nextpage = getnextpage(index,getembedinfo(ctx.message.embeds[0]))
    await sendpage(ctx,info,nextpage,edit=True)

@bot.component("last")
async def execNext(ctx : interactions.CommandContext):
    if ctx.member.id._snowflake != ctx.message.interaction.user.id._snowflake:
        await ctx.send("",ephemeral=True)
    info, nextpage = getlastpage(index,getembedinfo(ctx.message.embeds[0]))
    await sendpage(ctx,info,nextpage,edit=True)



bot.start()