from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """用户资料扩展"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    preferences = models.TextField(blank=True, verbose_name='旅行偏好')
    avatar = models.URLField(blank=True, verbose_name='头像')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f"{self.user.username} 的资料"

class TravelPlan(models.Model):
    """旅行计划"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_plans')
    title = models.CharField(max_length=200, verbose_name='计划标题')
    description = models.TextField(blank=True, verbose_name='计划描述')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='预算')
    destination = models.CharField(max_length=200, verbose_name='目的地')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '旅行计划'
        verbose_name_plural = '旅行计划'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Destination(models.Model):
    """目的地"""
    plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='destinations')
    name = models.CharField(max_length=200, verbose_name='目的地名称')
    description = models.TextField(blank=True, verbose_name='描述')
    arrival_date = models.DateField(verbose_name='到达日期')
    departure_date = models.DateField(verbose_name='离开日期')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='经度')

    class Meta:
        verbose_name = '目的地'
        verbose_name_plural = '目的地'

    def __str__(self):
        return f"{self.name} - {self.plan.title}"

class Attraction(models.Model):
    """景点"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=200, verbose_name='景点名称')
    description = models.TextField(blank=True, verbose_name='描述')
    visit_time = models.DateTimeField(verbose_name='参观时间')
    duration = models.PositiveIntegerField(default=60, verbose_name='预计时长(分钟)')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='费用')
    address = models.CharField(max_length=300, blank=True, verbose_name='地址')

    class Meta:
        verbose_name = '景点'
        verbose_name_plural = '景点'

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

class Itinerary(models.Model):
    """行程安排"""
    plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=200, verbose_name='行程标题')
    description = models.TextField(blank=True, verbose_name='行程描述')
    date = models.DateField(verbose_name='日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    location = models.CharField(max_length=200, blank=True, verbose_name='地点')
    notes = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '行程安排'
        verbose_name_plural = '行程安排'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.date}"

class TravelItem(models.Model):
    """旅行清单项目"""
    ITEM_TYPES = [
        ('luggage', '行李'),
        ('document', '证件'),
        ('other', '其他'),
    ]

    plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='travel_items')
    name = models.CharField(max_length=200, verbose_name='项目名称')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='other', verbose_name='项目类型')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    is_packed = models.BooleanField(default=False, verbose_name='是否已打包')
    notes = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '旅行清单项目'
        verbose_name_plural = '旅行清单项目'

    def __str__(self):
        return f"{self.name} - {self.plan.title}"

class TravelPreference(models.Model):
    """用户旅行偏好"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='travel_preference')
    preferred_activities = models.TextField(blank=True, verbose_name='偏好的活动类型')
    budget_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='预算范围最小值')
    budget_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='预算范围最大值')
    preferred_climate = models.CharField(max_length=100, blank=True, verbose_name='偏好的气候')
    special_requirements = models.TextField(blank=True, verbose_name='特殊要求')

    class Meta:
        verbose_name = '旅行偏好'
        verbose_name_plural = '旅行偏好'

    def __str__(self):
        return f"{self.user.username} 的旅行偏好"
