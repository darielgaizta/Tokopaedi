from django.db import models

# For creating thumbnails
from django.core.files import File

# For handling images
from PIL import Image
from io import BytesIO

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()

	class Meta:
		# Data will be ordered by its name
		ordering = ('name',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return f'/{self.slug}/'

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	image = models.ImageField(upload_to='uploads/', blank=True, null=True)
	thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		# Data will be ordered by its name
		ordering = ('name',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return f'/{self.category.slug}/{self.slug}/'

	def get_image(self):
		if self.image:
			return 'http://127.0.0.1:8000' + self.image.url
		return ''

	def get_thumbnail(self):
		if self.thumbnail:
			return 'http://127.0.0.1:8000' + self.thumbnail.url
		elif self.image:
			# Use image as thumbnail
			self.thumbnail = self.make_thumbnail(self.image)
			self.save()
			return 'http://127.0.0.1:8000' + self.thumbnail.url
		else:
			return ''

	def make_thumbnail(self, image, size=(300, 200)):
		# Read image file as bytes
		img = Image.open(image)

		# Convert image to RGB values
		img.convert('RGB')

		# Set thumbnail to defined size
		img.thumbnail(size)

		# Create thumbnail
		thumb_io = BytesIO()
		img.save(thumb_io, 'JPEG', quality=85)

		# Convert thumbnail to a file
		thumbnail = File(thumb_io, name=image.name)

		return thumbnail