from django.db import models

# Create your models here.
class CompanyInfo1(models.Model):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    territory = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    business = models.CharField(max_length=255, blank=True, null=True)
    product = models.TextField(blank=True, null=True)
    shareholder = models.CharField(max_length=255, blank=True, null=True)
    chairman = models.CharField(max_length=255, blank=True, null=True)
    board_secretariat = models.CharField(max_length=255, blank=True, null=True)
    correp = models.CharField(max_length=255, blank=True, null=True)
    generalmanager = models.CharField(max_length=255, blank=True, null=True)
    reg_fund = models.CharField(max_length=255, blank=True, null=True)
    num_employees = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_info1'


class Favorite(models.Model):
    id = models.IntegerField(primary_key=True)
    stock_id = models.IntegerField()
    fav_date = models.DateField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'favorite'
        unique_together = (('id', 'stock_id'),)


class FundamentalIndicators(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    eps = models.IntegerField(db_column='EPS', blank=True, null=True)  # Field name made lowercase.
    rota = models.FloatField(db_column='ROTA', blank=True, null=True)  # Field name made lowercase.
    roe = models.FloatField(db_column='ROE', blank=True, null=True)  # Field name made lowercase.
    per = models.FloatField(db_column='PER', blank=True, null=True)  # Field name made lowercase.
    pbr = models.FloatField(db_column='PBR', blank=True, null=True)  # Field name made lowercase.
    bvps = models.FloatField(db_column='BVPS', blank=True, null=True)  # Field name made lowercase.
    dyr = models.FloatField(db_column='DYR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fundamental_indicators'


class ManagerInfo(models.Model):
    manager_name = models.CharField(db_column='Manager_name', primary_key=True, max_length=255)  # Field name made lowercase.
    manager_gender = models.CharField(db_column='Manager_gender', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manager_age = models.CharField(db_column='Manager_age', max_length=6, blank=True, null=True)  # Field name made lowercase.
    manager_edu = models.CharField(db_column='Manager_edu', max_length=20, blank=True, null=True)  # Field name made lowercase.
    manager_intro = models.CharField(db_column='Manager_intro', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'manager_info'


class StockExternal(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=255)
    stock_address = models.CharField(max_length=255, blank=True, null=True)
    stock_industry = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_external'


class StockHisinfo(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    stock_date = models.DateField()
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    turnover = models.CharField(max_length=255, blank=True, null=True)
    vol = models.CharField(max_length=255, blank=True, null=True)
    swing = models.CharField(max_length=255, blank=True, null=True)
    changepercent = models.CharField(max_length=255, blank=True, null=True)
    changeamount = models.CharField(max_length=255, blank=True, null=True)
    turnover_rate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_hisinfo'
        unique_together = (('stock_id', 'stock_date'),)


class StockInfo(models.Model):
    no = models.BigIntegerField(db_column='No', blank=True, null=True)  # Field name made lowercase.
    stock_id = models.TextField(blank=True, null=True)
    stock_name = models.TextField(blank=True, null=True)
    now_price = models.FloatField(blank=True, null=True)
    changepercent = models.FloatField(blank=True, null=True)
    changeamount = models.FloatField(blank=True, null=True)
    turnover = models.FloatField(blank=True, null=True)
    vol = models.FloatField(blank=True, null=True)
    swing = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    close_price_yesterday = models.FloatField(blank=True, null=True)
    quantity_relative_ratio = models.FloatField(blank=True, null=True)
    turnover_rate = models.FloatField(blank=True, null=True)
    pe = models.FloatField(db_column='PE', blank=True, null=True)  # Field name made lowercase.
    pb = models.FloatField(db_column='PB', blank=True, null=True)  # Field name made lowercase.
    total_value = models.FloatField(blank=True, null=True)
    traded_market_value = models.FloatField(blank=True, null=True)
    higher_speed = models.FloatField(blank=True, null=True)
    five_min_up_down = models.FloatField(blank=True, null=True)
    sixty_day_up_down = models.FloatField(blank=True, null=True)
    yeartodate_up_down = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_info'


class StocksTechnicalIndicator(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    cci = models.FloatField(db_column='CCI', blank=True, null=True)  # Field name made lowercase.
    kdj = models.FloatField(db_column='KDJ', blank=True, null=True)  # Field name made lowercase.
    macd = models.FloatField(db_column='MACD', blank=True, null=True)  # Field name made lowercase.
    boll = models.FloatField(db_column='BOLL', blank=True, null=True)  # Field name made lowercase.
    vr = models.FloatField(db_column='VR', blank=True, null=True)  # Field name made lowercase.
    sar = models.FloatField(db_column='SAR', blank=True, null=True)  # Field name made lowercase.
    vol = models.FloatField(db_column='VOL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stocks_technical_indicator'


class TradeInfo(models.Model):
    trade_name = models.CharField(primary_key=True, max_length=10)
    trade_index = models.CharField(max_length=255, blank=True, null=True)
    trade_irise = models.CharField(max_length=255, blank=True, null=True)
    trade_today = models.CharField(max_length=255, blank=True, null=True)
    trade_yesterday = models.CharField(max_length=255, blank=True, null=True)
    trade_high = models.CharField(max_length=255, blank=True, null=True)
    trade_low = models.CharField(max_length=255, blank=True, null=True)
    trade_amount = models.CharField(max_length=255, blank=True, null=True)
    trade_crise = models.CharField(max_length=255, blank=True, null=True)
    trade_rank = models.CharField(max_length=255, blank=True, null=True)
    trade_srise = models.CharField(max_length=255, blank=True, null=True)
    trade_sfall = models.CharField(max_length=255, blank=True, null=True)
    trade_moneyin = models.CharField(max_length=255, blank=True, null=True)
    trade_goodmoney = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trade_info'


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.IntegerField()
    name = models.CharField(max_length=255)
    isManager = models.BooleanField()
    isSuperManager = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'user_info'
        unique_together = (('id', 'name'),)