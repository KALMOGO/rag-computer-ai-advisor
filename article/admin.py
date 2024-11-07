from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .computers.models import *
from .orders.models import *
# Register your models here.
admin.site.register([Supplier, Computer, Partner,Cooling,OperatingSystem, Acessoirs,
                    ComputerPhoto, Commend, Brand,GraphicalBrand,RecommendationResult,
                    Processor, Memory, Graphics, Case,MotherboardBrand,TokensList,
                    Storage,Motherboard,PowerSupply,ProcessorBrand,UserInfo, ComputerColor,
                    ComputerAcessoirsInfo, SimpleOrderRecommendation, ListJob,
                    ])
