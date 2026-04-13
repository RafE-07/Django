from django.db import models

# Create your models here.
class Mediafile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='mediafiles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filesize = models.PositiveIntegerField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.file and not self.filesize:
            self.filesize = self.file.size
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-uploaded_at']