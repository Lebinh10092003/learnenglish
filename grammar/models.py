from django.db import models

class Grammar(models.Model):
    vn_rule_name = models.CharField(max_length=255)
    rule_name = models.CharField(max_length=255)
    rule_description = models.TextField()
    example = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_name