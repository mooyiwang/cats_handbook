# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addr(models.Model):
    a_id = models.AutoField(primary_key=True, verbose_name='位置编号')
    a_name = models.CharField(max_length=12, verbose_name='位置名称')
    a_park = models.CharField(max_length=12, verbose_name='所属园区')

    class Meta:
        ordering = ['a_id']
        db_table = 'addr'
        verbose_name = "位置信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'位置：{self.a_park}/{self.a_name}'


class Cat(models.Model):
    c_id = models.AutoField(primary_key=True, verbose_name='猫咪编号')
    a = models.ForeignKey(Addr, models.DO_NOTHING, verbose_name='最近位置')
    s = models.ForeignKey('Sterilize', models.DO_NOTHING, blank=True, null=True, verbose_name='绝育编号')
    s_bool = models.IntegerField(choices=[(1, '已绝育'), (0, '未绝育')], verbose_name='绝育状态')
    c_name = models.CharField(max_length=12, verbose_name='猫咪昵称')
    c_sex = models.IntegerField(choices=[(1, '公'), (0, '母')], verbose_name='猫咪性别')
    c_look = models.CharField(max_length=4, verbose_name='猫咪外貌')
    c_icon = models.ImageField(upload_to='images/cats', null=True, blank=True, verbose_name='猫咪照片')
    c_status = models.IntegerField(choices=[(2, '健康'), (1, '良好'), (0, '较差')], verbose_name='猫咪状态')
    c_character = models.CharField(max_length=12, blank=True, null=True, verbose_name='猫咪性格')
    c_first = models.DateField(verbose_name='首次目击')
    c_recent = models.DateField(verbose_name='最近目击')

    class Meta:
        ordering = ['c_id']
        verbose_name = "猫咪信息"
        verbose_name_plural = verbose_name
        db_table = 'cat'

    def __str__(self):
        return f'猫咪：{self.c_id}/{self.c_name}'


class CatRel(models.Model):
    cr_id = models.AutoField(primary_key=True, verbose_name='关系编号')
    c_1 = models.ForeignKey(Cat, models.CASCADE, verbose_name='猫咪1', related_name='cat_1')
    c_2 = models.ForeignKey(Cat, models.CASCADE, verbose_name='猫咪2', related_name='cat_2')
    r_type = models.IntegerField(choices=[(0, '父子'), (1, '母子'), (2, '兄弟'), (3, '姐妹'), (4, '朋友'), (5, '敌人')],
                                 verbose_name='关系类型')

    class Meta:
        db_table = 'cat_rel'
        unique_together = (('c_1', 'c_2'),)
        verbose_name = "关系信息"
        verbose_name_plural = verbose_name
        ordering = ['cr_id']

    def __str__(self):
        return f'猫咪关系：{self.c}和{self.cat_c}是{self.r_type}'


class Checkcat(models.Model):
    k_id = models.AutoField(primary_key=True, verbose_name='打卡编号')
    c = models.ForeignKey(Cat, models.DO_NOTHING, verbose_name='打卡猫咪')
    a = models.ForeignKey(Addr, models.DO_NOTHING, verbose_name='打卡位置')
    u = models.ForeignKey('Userinfo', models.DO_NOTHING, verbose_name='打卡用户')
    k_time = models.DateField(verbose_name='打卡时间')

    class Meta:
        ordering = ['-k_id']
        verbose_name = "打卡信息"
        verbose_name_plural = verbose_name
        db_table = 'checkcat'

    def __str__(self):
        return f'打卡：{self.k_time}打卡猫咪{self.c}@位置{self.a}'


class Feed(models.Model):
    t_id = models.AutoField(primary_key=True, verbose_name='投喂编号')
    f = models.ForeignKey('Food', models.DO_NOTHING, verbose_name='投喂食品')
    u = models.ForeignKey('Userinfo', models.DO_NOTHING, verbose_name='投喂用户')
    a = models.ForeignKey(Addr, models.DO_NOTHING, verbose_name='投喂位置')
    c = models.ForeignKey(Cat, models.DO_NOTHING, verbose_name='投喂猫咪')
    t_time = models.DateField(verbose_name='投喂时间')

    class Meta:
        ordering = ['-t_id']
        verbose_name = "投喂信息"
        verbose_name_plural = verbose_name
        db_table = 'feed'

    def __str__(self):
        return f'投喂：{self.t_time}投喂{self.f}to猫咪{self.c}@位置{self.a}'


class Food(models.Model):
    f_id = models.AutoField(primary_key=True, verbose_name='食品编号')
    f_name = models.CharField(max_length=12, verbose_name='食品名称')

    class Meta:
        ordering = ['f_id']
        verbose_name = "食品信息"
        verbose_name_plural = verbose_name
        db_table = 'food'

    def __str__(self):
        return f'食品：{self.f_id}/{self.f_name}'


class Sterilize(models.Model):
    s_id = models.AutoField(primary_key=True, verbose_name='绝育编号')
    s_time = models.DateField(verbose_name='绝育日期')

    class Meta:
        ordering = ['s_id']
        verbose_name = "绝育信息"
        verbose_name_plural = verbose_name
        db_table = 'sterilize'

    def __str__(self):
        return f'绝育：{self.s_id}/{self.s_time}'


class Userinfo(models.Model):
    u_id = models.AutoField(primary_key=True, verbose_name='用户编号')
    u_name = models.CharField(max_length=12, verbose_name='用户名')

    class Meta:
        ordering = ['u_id']
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = 'userinfo'

    def __str__(self):
        return f'用户：{self.u_id}/{self.u_name}'
