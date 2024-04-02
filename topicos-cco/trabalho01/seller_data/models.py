from django.db import models

class Sell(models.Model):
    """Dados fornecidos pelo vendedor."""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    buyer_name = models.CharField(max_length = 200)
    product_value = models.FloatField()
    product_name = models.CharField(max_length = 200)
    
    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return self.text
    
    
