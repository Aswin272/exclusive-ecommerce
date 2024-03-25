from django.shortcuts import render
from .models import Category,Product,ProductImage
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def index(request):
    category=Category.objects.filter(is_active=True)
    products=Product.objects.filter(Category__in=category,is_active=True)
    return render(request,'index.html',{'category':category,'products':products})

@never_cache
def product_detail_page(request,pk):
    product=Product.objects.get(id=pk)
    related_product=Product.objects.filter(Category=product.Category).exclude(id=pk)
    img=ProductImage.objects.filter(product=pk)
    for i in img:
        print(i.image.url)
    return render(request,'product_detail_page.html',{'products':product,'img':img,'related_products':related_product})



def all_products_list(request):
    active_categories = Category.objects.filter(is_active=True)
    products=Product.objects.filter(Category__in=active_categories,is_active=True)
    return render(request,'all_product_list.html',{'products':products})
    







# def product_list(request):
#     if request.method =='POST':
#         product_form=ProductForm(request.POST,request.FILES)
#         product_img=ProductImageForm(request.POST,request.FILES)

#         if product_form.is_valid():
#             product=product_form.save()
#             product_id=product.id
            
#             images=request.FILES.getlist('image')
#             for img in images:
#                 ProductImage.objects.create(product_id=product_id,image=img)
                
#         else:
#             print('forms are not valid',product_form.errors,product_img.errors)
#     else:
#         product_form=ProductForm()
        
#     return render(request,'admin_product.html',{'frm':product_form})