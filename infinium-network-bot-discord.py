import requests
import discord
from discord.ext import commands

BOT_TOKEN = "TOKEN"  # Replace with your bot token
API_URL = "https://explorer.infinium.space/api/get_info/4294967295"

def get_info():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def format_hashrate(hashrate):
    units = ["H/s", "KH/s", "MH/s", "GH/s", "TH/s", "PH/s", "EH/s"]
    index = 0

    while hashrate >= 1000 and index < len(units) - 1:
        hashrate /= 1000
        index += 1

    return f"{hashrate:.2f} {units[index]}"

@commands.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="Infinium Network - Help",
        description="**Here is the list of available commands:**",
        color=0x5A9EC9
    )

    embed.add_field(name="!info", value="Displays basic information about Infinium.", inline=False)
    embed.add_field(name="!network", value="Displays statistics for the Infinium Network.", inline=False)
    embed.add_field(name="!price", value="Get the price of Infinium.", inline=False)
    embed.add_field(name="!donate", value="Shows addresses to donate to the project.\n", inline=False)

    embed.set_footer(text="Use the command with '!' followed by the command name.")
    embed.set_thumbnail(url="https://infinium.space/assets/img/icons/infinium_wordmark_color.png")
    await ctx.send(embed=embed)

@commands.command(name="info")
async def info_command(ctx):
    embed = discord.Embed(
        title="Infinium Network Information",
        description=(
            f"Infinium is Digital Currency You Can Spend Anywhere. Use Infinium to make secure, instant, private payments online or in-store using our secure open-source platform hosted by thousands of users around the world.\n\n"
            f" * **[Website](https://infinium.space)**\n"
            f" * **[Wallets](https://github.com/Infinium-8/Infinium/releases)**\n"
            f" * **[Pools](https://miningpoolstats.stream/infinium/)**\n"
            f" * **[Exchanges](https://infinium.space/ecosystem/exchanges/)**\n"
            f" * **[Explorer](https://explorer.infinium.space/)**\n"
            f" * **[Documentation](https://docs.infinium.space/)**\n"
            f" * **[GitHub](https://github.com/Infinium-8/)**\n"
            f" * **[Social](https://infinium.space/community/social/):** \n"
            f"  - **[Discord](https://discord.gg/6xF9EY6ZQr)**\n"
            f"  - **[Twitter](https://twitter.com/Infinium_8)**\n"
            f"  - **[Telegram](https://t.me/InfiniumGlobal)**\n"
        ),
        color=0x5A9EC9
    )
    embed.set_thumbnail(url="https://infinium.space/assets/img/icons/infinium_wordmark_color.png")
    await ctx.send(embed=embed)

@commands.command(name="network")
async def network_command(ctx):
        network = get_info()

        ticket = "INF"
        result = network.get("result", {})
        height = result.get("height", "N/A")
        hashrate = result.get("current_network_hashrate_50", "N/A")
        block_reward = result.get("block_reward", "N/A")
        minimum_fee = result.get("minimum_fee", "N/A")
        total_alias = result.get("alias_count", "N/A")
        tx_pool_size = result.get("tx_pool_size", "N/A")
        tx_count = result.get("tx_count", "N/A")
        last_block_hash = result.get("last_block_hash", "N/A")
        total_coins_str = result.get("total_coins", "N/A")
        transactions_cnt_per_day = result.get("transactions_cnt_per_day", "N/A")
        transactions_volume_per_day = result.get("transactions_volume_per_day", "N/A")

        try:
            total_coins = round(float(total_coins_str) / 10**8, 2)
            minimum_fee = round(float(minimum_fee) / 10**8, 2)
            transactions_volume_per_day = float(transactions_volume_per_day) / 10**8
            hashrate = format_hashrate(hashrate)
        except ValueError:
            total_coins = "N/A"
            minimum_fee = "N/A"
            transactions_volume_per_day = "N/A"


        embed = discord.Embed(
            title="Infinium Network Stats",
            description=(
                f" *Block Height:* `{height}`\n"
                f" *Total Network Hashrate:* `{hashrate}`\n"
                f" *Circulation Emission:* `{total_coins} {ticket}`\n"
                f" *Total TX Count:* `{tx_count}`\n"
                f" *Total Number of Registered Aliases:* `{total_alias}`\n"
                f" *Total Coin Supply:* `Infinite`\n"
                f" *Block Reward POW:* `{block_reward/10**8} {ticket}`\n"
                f" *Block Reward POS:* `{block_reward/10**8} {ticket}`\n"
                f" *Minimum Network Fee:* `{minimum_fee} {ticket}`\n"            
                f" *Transactions made in 24h:* `{transactions_cnt_per_day}`\n"
                f" *Transactions volume in 24h :* `{transactions_volume_per_day} {ticket}`\n"
                f" *Mempool TX Count:* `{tx_pool_size}`\n"
                f" *Last Block Hash:* [{last_block_hash}](https://explorer.infinium.space/block/{last_block_hash})\n\n"
                f"🔍 _Data obtained directly from the browser._"
            ),
            color=0x5A9EC9
        )
        embed.set_thumbnail(url="https://infinium.space/assets/img/icons/infinium_wordmark_color.png")
        await ctx.send(embed=embed)

@commands.command(name="price")
async def price_command(ctx, pair: str = "inf/usdt"):

    base_url = "https://api.xeggex.com/api/v2/ticker/"
    api_url = f"{base_url}{pair}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        last_price = data.get('last_price', 'N/A')
        high_price = data.get('high', 'N/A')
        low_price = data.get('low', 'N/A')
        target_currency = data.get('target_currency', 'N/A')
 
        if last_price != 'N/A':
            
            message = (
                f"📊 **Price for {pair.upper()}**\n\n"
                f"Last: {last_price} {target_currency}\n"
                f"Hight: {high_price} {target_currency}\n"
                f"Low: {low_price} {target_currency}\n\n"
                f"🔍 _Data obtained directly from the Xeggex Exchange._"
            )
        else:
            message = f"⚠️ No data found for the pair {pair.upper()}."
    except requests.exceptions.RequestException as e:
        message = f"⚠️ Error getting data: {e}"

    await ctx.send(message)


@commands.command(name="donate")
async def donate_command(ctx):
    message = (
            f" **`Crowdfunding`**\n\n"
            f" **BTC:** bc1q2e9kxhpxg59a573rkk5wk66n5y493eras9mq3d\n\n"
            f" **LTC:** ltc1q40j7rltqxfhja687gh0qmaa3p7pw4glps4sep5\n\n"
            f" **DOGE:** DF4EbEJnvdoq3nPhshG3zEFS47QBJ54B3f\n\n"
            f" **INF:** inf1guboUTvbBTQfapqET8Tf5oCMrZ3Qz32wny78Z6iu6XKDbBhTfiyL6FSG8mtuMEG2km3Wik3RdDY86ffaQs4N1NsNvyNgpe\n\n"
            f" **RTO:** ADxTWxPhhydhRDjAXfBYNF5qgMQ11Ry9SZwPpWqHadeWR5LFhMLKLkqJvCJ1v1cJ3MZW68fY6roJw3nK4mMp17TyMfTJTey\n\n"
            f" **XEQ:** TvzNex9M52wPGpQxJ3ycg4PMcWDo2Gy89Jjp3RrEMiMbfcQZz2m6kkJeh6AJcDAQXEi317AKxMqScG54qgDaBkMV2VYbfpPtR\n\n"
            f" **XMR:** 42Qd3kfwebtNZJGjNPgnNkUYmxkbKdmXGhd5o4pxrnG1W1wUYXx8GdNY2BU3ZhKJuMGSM48vWUk2iTBJfUEA8dNu8PjWb5t\n\n"
            f" **LTHN:** iz5Ys6WP4zFTF323uBfrePBELQax7b4PSaEnMWsm2f5ME3S62Z46sp3G55QSmz3zisDqfaF9aX9LJfxp2Tyz5E8j11LGoqJ1u\n\n"
            f" **GNTL:** gnt1jU5mwbALfjKsKJWt8HXHbaVNLf6oaExdmXpLqoDQGmdAodrpS73jXCuDPwEUHhTEDq5qDbq116XQVSCYE2E49EWyD1bZTd\n\n"
            f" **MRL:** emo1eSwJ8gXZwQNSVLQjLpemWRX8f5oeD9U5dkt6MXm8APU6bH2f3BERUYstpgDsQTChd746PGFDQ1uc1cNdJ1Fn7mY21DnpUK\n\n"
    )
    await ctx.send(message)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
bot.add_command(help_command)
bot.add_command(info_command)
bot.add_command(network_command)
bot.add_command(price_command)
bot.add_command(donate_command)
bot.run(BOT_TOKEN)
