from PIL import Image, ImageDraw, ImageFont, ImageOps
import io


class BannerProcessor:
    def __init__(self, template_path: str = "BannerLite.png"):
        self.font_size = 85
        self.position = (600, 600)  # example
        self.template_path = template_path
        self.fonts = {
            'status': "status.ttf",
            'montserrat': "ofont.ru_Montserrat.ttf",
            'name': "name.ttf"
        }

    async def process_banner(self, activity, voice_users: int,
                             most_active_member: str, timeout: str):
        try:
            banner = Image.open(self.template_path)
            draw = ImageDraw.Draw(banner)

            self._draw_activity(draw, activity)
            self._draw_voice_users(draw, voice_users)
            self.draw_active_member(draw, most_active_member)
            self._draw_time(draw, timeout)

            return banner
        except Exception as e:
            raise ValueError(f"Ошибка при обработке баннера: {str(e)}")

    async def _draw_activity(self, draw: ImageDraw.Draw, activity):

        if activity != None:
            font = ImageFont.truetype(
                self.fonts['status'], size=self.font_size)
            draw.text((self.position), f"{self.activity.name}"[:20], font=font)
        else:
            draw.text((615, 777), "Статус не задан", font=font)

    async def _draw_voice_users(self, draw: ImageDraw, voice_users: int):
        if voice_users < 5:
            font = ImageFont.truetype(
                self.fonts['status'], size=self.font_size)
            draw.text((1608, 807), f"{voice_users}", font=font, fill="white")
        else:
            font = ImageFont.truetype(
                self.fonts['montserrat'], size=self.font_size)
            draw.text((1608, 807), f"{voice_users}", font=font, fill="white")

    async def draw_most_active_member(self, draw: ImageDraw, most_active_member):
        user_image = str(most_active_member.display_avatar.url)[:10]
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = ImageOps.fit(response, (320, 320),
                                method=Image.LANCZOS, centering=(0.5, 0.5))
        mask = Image.new('L', (320, 320), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 320, 320), fill=255)
        response.putalpha(mask)

        self.banner.paste(response, (227, 601), response)
        font = ImageFont.truetype(self.fonts['status'], size=96)
        draw.text(
            (1608, 807), f"{most_active_member.name}", font=font, fill="white")

    async def _draw_time(self, draw: ImageDraw, timeout):
        font = ImageFont.truetype(self.fonts['status'], size=96)
        draw.text((1608, 807), f"{timeout}", font=font, fill="white")


banner_proccesor = BannerProcessor()
