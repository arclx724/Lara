import sys
from pyrogram import Client
import config
from logging import getLogger

LOGGER = getLogger(__name__)

assistants = []
assistantids = []

class Userbot:
    def __init__(self):
        self.one = Client(
            name="ShrutiAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="ShrutiAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="ShrutiAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="ShrutiAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="ShrutiAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER.info("Starting Assistants...")
        
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat(config.LOG_GROUP_ID)
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOG_GROUP_ID, "✅ Assistant 1 Started Successfully")
            except:
                LOGGER.error(
                    "Assistant Account 1 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER.info(f"Assistant 1 Started as {self.one.name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat(config.LOG_GROUP_ID)
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOG_GROUP_ID, "✅ Assistant 2 Started Successfully")
            except:
                LOGGER.error(
                    "Assistant Account 2 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER.info(f"Assistant 2 Started as {self.two.name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat(config.LOG_GROUP_ID)
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOG_GROUP_ID, "✅ Assistant 3 Started Successfully")
            except:
                LOGGER.error(
                    "Assistant Account 3 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER.info(f"Assistant 3 Started as {self.three.name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat(config.LOG_GROUP_ID)
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOG_GROUP_ID, "✅ Assistant 4 Started Successfully")
            except:
                LOGGER.error(
                    "Assistant Account 4 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER.info(f"Assistant 4 Started as {self.four.name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat(config.LOG_GROUP_ID)
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOG_GROUP_ID, "✅ Assistant 5 Started Successfully")
            except:
                LOGGER.error(
                    "Assistant Account 5 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER.info(f"Assistant 5 Started as {self.five.name}")

    async def stop(self):
        LOGGER.info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
            
