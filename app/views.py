from django.shortcuts import render,get_object_or_404,redirect
import requests
from pprint import pprint
from app.models import Coin
from django.contrib import  messages
# Create your views here.
def home(request):
    coin = request.GET.get("coin_name") or "hello"
    # pprint(coin)
    url ="https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    response = requests.get(url)
    content = response.json()
    
    # pprint(content[0]["name"])
    # text =""
    for i in content:
        if coin:
            if i["name"].lower() == coin.lower():
                name_c = i["name"]         
                if Coin.objects.filter(name = name_c):
                    # aynı veriden var
                    continue
                else :
                    Coin.objects.create(name=name_c)       
            else :
                continue
                # girilen veri api de yok  
    coins = Coin.objects.all().order_by("-id")
    
    # for k in coins:
    #     for n  in range(0,100):
    coin_data = []       
    for k in coins:
        # print(k)
        for n in content:
            if  n["name"] == str(k):
                
                data = {
                    "k":k,
                    "name":n["name"],
                    "image":n["image"],
                    "market":n["current_price"],
                    "change":n["price_change_24h"],
                }
                
                pprint(data)
                coin_data.append(data)
                
                # x = n["name"]
                # print(x)
    context = {
        "coin_data": coin_data
    }
    
    
    return render(request, "app/home.html", context)

def delete_coin(request, id):
    coin = get_object_or_404(Coin, id=id)
    coin.delete()
    messages.success(request, 'City deleted!')
    return redirect('home')