import requests

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, DisconnectEvent, CommentEvent, GiftEvent
from TikTokLive.client.logger import LogLevel


TIKTOK_USERNAME = "cheler48"

BRIDGE_URL = "http://127.0.0.1:5000/gift"

SECRET = "cheler48_bridge_2026"


client = TikTokLiveClient(
    unique_id=TIKTOK_USERNAME
)


def send_gift_to_bridge(username, gift_name, coins):

    data = {
        "secret": SECRET,
        "username": username,
        "gift": gift_name,
        "coins": coins
    }

    try:

        response = requests.post(
            BRIDGE_URL,
            json=data,
            timeout=5
        )

        if response.ok:

            print()
            print("================================")
            print("TRIMIS CATRE ROBLOX BRIDGE!")
            print("Username:", username)
            print("Gift:", gift_name)
            print("Coins:", coins)
            print("================================")
            print()

        else:

            print(
                "Bridge error:",
                response.status_code,
                response.text
            )

    except Exception as e:

        print()
        print("NU POT CONTACTA BRIDGE-UL!")
        print("Eroare:", e)
        print()


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):

    print()
    print("========================================")
    print("CONECTAT LA TIKTOK LIVE!")
    print("Username:", TIKTOK_USERNAME)
    print("Room ID:", client.room_id)
    print("========================================")
    print()


@client.on(DisconnectEvent)
async def on_disconnect(event: DisconnectEvent):

    print()
    print("TIKTOK LIVE S-A DECONECTAT")
    print()


@client.on(CommentEvent)
async def on_comment(event: CommentEvent):

    username = event.user.unique_id
    comment = event.comment

    print(
        "[COMMENT]",
        username,
        ":",
        comment
    )


@client.on(GiftEvent)
async def on_gift(event: GiftEvent):

    username = event.user.unique_id

    gift_name = event.gift.name

    coins = getattr(
        event.gift,
        "diamond_count",
        0
    )

    print()
    print("================================")
    print("GIFT PRIMIT!")
    print("Username:", username)
    print("Gift:", gift_name)
    print("Coins:", coins)
    print("================================")
    print()

    if coins in [1, 5, 10, 30]:

        send_gift_to_bridge(
            username,
            gift_name,
            coins
        )

    else:

        print(
            "Gift ignorat deoarece valoarea nu este 1/5/10/30 coins."
        )


if __name__ == "__main__":

    print("========================================")
    print("       TIKTOK ROBLOX CONNECTOR")
    print("========================================")
    print("Cont TikTok:", TIKTOK_USERNAME)
    print("Bridge:", BRIDGE_URL)
    print("Pornesc conectarea...")
    print()

    client.logger.setLevel(
        LogLevel.INFO.value
    )

    client.run()