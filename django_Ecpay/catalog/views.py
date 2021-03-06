from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .createOrder import main
from django.http import HttpResponse
import json
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm
import pathlib
import os
# Create your views here.

from .models import Item ,Order
from .addstamp import addstamp

def index(request):

    num_Items = Item.objects.all().count()
    num_Users = User.objects.all().count()
    num_Orders = Order.objects.all().count()
    all_items = Item.objects.all()

    context =  {
        'num_Items' : num_Items,
        'num_Users' : num_Users,
        'num_Orders' : num_Orders,
        'all_items' : all_items,
    }

    return render(request,'index.html',context=context)

#itemShow 產品頁面

def itemShow_view(request):

    response = {}
    ItemField = {}
    ItemData = {}
    try:
        ItemGet = Item.objects.filter(item_id=request.GET.get('item_id'))
        response['list'] = json.loads(serializers.serialize("json", ItemGet))

        ItemData = response['list']
        print (ItemData[0])
        ItemField = ItemData[0]['fields']
        print (ItemField)
        response['msg'] = 'success'
        response['error_num'] = 0

    

    except  Exception as e:

        response['msg'] = str(e)

        response['error_num'] = 1



    path="./catalog/static/images/"+str(request.GET.get('item_id'))  # insert the path to your directory   
    img_list =os.listdir(path) 
    print  (img_list)
    #'/static/images/'+str(request.GET.get('item_id'))+'/1.jpg'

    context =  {      
        'item_images' : img_list , 
        'item_name' : ItemField['item_name'],
        'item_id'  : ItemData[0]['pk'],
        'item_user'  : User.objects.get(id=ItemField['item_user']),
        'item_price'  : ItemField['item_price'],
        'item_content'  : ItemField['item_content'],
        'item_amount'  : ItemField['item_amount'],
    }
    print (ItemData[0]['pk'])
    return render(request,'itemShow.html',context=context)

# Create Ecpay Order
@csrf_exempt
def createOrder_view(request):
    response = {}
    ItemField = {}
    ItemData = {}
    customerEmail = ''
    try:
        
        ItemGet = Item.objects.filter(item_name=request.POST.get('item_name'))
    
        response['list'] = json.loads(serializers.serialize("json", ItemGet))

        ItemData = response['list']
        
        ItemField = ItemData[0]['fields']
        
        response['msg'] = 'success'
        response['error_num'] = 0

    except  Exception as e:

        response['msg'] = str(e)

        response['error_num'] = 1

    print (ItemData[0]['pk'])
    print (response['msg'])
    return HttpResponse(main(ItemField['item_name'],str(ItemData[0]['pk']),ItemField['item_price'],request.POST.get('customerEmail'),ItemField['item_user'],ItemField['item_MerchantID'],ItemField['item_HashKey'],ItemField['item_HashIV'],ItemField['item_watermark']))
    #

#接收綠界回傳成功訂單資料
@require_http_methods(["POST"])
def ecpayReply_view(request):
    response = {}
    Trade = {}
    # print(request)
    try:
        
        Trade = request.POST
        print(Trade)
        newOrder=Order(CheckMacValue=Trade['CheckMacValue'])
        newOrder.CustomField1=Trade['CustomField1']
        newOrder.CustomField2=Trade['CustomField2']
        newOrder.CustomField3=Trade['CustomField3']
        newOrder.CustomField4=Trade['CustomField4']
        newOrder.MerchantID=Trade['MerchantID']
        newOrder.MerchantTradeNo=Trade['MerchantTradeNo']
        newOrder.PaymentDate=Trade['PaymentDate']
        newOrder.PaymentType=Trade['PaymentType']
        newOrder.PaymentTypeChargeFee=Trade['PaymentTypeChargeFee']
        newOrder.RtnCode=Trade['RtnCode']
        newOrder.RtnMsg=Trade['RtnMsg']
        newOrder.SimulatePaid=Trade['SimulatePaid']
        newOrder.StoreID=Trade['StoreID']
        newOrder.TradeAmt=Trade['TradeAmt']
        newOrder.TradeDate=Trade['TradeDate']
        newOrder.TradeNo=Trade['TradeNo']
        newOrder.save()
        if Trade['RtnCode']=='1' :
            print(Trade)
            addstamp(Trade['CustomField1'],Trade['CustomField2'],Trade['CustomField4'])           
            
        
        response['list'] = json.loads(serializers.serialize("json", Trade))

        ItemData = response['list']
        
        
        response['msg'] = 'success'
        response['error_num'] = 0

    except  Exception as e:
        print(e)

        response['msg'] = str(e)

        response['error_num'] = 1

    
    return HttpResponse('1|OK')

#註冊
from django.contrib.auth.forms import UserCreationForm
def signUp_view(request):

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/catalog/accounts/login')  #重新導向到登入畫面

    context = {
        'form': form
    }

    return render(request, 'registration/signUp.html', context)

#新增產品頁面
def addItem_view(request):
    context = {

    }
    return render(request, 'addItem.html', context)

#新增商品至資料庫
@csrf_exempt
def addItemOK_view(request):
    response = {}
  
    try:
        
        print(request.POST)
        newItemUser = User.objects.get(username=request.POST['item_user'])
        
        
        newItemWatermark = False
        
        try:
            if request.POST['item_watermark'] :
                newItemWatermark = True
                
        except:
            pass
           
        #UserData = json.loads(serializers.serialize("json",newItemUser))
        newItem = Item(item_name=request.POST['item_name'],item_user=newItemUser,item_amount=0,item_price=request.POST['item_price'],item_content=request.POST['item_content'],item_watermark=newItemWatermark,item_MerchantID=request.POST['item_MerchantID'],item_HashKey=request.POST['item_HashKey'],item_HashIV=request.POST['item_HashIV'])
       
        newItem.save()
        print(newItem.item_id)

        
        flist=request.FILES.getlist('item_image')
        if not os.path.exists('./catalog/static/images/'+str(newItem.item_id)):
            os.makedirs('./catalog/static/images/'+str(newItem.item_id))
       
        for f in flist:
            print(f)
            print(flist.index(f))
            with open('./catalog/static/images/'+str(newItem.item_id)+'/'+str(flist.index(f)+1)+'.jpg','wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        if not os.path.exists('./catalog/item_file/'+str(newItem.item_id)):
            os.makedirs('./catalog/item_file/'+str(newItem.item_id))
       
        flist=request.FILES.getlist('item_file')
        # print(f[0])
        # print(len(f))
        # savename=f.name	
        for f in flist:
            savename=f.name
            with open('./catalog/item_file/'+str(newItem.item_id)+'/' + savename,'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        response['msg'] = 'success'
        response['error_num'] = 0
        print(response)

        return redirect('/catalog/')

    except  Exception as e:
        print(e)
        response['msg'] = str(e)

        response['error_num'] = 1

    
    print(response)
    return HttpResponse('alert("新增失敗")')

#所有商品列表
def myItem_view(request):

    
    all_items = Item.objects.filter(item_user=request.GET.get('user_id'))
    
    #print(user.get_username)
    print(all_items)
    
    return render(request, 'myItem.html', {'all_items' : all_items ,'user_id': request.GET.get('user_id')} )

#修改商品
@csrf_exempt
def update_view(request):
    response = {}
    updateItem = Item
    try:
        updateItem = Item.objects.get(item_id=request.GET.get('item_id'))
       
        updateItemId = request.GET.get('item_id')
        if request.method == 'POST':

            updateItemWatermark = False
            try:
                if request.POST['item_watermark'] == True :
                    updateItemWatermark = True
            except:
                pass

            updateItemUser = User.objects.get(username=request.POST['item_user'])
            updateItemOK = Item(item_name=request.POST['item_name'],item_user=updateItemUser,item_id=updateItemId,item_amount=0,item_price=request.POST['item_price'],item_content=request.POST['item_content'],item_watermark=updateItemWatermark)
            updateItemOK.save() 
            response['msg'] = 'success'
            response['error_num'] = 0
            print(response)
            return redirect('/catalog/')

       
        
    
    except  Exception as e:

        response['msg'] = str(e)

        response['error_num'] = 1
        print(response)

    return render(request, 'update.html', {'updateItem' : updateItem ,'item_image' : '/static/images/'+str(request.GET.get('item_id'))+'.jpg' })

#刪除商品
@csrf_exempt
def delete_view(request):
    response = {}
    deleteItem = Item
    try:
        deleteItem = Item.objects.get(item_id=request.GET.get('item_id'))
        deleteItemId = request.GET.get('item_id')
        if request.method == 'POST':                   
            deleteItem.delete() 
            response['msg'] = 'success'
            response['error_num'] = 0
            print(response)
            return redirect('/catalog/')

       
        
    
    except  Exception as e:

        response['msg'] = str(e)

        response['error_num'] = 1
        print(response)

    return render(request, 'delete.html', {'deleteItem' : deleteItem  })

from django.db.models.query import QuerySet

#所有訂單列表
def myOrder_view(request):
    
    all_orders = Order.objects.filter(CustomField3=request.GET.get('user_id'))

    all_item_names = Item.objects.filter(item_id=request.GET.get('user_id'))
     
    
    
    return render(request, 'myOrder.html', {'all_orders' : all_orders,'user_id': request.GET.get('user_id') } )


#訂單細節
def orderDetail_view(request):

    orderDetail = Order.objects.get(TradeNo=request.GET.get('TradeNo'))

  
    return render(request, 'orderDetail.html', {'orderDetail' : orderDetail } )