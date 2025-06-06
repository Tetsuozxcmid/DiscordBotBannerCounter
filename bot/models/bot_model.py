from PIL import Image
import discord
import pytz
from discord.ext import commands, tasks
import datetime
from core.BotSettings.config import settings
from models.banner_model import banner_proccesor
from io import BytesIO


class Bot(commands.Bot):
    def __init__(self):
        self.bot_token = settings.bot_token
        self.messages_from_users = {}
        self.members_all = {}
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(intents=intents,
                         command_prefix='!',
                         description='Banner Updating Counter Bot',
                         )

        @self.command(name='get_info')
        async def get_info(ctx):
            guild = self.get_guild(settings.server_id)
            voice_users = sum(len(vc.members) for vc in guild.voice_channels)
            most_active_member, message_count = max(
                self.messages_from_users.items(), key=lambda x: x[1])
            member_count = guild.member_count
            timeout = datetime.datetime.now(
                pytz.timezone('Europe/Moscow')).strftime('%H:%M')

            response = {
                'all_members': member_count,
                'voice_users': voice_users,
                'most_active': most_active_member.name,
                'time': timeout
            }

            await ctx.send(str(response))

        @self.command(name='get_info_by_user')
        async def get_info_by_user(ctx, target_user: str):
            guild = self.get_guild(settings.server_id)
            if not guild:
                return await ctx.send("Сервер не найден")

            found_member = None
            for member in guild.members:
                if target_user.lower() == member.name.lower():
                    found_member = member
                    break

            user_messages = []
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=100):
                        if message.author == found_member:
                            user_messages.append(message.content)

                except discord.Forbidden:
                    continue
            response = {
                'author': found_member.name,
                'message': user_messages
            }
            await ctx.send(str(response))

    async def on_ready(self):
        self.updating_banner_and_timezone.start()
        self.remove_command('help')

    @tasks.loop(seconds=3)
    async def updating_banner_and_timezone(self):
        self.messages_from_users = {}

        guild = self.get_guild(settings.server_id)
        if not guild:
            print(f"server with id {settings.server_id} not found! ")

        getting_time_past = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        timeout = datetime.datetime.now(
            pytz.timezone('Europe/Moscow')).strftime('%H:%M')

        for channels in guild.text_channels:
            try:
                async for message in channels.history(limit=100):
                    if message.author and not message.author.bot:
                        self.messages_from_users[message.author] = self.messages_from_users.get(
                            message.author, 0) + 1
            except Exception as e:
                print(f"error in {channels.name}: {e}")

        for member in guild.members:
            if not member.bot:
                if member.name not in self.members_all:
                    self.members_all[member.name] = self.members_all.get(
                        member.name, 0) + 1

        try:

            most_active_member, message_count = max(
                self.messages_from_users.items(), key=lambda x: x[1])
            print(
                f"most active is {most_active_member.name} -- {message_count} messages got")

            self.guild = self.get_guild(settings.server_id)

            voice_users = sum(len(vc.members) for vc in guild.voice_channels)
            print(f"users in voice {voice_users}")

            member_count = guild.member_count
            print(f"Members {member_count}")

            print(f"{self.members_all}")

            banner = await banner_proccesor.process_banner(
                activity=str(member_count),
                voice_users=voice_users,
                most_active_member=most_active_member,
                timeout=timeout
            )

            banner.save("current_banner.png")

            with BytesIO() as ImageBinary:
                banner.save(ImageBinary, "png")
                ImageBinary.seek(0)
                await self.guild.edit(banner=ImageBinary.read())

        except discord.DiscordException as e:
            print(f"Ошибка Discord API: {e}")

        except (IOError, Image.DecompressionBombError) as e:
            print(f"Ошибка обработки изображения: {e}")

        except ValueError as e:
            print(f"Ошибка данных: {e}")

        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
