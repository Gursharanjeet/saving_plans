from django.db import models


class Plans(models.Model):
    planId = models.AutoField(primary_key=True)
    planName = models.CharField(max_length=256, null=None)
    amountOption = models.TextField(null=None)
    tenureOption = models.TextField(null=None)
    benefitPercentage = models.FloatField(null=None)
    benefitType = models.CharField(max_length=256, null=None)
    is_active = models.BooleanField(default=True)


class Promotions(models.Model):
    planID = models.ForeignKey(Plans, on_delete=models.CASCADE)
    promotionId = models.AutoField(primary_key=True)
    promotionType = models.CharField(max_length=256, null=None)
    promotionStartDate = models.DateTimeField(null=True)
    promotionEndDate = models.DateTimeField(null=True)
    promotionCount = models.IntegerField(null=True)
    promotionBenefitPercentage = models.FloatField(null=None)
    is_active = models.BooleanField(default=True)


class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=None)


class CustomerGoal(models.Model):
    customerId = models.AutoField(primary_key=True)
    planID = models.ForeignKey(Plans, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    promotionId = models.IntegerField(null=True)
    amount = models.FloatField(null=None)
    tenure = models.IntegerField(null=None)
    startDate = models.DateTimeField(null=None)
    depositAmount = models.FloatField(null=None, default=0)
    benefitPercentage = models.FloatField(null=None)
