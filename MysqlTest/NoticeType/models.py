from django.db import models

class bbb(models.Model):
    customer_sn = models.CharField(max_length=255)
    server_id = models.CharField(max_length=255)
    
    def __str__(self):
        return self.server_id