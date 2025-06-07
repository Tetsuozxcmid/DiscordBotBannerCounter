from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import aiohttp
import os

class BannerProcessor:
    def __init__(self, template_path: str = "BannerLite.png"):
        self.width = 1590
        self.height = 350
        self.font_size = 15
        self.position = (50, 50)
        self.template_path = template_path
        
        try:
            self.fonts = {
                'status': ImageFont.truetype("arial.ttf", size=25),
                'montserrat': ImageFont.truetype("arial.ttf", size=25),
                'name': ImageFont.truetype("arial.ttf", size=25)
            }
        except:
            
            self.fonts = {
                'status': ImageFont.load_default(),
                'montserrat': ImageFont.load_default(),
                'name': ImageFont.load_default()
            }

    def process_banner(self, activity, voice_users: int,
                           most_active_member, timeout: str):
        try:

            banner = Image.open(self.template_path)
            draw = ImageDraw.Draw(banner)

            
            self._draw_activity(draw, activity)
            self._draw_voice_users(draw, voice_users)
            self._draw_active_member( draw, most_active_member)
            self._draw_time(draw, timeout)

            return banner

        except Exception as e:
            raise ValueError(f"Ошибка при обработке баннера: {str(e)}")

    def _draw_activity(self, draw: ImageDraw.Draw, activity):
        x, y = 20, 20
        text = f"Активность: {activity if activity else 'Нет данных'}"[:30]
        draw.text((x, y), text, font=self.fonts['status'], fill="white")

    def _draw_voice_users(self, draw: ImageDraw.Draw, voice_users: int):
        x, y = self.width // 2, 20
        text = f"В голосовых: {voice_users}"
        draw.text((x, y), text, font=self.fonts['status'], fill="white")

    def _draw_active_member(self, draw: ImageDraw.Draw, member):
        x, y = 60, self.height // 3
        name = str(getattr(member, 'name', member))[:20]
        text = f"Самый активный: {name}"
        draw.text((x, y), text, font=self.fonts['status'], fill="white")

    def _draw_time(self, draw: ImageDraw.Draw, timeout: str):
        x, y = self.width // 2, self.height // 3
        draw.text((x, y), f"Время: {timeout}", font=self.fonts['status'], fill="white")


banner_proccesor = BannerProcessor()
