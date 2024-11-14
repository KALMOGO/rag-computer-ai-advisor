from django.db import models
from ..suppliers.models import *
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class MotherboardBrand(models.Model):
    name = models.CharField(max_length=200)
    model = models.CharField( max_length=250, null=True, blank=True)
    def __str__(self):
        return f"{self.name} {self.model}"

class ProcessorBrand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class GraphicalBrand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Processor(models.Model):
    brand = models.ForeignKey(ProcessorBrand, on_delete=models.PROTECT, related_name='processors')
    model = models.CharField(max_length=100, blank=True, null=True)
    cores = models.PositiveIntegerField(blank=True, null=True)
    threads = models.PositiveIntegerField(blank=True, null=True)
    base_clock_speed = models.CharField(max_length=20,blank=True, null=True)
    turbo_clock_speed = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.cores}"

class Memory(models.Model):
    type = models.CharField(max_length=20,blank=True, null=True)
    capacity = models.CharField(max_length=20,blank=True, null=True)
    speed = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f"{self.capacity}"

class Storage(models.Model):
    type = models.CharField(max_length=20,blank=True, null=True)
    capacity = models.CharField(max_length=20,blank=True, null=True)
    interface = models.CharField(max_length=50, null=True, blank=True)
    rpm = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.capacity} {self.type}"

class Graphics(models.Model):
    type = models.CharField(max_length=20,blank=True, null=True)
    brand = models.ForeignKey(GraphicalBrand, on_delete=models.PROTECT, related_name='graphics_cards')
    model = models.CharField(max_length=100,blank=True, null=True)
    memory = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Motherboard(models.Model):
    brand = models.ForeignKey(MotherboardBrand, on_delete=models.PROTECT, related_name='motherboards')
    model = models.CharField(max_length=100,blank=True, null=True)
    chipset = models.CharField(max_length=100,blank=True, null=True)
    
    def __str__(self):
        return f"{self.brand} {self.model}"

class PowerSupply(models.Model):
    wattage = models.PositiveIntegerField()
    efficiency = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f"{self.wattage}W {self.efficiency}"

class Cooling(models.Model):
    type = models.CharField(max_length=50)
    radiator_size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.type} cooling"

class Case(models.Model):
    brand = models.CharField(max_length=50,blank=True, null=True)
    model = models.CharField(max_length=50,blank=True, null=True)
    form_factor = models.CharField(max_length=50,blank=True, null=True)
    color = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return f"{self.color} {self.form_factor}"

class OperatingSystem(models.Model):
    name    = models.CharField(max_length=50,blank=True, null=True)
    version = models.CharField(max_length=50,blank=True, null=True)
    bitness = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.version} {self.bitness}-bit"


class ComputerKeyboard(models.Model):
    type = models.CharField(max_length=200)
    is_backlit = models.BooleanField(default=False)
    as_numeric_panel = models.BooleanField(default=False)
    as_finger_print = models.BooleanField(default=False)
    creation_date = models.DateField( auto_now_add=True)

    class Meta:
        ordering = ("-creation_date",)
    
    def __str__(self) -> str:
        return self.type + " lum : " + str(self.is_backlit) + " et num : " + str(self.as_numeric_panel) + " et finger : " + str(self.as_finger_print)

class ComputerManager(models.Manager):
    def get_next_id(self):
        last_computer = self.order_by('-id').first()
        if not last_computer:
            return 'PC001'
        last_id = int(last_computer.id[2:])
        next_id = last_id + 1
        return f'PC{next_id:03d}'
    
    @staticmethod
    def max_image_size(image): # Taille des images
        max_size = 1000 * 1024  # 2 KB or 5 * 1024 * 1024   5 MB
        if image.size > max_size:
            raise ValidationError(f'Image size must be under {max_size / (1024 * 1024)} MB.')

class ComputerColor(models.Model):
    color = models.CharField(max_length=200)
    creation_date = models.DateField( auto_now_add=True)

    class Meta:
        ordering = ("-creation_date",)
    
    def __str__(self) -> str:
        return self.color

class Computer(models.Model):
    id    = models.CharField(max_length=20, primary_key=True, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='computers')
    model = models.CharField(max_length=100,blank=True, null=True)
    type  = models.CharField(max_length=50,blank=True, null=True)
    price_amount   = models.DecimalField(default=0.0,max_digits=10, decimal_places=2)
    price_currency = models.CharField(max_length=3,blank=True, null=True)
    color =  models.ForeignKey(ComputerColor, on_delete=models.PROTECT,blank=True, null=True)

    processor = models.ForeignKey(Processor, on_delete=models.PROTECT)
    memory    = models.ForeignKey(Memory, on_delete=models.PROTECT)
    graphics  = models.ForeignKey(Graphics, on_delete=models.PROTECT,blank=True, null=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.PROTECT,blank=True, null=True)
    power_supply= models.ForeignKey(PowerSupply, on_delete=models.PROTECT,blank=True, null=True)
    cooling = models.ForeignKey(Cooling, on_delete=models.PROTECT,blank=True, null=True)
    case    = models.ForeignKey(Case, on_delete=models.PROTECT,blank=True, null=True)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.PROTECT)

    storages  = models.ManyToManyField(Storage, related_name='computers')
    
    wifi      = models.CharField(max_length=50,blank=True, null=True)
    bluetooth = models.CharField(max_length=10,blank=True, null=True)
    ethernet  = models.CharField(max_length=50,blank=True, null=True)
    
    usb3_2_gen2_typeC = models.PositiveIntegerField(default=0)
    usb3_2_gen2_typeA = models.PositiveIntegerField(default=0)
    usb3_2_gen1_typeA = models.PositiveIntegerField(default=0)
    usb2_0 = models.PositiveIntegerField(default=0)
    
    hdmi_ports    = models.PositiveIntegerField(default=0)
    display_ports = models.PositiveIntegerField(default=0)
    
    audio_front_panel = models.CharField(max_length=100,blank=True, null=True)
    audio_rear_panel  = models.CharField(max_length=100,blank=True, null=True)
        
    height= models.CharField(max_length=20,blank=True, null=True)
    width = models.CharField(max_length=20,blank=True, null=True)
    depth = models.CharField(max_length=20,blank=True, null=True)
    weight= models.CharField(max_length=20,blank=True, null=True)
    
    warranty_duration= models.CharField(max_length=50,blank=True, null=True)
    warranty_type    = models.CharField(max_length=100,blank=True, null=True)
    warranty_support = models.CharField(max_length=100,blank=True, null=True)
    
    energy_rating = models.CharField(max_length=50,blank=True, null=True)
    extras        = models.TextField(blank=True,null=True)
    
    in_stock = models.BooleanField(default=True)
    estimated_shipping_time = models.CharField(max_length=50,blank=True, null=True)
    
    average_rating    = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    number_of_reviews = models.PositiveIntegerField(default=0)

    objects  = ComputerManager()

    supplier    = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='computers')
    percentage  = models.FloatField(default=0.0)
    description = HTMLField(blank=True, null=True) 
    screen_size = models.CharField(max_length=50, blank=True, null=True)
    keyboard     = models.ForeignKey(ComputerKeyboard, on_delete=models.PROTECT,blank=True, null=True)

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = Computer.objects.get_next_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model}"

class ListSofware(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    version = models.CharField(max_length=100,blank=True, null=True)
    creation_date = models.DateField( auto_now_add=True)
    description   = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Liste des logiciels"
        ordering = ("-creation_date",)
        
    def __str__(self):
        return self.name
class PreInstalledSoftware(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    version = models.CharField(max_length=100,blank=True, null=True)
    computer      = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='pre_installed_software')
    creation_date = models.DateField( auto_now_add=True)
    description   = models.TextField(blank=True, null=True)

    class Meta:
        # verbose_name_plural = "Logiciels pre-installés",
        ordering = ("-creation_date",)
        
    def __str__(self):
        return self.name


class ComputerPhoto(models.Model):
    image = models.ImageField(upload_to='media/computers/images/',
                            validators=[ComputerManager.max_image_size])
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='photos')
    slug = models.SlugField("Slug")
    creation_date = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    is_cover = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Computer Photos"
        ordering = ("-creation_date",)

    def save(self, *args, **kwargs) -> None:
        self.slug = f"{self.computer.pk}{random.random() * 100}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.computer.id } / {self.computer.brand.name} / {self.computer.model} / core i {self.computer.processor.cores-1} / PHOTO" 

class RecommendationResult(models.Model):
    computer_id   = models.CharField(max_length=50,blank=True, null=True)
    choose_reason =  models.TextField(blank=True, null=True)
    recommendation_time = models.CharField(max_length=250, blank=True, null=True)
    max_budget  = models.CharField(max_length=50,blank=True, null=True)
    min_budget  = models.CharField(max_length=50,blank=True, null=True)
    job_title    =  models.CharField(max_length=50,blank=True, null=True)
    job_description =  models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return f"Job: {self.job_title} computer : {self.computer_id} time: {self.recommendation_time}"


class Acessoirs(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    description = models.CharField(max_length=100,blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Acessoirs"
        ordering = ("-creation_date",)

    def __str__(self):
        return f"{self.name}"
    
class ComputerAcessoirsInfo(models.Model):
    image = models.ImageField(upload_to='media/computers/images/', blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    acessoirs = models.ForeignKey(Acessoirs, on_delete=models.CASCADE, related_name='computer_acessoirs_info')
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='acessoirs_info')
    is_applied = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Acessoirs Detail"
        ordering = ("-creation_date",)

    def __str__(self):
        return f"{self.computer.id} {self.acessoirs.name}"


class SimpleOrderRecommendation(models.Model):
    computer_id       = models.CharField(max_length=50,blank=True, null=True)
    recommendation_id = models.CharField(max_length=250, blank=True, null=True)
    max_budget  = models.CharField(max_length=50,blank=True, null=True)
    min_budget  = models.CharField(max_length=50,blank=True, null=True)
    brand       =  models.CharField(max_length=50,blank=True, null=True)
    ram         =  models.CharField(max_length=50,blank=True, null=True)
    processor_core =  models.CharField(max_length=50,blank=True, null=True)
    storage        =  models.CharField(max_length=50,blank=True, null=True)
    os      =  models.CharField(max_length=50,blank=True, null=True)
    color   =  models.CharField(max_length=50,blank=True, null=True)
    graphic =  models.CharField(max_length=50,blank=True, null=True)
    processor_speed =  models.CharField(max_length=50,blank=True, null=True)
    creation_date   = models.DateTimeField(auto_now_add=True)
    user_id         = models.CharField(max_length=50,blank=True, null=True)
    user_location   = models.CharField(max_length=50,blank=True, null=True)
    is_processed    = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Recommandation sans IA Results"
        ordering = ("-creation_date",)

    def __str__(self):
        return f"user: {self.user_id} computer : {self.computer_id} time: {self.recommendation_id}"


class ListJob(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    description = models.CharField(max_length=100,blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "List Jobs"
        ordering = ("-creation_date",)

    def __str__(self):
        return f"{self.name}"