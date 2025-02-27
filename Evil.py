import logging
from decouple import config
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantsRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChannelParticipantsBanned
from telethon.tl.types import ChannelParticipantsKicked
from telethon.tl.types import Message
from time import sleep
from telethon.tl.types import InputUser
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator


BOT_TOKEN = config("BOT_TOKEN", "6964909307:AAGroKLtu2c2RO2ovbymnuSai_dHMVgEa-M")
EVILS = [760067286, 760067286]
ALTRONS = [-1001784672307]
sudo_users_str = config("SUDO", default="")
SUDO_USERS = list(map(int, sudo_users_str.split()))
YOUR_DESTINATION_CHANNEL_ID = -1001784672307  # Replace with your actual destination channel ID

# Add your ID to the SUDO_USERS list
SUDO_USERS.append(760067286)

RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

logging.basicConfig(level=logging.INFO)
client = TelegramClient('EVIL', 22418774, "d8c8dab274f9a811814a6a96d044028e").start(bot_token=BOT_TOKEN)

# Dictionary to store chat-specific spam information
spam_info = {}


@client.on(events.NewMessage(pattern=r'/spam'))
async def spam_command(event):
    # Extract the message from the command
    message_to_spam = event.text.split('/spam', 1)[1].strip()

    # Get the chat ID
    chat_id = event.chat_id

    # Check if the chat is not in the spam_info dictionary, or if it's not spamming
    if chat_id not in spam_info or not spam_info[chat_id]['spamming']:
        # Initialize spam_info for the chat
        spam_info[chat_id] = {'spamming': True, 'message_to_spam': message_to_spam}

        # Start the spamming loop
        while spam_info[chat_id]['spamming']:
            await event.respond(message_to_spam)
            sleep(10)  # Wait for 10 seconds between each spam message
    else:
        # Stop spamming if already spamming
        spam_info[chat_id]['spamming'] = False
        await event.respond("Spamming stopped.")


@client.on(events.NewMessage(pattern=r'/bamall -\d+', chats=None))
async def bam_all(event):
    channel_id = int(event.text.split()[1])  # Extract channel ID from the command
    async for user in client.iter_participants(channel_id):
        try:
            await client(EditBannedRequest(channel_id, user.id, RIGHTS))
            print(f"Banned user: {user.id}")
        except Exception as e:
            print(f"Error banning user {user.id}: {e}")

@client.on(events.NewMessage(pattern=r'/banall -\d+', chats=None))
async def ban_all(event):
    channel_id = int(event.text.split()[1])  # Extract channel ID from the command
    try:
        async for user in client.iter_participants(channel_id):
            try:
                await client(EditBannedRequest(channel_id, user.id, ChatBannedRights(until_date=0, view_messages=True)))
                print(f"Banned user: {user.id}")
            except Exception as e:
                print(f"Error banning user {user.id}: {e}")
                # Sleep for a few seconds in case of an error
                sleep(5)
    except Exception as e:
        print(f"Error getting participants: {e}")

client.run_until_disconnected()

@client.on(events.NewMessage(pattern=r'/unbanall', chats=None))
async def unban_all(event):
    if event.sender_id not in SUDO_USERS:
        return  # Only allow sudo users to execute this command

    await event.reply("Initiating unban process. This may take some time...")

    try:
        # Fetch kicked participants using GetParticipantsRequest
        participants = await client(GetParticipantsRequest(channel=event.chat_id, filter=ChannelParticipantsKicked()))

        unban_count = 0  # Initialize the counter
        for participant in participants.users:
            try:
                # Unban each participant
                await client(EditBannedRequest(event.chat_id, participant.id, ChatBannedRights(until_date=0, view_messages=True)))
                unban_count += 1  # Increment the counter for each successful unban
            except Exception as e:
                print(f"Error unbanning user {participant.id}: {e}")

    except Exception as e:
        print(f"Error getting participants: {e}")
        return

    print(f"Unbanned {unban_count} users successfully.")
    await event.reply(f"Unbanned {unban_count} users successfully.")

client.run_until_disconnected()
@client.on(events.NewMessage(pattern="^/bamsall"))
async def banall(event):
    if event.sender_id in SUDO_USERS:
        await event.delete()
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        all = 0
        bann = 0
        if int(event.chat_id) in ALTRONS:
            return
        async for user in event.client.iter_participants(event.chat_id):
            all += 1
            try:
                if user.id not in admins_id and user.id not in EVILS:
                    await event.client(EditBannedRequest(event.chat_id, user.id, RIGHTS))
                    bann += 1
            except Exception as e:
                pass

print("TRIPPY OP")

client.run_until_disconnected()
                 
