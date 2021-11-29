from django.db import models

# Create your models here.
class EmailDefaultValues(models.Model):
    """Model definition for EmailDefaultValues."""

    # TODO: Define fields here
    subject = models.CharField(max_length=500)
    message_body = models.TextField()

    class Meta:
        """Meta definition for EmailDefaultValues."""

        verbose_name = 'EmailDefaultValue'
        verbose_name_plural = 'EmailDefaultValues'

    def __str__(self):
        """Unicode representation of EmailDefaultValues."""
        return self.subject
