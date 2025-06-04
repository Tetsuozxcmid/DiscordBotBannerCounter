from PIL import Image
import discord
import pytz
from discord.ext import commands, tasks
import datetime
from core.BotSettings.config import settings
from models.banner_model import banner_proccesor


class Bot(commands.Bot):
    def __init__(self):
        self.bot_token = settings.token
        self.messages_from_users = {}
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(intents=intents,
                         command_prefix='!',
                         description='Banner Updating Counter Bot',
                         )

    async def bot_ready_to_use(self):
        self.banner_update_counter.start()
        self.remove_command('help')

    @tasks.loop(seconds=10)
    async def updating_banner_and_timezone(self):
        getting_time_past = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

        getting_timezone = datetime.datetime.now(
            pytz.timezone('Europe/Moscow'))
        timeout = getting_timezone("%H:%M")

        guild = self.get_guild(settings.server_id)
        async for channels in guild.text_channels:
            async for message in channels.history(after=getting_time_past):
                members = guild.members
                if message.author not in members and not message.author.bot:
                    self.messages_from_users[message.author] += 1

        try:
            most_active_member = max(
                self.messages_from_users, key=self.messages_from_users.get)

            self.guild = self.get_guild(settings.server_id)

            for vc in self.guild.voice_channels:
                voice_users = sum(len(vc.members))

            server_members = len(self.guild.members)

            banner_proccesor.draw_most_active_member(
                draw=self.draw, most_active_member=most_active_member)
            
            banner_proccesor._draw_time(draw=self.draw, timeout=timeout)

            banner_proccesor._draw_activity(
                draw=self.draw, activity=server_members)
            
            banner_proccesor._draw_voice_users(
                draw=self.draw, voice_users=voice_users)
            
        except discord.DiscordException as e:
            print(f"Ошибка Discord API: {e}")

        except (IOError, Image.DecompressionBombError) as e:
            print(f"Ошибка обработки изображения: {e}")

        except ValueError as e:
            print(f"Ошибка данных: {e}")
            
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
