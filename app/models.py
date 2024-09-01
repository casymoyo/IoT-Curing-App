from django.db import models
from django.utils.translation import gettext_lazy as _

class Stage(models.Model):
    class StageChoices(models.TextChoices):
        INITIAL = 'initial', _("Initial")
        MID = 'mid', _("Mid")
        FINAL = 'final', _("Final")
        
    name = models.CharField(max_length=10, verbose_name=_("Stage Name"), choices=StageChoices.choices)
    selected = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("Stage")
        verbose_name_plural = _("Stages")

class Temperature(models.Model):
    value = models.FloatField(verbose_name=_("Temperature Value"))
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Timestamp"))
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.value}°C'
    
    class Meta:
        verbose_name = _("Temperature")
        verbose_name_plural = _("Temperatures")

class Humidity(models.Model):
    value = models.FloatField(verbose_name=_("Humidity Value"))
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Timestamp"))
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.value}%'
    
    class Meta:
        verbose_name = _("Humidity")
        verbose_name_plural = _("Humidity Levels")

class Config(models.Model):
    class NameChoices(models.TextChoices):
        TEMPERATURE = 'temperature', _("Temperature")
        HUMIDITY = 'humidity', _("Humidity")
    
    class StageChoices(models.TextChoices):
        INITIAL = 'initial', _("Initial")
        MID = 'mid', _("Mid")
        FINAL = 'final', _("Final")
        
    stage = models.CharField(max_length=20, choices=StageChoices.choices)
    name = models.CharField(max_length=20, choices=NameChoices.choices)
    lower_limit_value = models.FloatField(verbose_name=_("Config Value"))
    upper_limit_value = models.FloatField(verbose_name=_("Config Value"))
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, verbose_name=_("User"))
    
    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")
        indexes = [
            models.Index(fields=['stage', 'user']),
        ]

class AlertLog(models.Model):
    class AlertType(models.TextChoices):
        LOW = 'low', _("Low")
        MID = 'mid', _("Mid")
        HIGH = 'high', _("High")

    timestamp = models.DateTimeField(db_index=True, verbose_name=_("Timestamp"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    alert_type = models.CharField(max_length=10, choices=AlertType.choices, verbose_name=_("Alert Type"))
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return f'{self.timestamp}: ({self.get_alert_type_display()})'
    
    class Meta:
        verbose_name = _("Alert Log")
        verbose_name_plural = _("Alert Logs")
        indexes = [
            models.Index(fields=['timestamp', 'alert_type']),
        ]
