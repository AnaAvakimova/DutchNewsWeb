from django.db import models
from django.utils import timezone
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File


class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=5000)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/')
    image_url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}", File(img_temp))
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
