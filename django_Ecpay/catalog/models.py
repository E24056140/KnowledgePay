from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Item(models.Model):

    #name 產品名稱
    item_name = models.CharField(max_length=20)

    #id 產品編號
    item_id = models.AutoField(primary_key=True)
    
    #user 販售者 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #item_user = models.CharField(max_length=20)
    item_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    #price 價格
    item_price = models.IntegerField()

    #content 介紹
    item_content = models.TextField(help_text='Enter item content')

    #amount 已售出數量
    item_amount = models.IntegerField()

    #watermark 是否增加浮水印
    item_watermark = models.BooleanField()

    #綠界特店編號
    item_MerchantID = models.CharField(max_length=20,default='2000132')

    #綠界HashKey
    item_HashKey = models.CharField(max_length=20,default='5294y06JbISpM5x9')

    #綠界HashIV
    item_HashIV = models.CharField(max_length=20,default='v77hoKGq4kWxNNIS')

    
    # Methods
    def get_absolute_url(self):
         """Returns the url to access a particular instance of MyModelName."""
         return reverse('model-detail-view', args=[str(self.item_id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.item_name


class Order(models.Model):
    CheckMacValue = models.TextField()
    CustomField1 = models.TextField() 
    CustomField2 = models.TextField()
    CustomField3 = models.TextField()
    CustomField4 = models.TextField()
    MerchantID = models.TextField()
    MerchantTradeNo = models.TextField()
    PaymentDate = models.TextField()
    PaymentType = models.TextField()
    PaymentTypeChargeFee  = models.TextField()
    RtnCode = models.TextField()
    RtnMsg  = models.TextField()
    SimulatePaid = models.TextField()
    StoreID = models.TextField()
    TradeAmt = models.TextField()
    TradeDate = models.TextField()
    TradeNo = models.TextField()