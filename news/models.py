from django.db import models
from django.utils import timezone
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from PIL import Image
import io

class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=5000)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/')
    image_url = models.URLField(null=True)

    def compress_image(self, image):
        im = Image.open(image)
        # Convert to RGB if image is in RGBA mode
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        # Resize the image
        im.thumbnail((800, 800))
        # Save the image to a buffer
        buffer = io.BytesIO()
        im.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        return buffer

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            compressed_image = self.compress_image(img_temp)
            self.image.save(f"image_{self.pk}.jpg", File(compressed_image), save=False)
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
