from django.db import models
from django.contrib.auth.models import User
import time

class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    health = models.IntegerField(default=10)
    max_health = models.IntegerField(default=10)
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    strength = models.IntegerField(default=1)
    dexterity = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)
    luck = models.IntegerField(default=1)
    last_update = models.DateTimeField(auto_now=True)
    skill_points = models.IntegerField(default=0)  # Новое поле для очков навыков
    photo = models.ImageField(upload_to='characters/', blank=True, null=True, default='/static/images/default.png')

    LEVEL_THRESHOLDS = [110, 320, 640, 1280, 2480]

    def update_level(self):
        old_level = self.level
        for i, threshold in enumerate(self.LEVEL_THRESHOLDS):
            if self.experience >= threshold:
                self.level = i + 1
            else:
                break
        if self.level > old_level:  # Добавляем очки навыков только при повышении уровня
            self.skill_points += 5

    def update_health(self):
        current_time = time.time()
        last_update_time = self.last_update.timestamp()
        health_to_recover = int((current_time - last_update_time))  # 1 HP в секунду
        self.health = min(self.health + health_to_recover, self.max_health)
        self.last_update = time.time()  # Обновляем время последнего восстановления
        self.save(update_fields=['health', 'last_update'])

    def reduce_health(self, health_loss):
        self.health = max(self.health - health_loss, 0)  # Убедимся, что здоровье не менее 0

    def __str__(self):
        return self.name