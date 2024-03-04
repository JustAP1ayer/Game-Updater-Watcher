import iso8601
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import asyncio
import json
import time
with open("settings.json", "r") as config_file:
    config = json.load(config_file)

session = requests.session()
session.cookies['.ROBLOSECURITY'] = config["roblosecurityCookie"]
token = None
# ty frames for this code 💋
def _set_auth():
    global token, session
    try:
        conn = session.post("https://auth.roblox.com/v2/logout")
        if conn.headers.get("x-csrf-token"):
            token = conn.headers["x-csrf-token"]
    except:
        time.sleep(5)
        return _set_auth()
    
_set_auth()

headersxd = {
    'Content-Type': 'application/json',
    "x-csrf-token": token
}
print(token)
async def send_webhook(webhook_url, embed, game_id, unix_timestamp):
    webhook = DiscordWebhook(webhook_url, content="@everyone")
    webhook.add_embed(embed)
    embed.set_timestamp()
    response = webhook.execute()
    print("Message sent")

    with open("cookielogger.json", 'r') as json_file:
        data = json.load(json_file)

    data[str(game_id)] = unix_timestamp

    with open("cookielogger.json", 'w') as json_file:
        json.dump(data, json_file, indent=2)


async def check_game():
    try:
        for game_id in config["game_ids"]:
            eco_url = f"https://economy.roblox.com/v2/assets/{game_id}/details"
            eco_response = requests.get(eco_url)
            
            if eco_response.status_code == 200:
                eco_data = eco_response.json()
                eco_name = eco_data.get("Name")
                update = eco_data.get("Updated")
                dt_object = iso8601.parse_date(update)
                unix_timestamp = int(dt_object.timestamp())

                with open("cookielogger.json", 'r') as json_file:
                    data = json.load(json_file)

                if str(game_id) not in data:
                    data[str(game_id)] = unix_timestamp
                    with open("cookielogger.json", 'w') as json_file:
                        json.dump(data, json_file, indent=2)

                    game_url = f"https://www.roblox.com/places/api-get-details?assetId={game_id}"
                    game_response = session.get(game_url, headers=headersxd)
                    
                    if game_response.status_code == 200:
                        game_data = game_response.json()
                        owner = game_data.get("Builder")
                        probition = game_data.get("ReasonProhibited")
                        if probition == "AnonymousAccessProhibited":
                            _set_auth()
                            game_response = session.get(game_url, headers=headersxd)
                            game_data = game_response.json()
                            probition = game_data.get("ReasonProhibited")
                        if probition != "None" and probition is not None:
                            reason = game_data.get("ReasonProhibitedMessage")
                            embed = DiscordEmbed(
                                title=f"{eco_name} HAS UPDATED",
                                description=f"``Game`` - **https://www.roblox.com/games/{game_id}/redblue**\n``Owner`` - **{owner}**\n``Previous Time Updated`` - **<t:{data[str(game_id)]}:R>** **|** **<t:{data[str(game_id)]}>**\n``Time Updated`` - **<t:{unix_timestamp}:R>** **|** **<t:{unix_timestamp}>**\n``⚠️`` - **{probition}** ({reason})"
                            )
                        else:
                            embed = DiscordEmbed(
                                title=f"{eco_name} HAS UPDATED",
                                description=f"``Game`` - **https://www.roblox.com/games/{game_id}/redblue**\n``Owner`` - **{owner}**\n``Previous Time Updated`` - **<t:{data[str(game_id)]}:R>** **|** **<t:{data[str(game_id)]}>**\n``Time Updated`` - **<t:{unix_timestamp}:R>** **|** **<t:{unix_timestamp}>**"
                            )

                        thumbnail_response = requests.get(
                            f"https://thumbnails.roblox.com/v1/places/gameicons?placeIds={game_id}&returnPolicy=PlaceHolder&size=128x128&format=Png&isCircular=false")
                        
                        if thumbnail_response.status_code == 200:
                            thumbnail_data = thumbnail_response.json()
                            thumbnail = thumbnail_data["data"][0]["imageUrl"]
                            embed.set_thumbnail(url=thumbnail)

                        await send_webhook(config["webhook"], embed, game_id, unix_timestamp)

                elif data[str(game_id)] != unix_timestamp:
                    game_url = f"https://www.roblox.com/places/api-get-details?assetId={game_id}"
                    game_response = session.get(game_url, headers=headersxd)
                    
                    if game_response.status_code == 200:
                        game_data = game_response.json()
                        owner = game_data.get("Builder")
                        probition = game_data.get("ReasonProhibited")
                        if probition == "AnonymousAccessProhibited":
                            _set_auth()
                            game_response = session.get(game_url, headers=headersxd)
                            game_data = game_response.json()
                            probition = game_data.get("ReasonProhibited")
                        if probition != "None" and probition is not None:
                            reason = game_data.get("ReasonProhibitedMessage")
                            embed = DiscordEmbed(
                                title=f"{eco_name} HAS UPDATED",
                                description=f"``Game`` - **https://www.roblox.com/games/{game_id}/redblue**\n``Owner`` - **{owner}**\n``Previous Time Updated`` - **<t:{data[str(game_id)]}:R>** **|** **<t:{data[str(game_id)]}>**\n``Time Updated`` - **<t:{unix_timestamp}:R>** **|** **<t:{unix_timestamp}>**\n``⚠️`` - **{probition}** ({reason})"
                            )
                        else:
                            embed = DiscordEmbed(
                                title=f"{eco_name} HAS UPDATED",
                                description=f"``Game`` - **https://www.roblox.com/games/{game_id}/redblue**\n``Owner`` - **{owner}**\n``Previous Time Updated`` - **<t:{data[str(game_id)]}:R>** **|** **<t:{data[str(game_id)]}>**\n``Time Updated`` - **<t:{unix_timestamp}:R>** **|** **<t:{unix_timestamp}>**"
                            )

                        thumbnail_response = requests.get(
                            f"https://thumbnails.roblox.com/v1/places/gameicons?placeIds={game_id}&returnPolicy=PlaceHolder&size=128x128&format=Png&isCircular=false")
                        
                        if thumbnail_response.status_code == 200:
                            thumbnail_data = thumbnail_response.json()
                            thumbnail = thumbnail_data["data"][0]["imageUrl"]
                            embed.set_thumbnail(url=thumbnail)

                        await send_webhook(config["webhook"], embed, game_id, unix_timestamp)
                        data[str(game_id)] = unix_timestamp
                        with open("cookielogger.json", 'w') as json_file:
                            json.dump(data, json_file, indent=2)
    except Exception as e:
        print(e)

async def main():
    while True:
        task = asyncio.create_task(check_game())
        await task
        await asyncio.sleep(config['watch_speed'])

asyncio.run(main())
