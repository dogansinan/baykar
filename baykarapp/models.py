from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid


# Create your models here.





class Kategori(models.Model):
    isim = models.CharField(max_length=50)
    kategoriresim = models.FileField(upload_to='kategoripic/' , blank=True)
    slug = models.SlugField(null=True , unique=True , db_index=True , blank=True , editable=False)
     
    def save(self, *args , **kwargs):
        self.slug = slugify(self.isim)
        super().save(*args , **kwargs)

    def __str__(self):
        return self.isim
    
class Iha (models.Model):
    id = models.UUIDField(primary_key=True , db_index= True , default=uuid.uuid4 , editable=False)
    isim = models.CharField(max_length=50)
    kategori = models.ForeignKey(Kategori ,on_delete=models.CASCADE , null=True)
    agirlik = models.IntegerField(null=True)
    tanitim = models.TextField(max_length=2000)
    fiyat = models.IntegerField(null=True)
    kiralanacak = models.ManyToManyField(User, related_name='favori')
    resim = models.FileField(upload_to='ihapic/')
    slug = models.SlugField(null=True , unique=True , db_index=True , blank=True , editable=False)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.isim)
        super().save(*args , **kwargs)
    
    def __str__(self):
        return self.isim

class Kiralama(models.Model):
    iha = models.ForeignKey(Iha , on_delete = models.CASCADE)
    kullanici = models.ForeignKey(User , on_delete=models.CASCADE)
    kiralamaSaat = models.IntegerField()
    kiralamaToplam = models.FloatField()
    

    def __str__(self):
        return self.iha.isim 
    
    #JSON
    def get_data(self):
        return {
            'iha' : self.iha,
            'kullanici' : self.kullanici,
            'kiralamaSaat' : self.kiralamaSaat,
            'kiralamaToplam' : self.kiralamaToplam,

        }
    
class Profil (models.Model):
    id = models.UUIDField(primary_key=True , db_index= True , default=uuid.uuid4 , editable=False)
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    isim = models.CharField(max_length=50)
    soyisim = models.CharField(max_length=50)
    profilresim = models.FileField(upload_to='userpic/' ,default='userpic/default.jpg',blank=True)
    slug = models.SlugField(null=True , unique= True , db_index=True , blank=True , editable=False)

    def save(self, *args , **kwargs):
        self.slug = slugify(self.id)
        super().save(*args , **kwargs)

    def __str__(self):
        return str(self.isim)




