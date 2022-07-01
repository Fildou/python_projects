from django.db import models
from django.contrib.auth.models import User

TYPE = (
    ('All types','All types'),
    ('Analyzer','Analyzer'),
    ('Board', 'Board'),
    ('Board with display', 'Board with display'),
    ('Development board', 'Development board'),
    ('Display Touch Panel', 'Display Touch Panel'),
    ('Elevator', 'Elevator'),
    ('Kit - Debug adapter', 'Kit - Debug adapter'),
    ('Lauterbach Body', 'Lauterbach Body'),
    ('Lauterbach Head', 'Lauterbach Head'),
    ('Measurement card', 'Measurement card'),
    ('PC', 'PC'),
    ('Power stage', 'Power stage'),
)

LOCATION = (
    ('All locations', 'All locations'),
    ('Brno', 'Brno'),
    ('R-113 Cupboard', 'R-113 Cupboard'),
    ('R-114 Cupboard', 'R-114 Cupboard'),
    ('Roznov', 'Roznov'),
)

TEAM = (
    ('All teams', 'All teams'),
    ('MICR SW Operations and Quality', 'MICR SW Operations and Quality'),
    ('MICR SW Libs', 'MICR SW Libs'),
    ('AITEC', 'AITEC'),
    ('IMX ToolBox', 'IMX ToolBox'),
    ('IMCUXpresso Config Tools', 'IMCUXpresso Config Tools'),
    ('MPU Systems EMEA', 'MPU Systems EMEA'),
    ('MICR Solution Engineering', 'MICR Solution Engineering'),
    ('GPIS Solutions', 'GPIS Solutions'),
    ('MICR STEC', 'MICR STEC'),
    ('EP SW ATT', 'EP SW ATT'),
    ('Secure Provisioning SDK', 'Secure Provisioning SDK'),
    ('DevOps', 'DevOps'),
    ('Secure Provisioning SDK', 'Secure Provisioning SDK'),
)

ITEM_STOCK = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_PN = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50, choices=TYPE)
    item_stock = models.CharField(max_length=5, choices=ITEM_STOCK)
    team = models.CharField(max_length=50, choices=TEAM)
    location = models.CharField(max_length=50, choices=LOCATION)



    def __str__(self):
        return f'{self.item_name}'


class Borrowed_item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item} ordered by {self.user.username}'



