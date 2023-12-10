from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
# Ön yüz tarafında tüm kullanıcı kiralama kayıtlarının yönetimi
def management(request):
    if request.user.is_authenticated:
        ihalar = Kiralama.objects.filter(kullanici = request.user)
    else:
        ihalar = 0
    kategoriler = Iha.objects.all()
    context={
        'kategoriler' :kategoriler,
        'ihalar' :ihalar
    }
    return render(request,'management.html',context)

#Tüm Kiralanan İHA'lar JSON Oluşturma
def kiralanan_iha_json (request):
   data = Kiralama.objects.all().values('iha','kullanici','kiralamaSaat','kiralamaToplam')
   return JsonResponse(list(data),safe=False)
#Tüm İHA Kayıtları JSON Oluşturma
def iha_json (request):
   data = Kategori.objects.all().values('iha','isim','kategoriresim','slug')
   return JsonResponse(list(data),safe=False)
#Tüm Kullanıcı Kayıtları JSON Oluşturma
#Tüm İHA Kayıtları JSON Oluşturma
def user_json (request):
   data = User.objects.all().values('first_name','last_name','username','email','date_joined','is_active',)
   return JsonResponse(list(data),safe=False)





def kiralama(request):
    if request.user.is_authenticated:
        ihalar = Kiralama.objects.filter(kullanici = request.user)
    else:
        ihalar = 0
    toplamFiyat = 0
    for i in ihalar:
        toplamFiyat += i.kiralamaToplam

    context = {
        'ihalar' :ihalar,
        'toplamFiyat' : toplamFiyat
    }

    return render(request , 'rental.html' , context)

def deleteIha(request , id):
    iha = Kiralama.objects.filter(id = id)
    iha.delete()
    return redirect('rental')


def index(request):
    if request.user.is_authenticated:
        ihalar = Kiralama.objects.filter(kullanici = request.user)
    else:
        ihalar = 0
    kategoriler = Iha.objects.all()
    context={
        'kategoriler' :kategoriler,
        'ihalar' :ihalar
    }
    return render(request,'index.html',context)

def iha(request):
    if request.user.is_authenticated:
        ihalar = Kiralama.objects.filter(kullanici = request.user)
    else:
        ihalar = 0
    kategoriler = Iha.objects.all()
    context={
        'kategoriler' :kategoriler,
        'ihalar' :ihalar
    }
    return render(request,'iha.html',context)

def ihaDetay(request , ihaid):
    kategoriler = Iha.objects.all()
    ihaDetay = Iha.objects.get(slug = ihaid)
    if request.user.is_authenticated:
        ihalar = Kiralama.objects.filter(kullanici = request.user)
    else:
        ihalar = 0

    if 'listele' in request.POST:
        ihaId = request.POST['ihaid']
        iha = Iha.objects.get(id = ihaId)
        if Iha.objects.filter(kiralanacak__in =[request.user] , id = ihaId).exists():
            iha.kiralanacak.remove(request.user)
            iha.save()
        else:
            iha.kiralanacak.add(request.user)
            iha.save()

    if 'kirala' in request.POST:
        saat = int(request.POST.get('number'))
        if Kiralama.objects.filter(kullanici = request.user , iha = ihaDetay):
            iha = Kiralama.objects.get(kullanici = request.user , iha = ihaDetay)
            iha.kiralamaSaat += saat
            iha.kiralamaToplam += saat * ihaDetay.fiyat
            iha.save()
        else:
            kiralama = Kiralama(iha = ihaDetay , kullanici = request.user , kiralamaSaat = saat , kiralamaToplam = saat*ihaDetay.fiyat)
            kiralama.save()     

    context = {
        'ihaDetay' :ihaDetay,
        'kategoriler' :kategoriler,
        'ihalar' :ihalar
    }
    return render(request , 'iha-information.html',context)

def profil(request):
    kategoriler = Iha.objects.all()
    ihalar = Kiralama.objects.filter(kullanici = request.user)



    user = request.user
    
    favoriler = Iha.objects.filter(kiralanacak= request.user)

    context={
        'user' :user,
        'favoriler' :favoriler,
        'kategoriler' : kategoriler,
        'ihalar' :ihalar
    }

    return render(request,'profile.html',context)

def register(request):

    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        email = request.POST['email']
        isim = request.POST['isim']
        soyisim = request.POST['soyisim']
        sifre1 = request.POST['sifre1']
        sifre2=request.POST['sifre2']

        if sifre1 == sifre2:
            if User.objects.filter(username = kullanici).exists():
                messages.error(request , 'Kullanıcı adı sistemde mevcut!')
                return redirect('register')
            

            elif User.objects.filter(email = email).exists():
                messages.error(request , 'E-Posta adresi sistemde mevcut!')
                return redirect('register')
            
            elif len(sifre1) < 6 :
                messages.error(request , 'Şifre en az 6 karakter olmalıdır!')
                return redirect('register')
            
            else:
                user = User.objects.create_user(
                    username= kullanici , email=email , password= sifre1
                )
                Profil.objects.create(
                    kullanici = user ,
                    isim = isim ,
                    soyisim = soyisim
                )
                user.save()
                messages.success(request , 'Kayıt başarılı!')
                return redirect('login')
        else:
            messages.error(request , 'Şifreler uyuşmuyor!')
            return redirect('register')
    return render(request,'register.html')

def login (request):

    if request.method == 'POST':
        username = request.POST['kullanici']
        password = request.POST['sifre']

        user = authenticate(request, username = username , password = password)

        if user is not None:
            auth_login(request , user)
            messages.success(request , 'Giriş Başarılı!')
            return redirect('index')
        else:
            messages.error(request , 'Kullanıcı adı veya parola hatalı!')
            return redirect('login')
    return render(request,'login.html')

def logout_request(request):
    logout(request)
    return redirect ("index")


