from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save( *args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        

class ProductImage(BaseModel):
    image = models.ImageField(upload_to="products/", null=True, blank=True) # Relationship
    product = models.ForeignKey(to="furni.Product", on_delete=models.CASCADE, related_name="images")
    
    class Meta:
        db_table = "product_images"


class Product(BaseModel):
    FIXED = "fixed"
    INDEFINITE = "indefinite"
    NOT_AVAILABLE = "not_available"
    STATUSES = (
        (FIXED, "Fixed"),
        (INDEFINITE, "Indefinite"),
        (NOT_AVAILABLE, "Not available")
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = RichTextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_status = models.CharField(choices=STATUSES, default=INDEFINITE)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="products")
    discount = models.ManyToManyField(to="furni.Discount", related_name="products", blank=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="products", null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save( *args, **kwargs)
    
    class Meta:
        ordering = ["-id"]
        db_table = "products"


class Discount(BaseModel):
    name = models.CharField(max_length=255)
    percent = models.PositiveIntegerField(default=0)
    deadline = models.DateTimeField()
    
    def __str__(self):
        return self.name
