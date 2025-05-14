from django.db import models
from django.contrib.auth.models import User

class Musician(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    birth=models.DateField()
    def __str__(self):
        return f"Musician={self.id}, first_name={self.first_name}, last_name={self.last_name}, birth={self.birth}"
    
class Venue(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"id={self.id}, name={self.name}"

class Room(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room={self.id}, name={self.name}, venue={self.venue}"

class Band(models.Model):
    name = models.CharField(max_length=50)
    musicians = models.ManyToManyField(Musician)

    def __str__(self):
        return f"Band={self.id}, name={self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    musician_profiles = models.ManyToManyField(Musician)
    venue_controlled=models.ManyToManyField(Venue,blank=True)

# Musicians
# ● Bands
# ● Classifieds
# ● Venues
# ● Venue lineups
