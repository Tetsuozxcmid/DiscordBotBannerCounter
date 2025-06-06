from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import aiohttp


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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(most_active_member.display_avatar.url)) as resp:
                    avatar_data = await resp.read()

            avatar_img = Image.open(io.BytesIO(avatar_data))
            avatar_img = avatar_img.convert('RGBA')
            avatar_img = ImageOps.fit(avatar_img, (320, 320),
                                      method=Image.LANCZOS,
                                      centering=(0.5, 0.5))

            mask = Image.new('L', (320, 320), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, 320, 320), fill=255)
            avatar_img.putalpha(mask)

            self.banner.paste(avatar_img, (227, 601), avatar_img)

            font = ImageFont.truetype(self.fonts['status'], size=96)
            draw.text(
                (1608, 807), most_active_member.name[:20], font=font, fill="white")

        except Exception as e:
            print(f"Ошибка при обработке аватара: {e}")

    async def _draw_time(self, draw: ImageDraw, timeout):
        font = ImageFont.truetype(self.fonts['status'], size=96)
        draw.text((1608, 807), f"{timeout}", font=font, fill="white")


banner_proccesor = BannerProcessor()
