from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Data(models.Model):
    transmission_rate = models.FloatField(default=1)
    c_contact_rate = models.FloatField(default=1)
    T_transmissibility = models.FloatField(default=1)
    R0 = models.FloatField(default=1)
    new_infected_cases = models.FloatField(default=0.0)
    time = models.IntegerField(default=0)
    new_recovered_cases = models.IntegerField(default=0)
    new_death_cases = models.IntegerField(default=0)
    total_infected_cases = models.IntegerField(default=0)
    total_population = models.IntegerField(default=30000)
    m_total_asset = models.IntegerField(default=18)
    s_student_satisfaction = models.IntegerField(default=0)
    death_rate = models.FloatField(default=0.014)
    

    def updateTime(curTime):
        cur = Data(time = curTime+1)
        cur.save()
        return curTime+1

    def updateTransmissionRate(curTime):
        curData = Data.objects.get(time = curTime)
        curData.transmission_rate = curData.contact_rate * curData.T_transmissibility
        curData.save()
        return curData.transmission_rate

    def updateR0(time):
        R0 = 0
        if (time <= 3):
            R0 = 0
        elif (time <= 21 and time > 3):
            R0 = 0.18
        elif (time <= 28 and time > 21):
            R0 = 0.3
        elif (time <= 35 and time > 28):
            R0 = R0 * 0.3
        elif (time <= 42 and time > 35):
            R0 = R0 * 2
        elif (time <= 49 and time > 42):
            R0 = R0 * 1.5
        elif (time > 49):
            R0 = 2 
        curData = Data.objects.get(time = time)
        curData.R0 = R0
        curData.save()
        return R0
        
    def updateNew_infected_cases(curTime):
        curData = Data.objects.get(time = curTime)
        prevData = Data.objects.get(time = curTime - 1)
        Data.updateR0(curTime)
        curData.new_infected_cases = prevData.new_infected_cases * curData.R0
        curData.total_infected_cases = curData.total_infected_cases + curData.new_infected_cases
        curData.save()

      

class RandomNews(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text

class FixedNews(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text

"""
from game.models import RandomNews, FixedNews
q = RandomNews(text = "")
q.save()
from game.models import Data
Data.updateTransmissionRate(0)
q = Data(time = 0, R0 = 0, new_infected_cases = 10)
q = Data.objects.get(time = 0)
RandomNews.objects.all()
from game.models import Data
q = Data(time = 0, R0 = 0, new_infected_cases = 10)
q.transmission_rate = 1
q.c_contact_rate = 1
q.T_transmissibility = 1
q.new_infected_cases = 1
q.death_rate = 0.014
q.s_student_satisfaction = 25
"""