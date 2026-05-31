from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255) 
    is_admin = models.BooleanField(default=False)
    
    failed_login_attempts = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()

    def __str__(self):
        return f"Note by {self.user.username}: {self.content[:20]}"

class SecurityLog(models.Model):
    message = models.CharField(max_length=255)
    severity = models.CharField(max_length=50, default='INFO')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.severity}] {self.message} at {self.created_at}"
