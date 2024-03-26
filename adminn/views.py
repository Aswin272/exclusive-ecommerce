from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from products.models import Category,Product,ProductImage
from . forms import UpdateCategoryForm,ProductForm,ProductImageForm,ProductUpdateForm
from Customers.models import Customers
import base64
import re
from django.core.files.base import ContentFile
# Create your views here.

username='aswin'
password=12345


@never_cache
def adminn(request):
    if 'superuser' in request.session:       
        return redirect('adminn_dashboard')    
    if request.method=='POST':       
        username=request.POST.get('username')
        password=request.POST.get('password')      
        user=authenticate(username=username,password=password)       
        if user is not None:          
            request.session['superuser']=username
            return render(request,'admin_dashboard.html')             
    return render(request,'adminn_signin.html')

@never_cache
def adminn_dashboard(request):
    if 'superuser' in request.session:
        return render(request,'admin_dashboard.html')
    return redirect('adminn')

@never_cache
def logout(request):
    if 'username' in request.session:
        print("yesssss.......")
        request.session.flush() 
        return redirect('signin')
    if 'superuser' in request.session:
        request.session.flush()       
        return redirect('adminn')

# categoryyy----------------------------------------#

@never_cache
def category(request):
    if 'superuser' in request.session:
        
        category_instance=Category.objects.all()
        return render(request,'admin_category.html',{'categories':category_instance})

@never_cache
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')  # Get uploaded image file
        print(image_file)
        print(request.POST)
        if image_file is not None:
            # Read the image file content and encode it as base64
            imgstr = base64.b64encode(image_file.read()).decode()
            
            # Get image format from the file name
            format = image_file.name.split('.')[-1]
            
            # Decode base64 encoded image data
            image_data = 'data:image/' + format + ';base64,' + imgstr
            
            # Create a new Category object and assign the image_data to the image field
            new_category = Category(name=name, description=description, image=image_data)
            new_category.save()

            return redirect('category')  # Redirect to category list view
    
    return render(request, 'add_category.html')
@never_cache
# def add_category(request):
#     if request.method=='POST':
#         categ=request.POST.get('name')
#         description=request.POST.get('description')
#         image = request.FILES.get('image')
        
        
#         Category.objects.create(name=categ,description=description,image=image)
#         return redirect('category')
#     return render(request,'add_category.html')
@never_cache
def UpdateCategory(request,pk):
    if 'superuser' in request.session:
        instance=Category.objects.get(id=pk)
      
        f=UpdateCategoryForm(instance=instance)
        if request.POST:
            fm=UpdateCategoryForm(request.POST,request.FILES,instance=instance)
            
            if fm.is_valid():
                fm.save()
                return redirect('category')
            else:
                f=UpdateCategoryForm(instance=instance)
                
        return render(request,'admin_update_category.html',{'instance':instance,'f':f})
    return redirect('adminn')

def active_unactive_category(request,pk):
    print("reached")
    category=Category.objects.get(id=pk)
    if category.is_active:
        category.is_active = False
    else:
        category.is_active = True
    category.save()
    return redirect('category')

#product--------------------------------------
@never_cache
def product_list(request):
    products=Product.objects.all()
    return render(request,'admin_product_list.html',{'products':products})


@never_cache
def add_products(request):
    if request.method =='POST':
        product_form=ProductForm(request.POST,request.FILES)
        product_img=ProductImageForm(request.POST,request.FILES)

        if product_form.is_valid():
            product=product_form.save()
            product_id=product.id
            
            images=request.FILES.getlist('image')
            for img in images:
                ProductImage.objects.create(product_id=product_id,image=img)
            return redirect('product_list')
        else:
            print('forms are not valid',product_form.errors,product_img.errors)
    else:
        product_form=ProductForm()
        
    return render(request,'admin_add_product.html',{'frm':product_form})

def product_update(request,pk):
    instance_to_be_edited=Product.objects.get(id=pk)
    f=ProductUpdateForm(instance=instance_to_be_edited)
    if request.POST:
        
        form=ProductUpdateForm(request.POST,instance=instance_to_be_edited)
        if form.is_valid:
            form.save()
            print("saved")
            return redirect('product_list')
        else:
            f=ProductUpdateForm(instance=instance_to_be_edited)
            
    return render(request,'admin-product-update.html',{'form':f})
    
    
def active_unactive_product(request,pk):
    print("entered....")
    product=Product.objects.get(id=pk)
    if product.is_active:
        print("done")
        product.is_active=False
    else:
        product.is_active=True
    product.save()
    return redirect('product_list')
    



@never_cache
def admin_customer_list(request):
    customers=Customers.objects.all()
    return render(request,'admin_customers.html',{'customers':customers})
@never_cache
def listandunlistcustomer(request,pk):
    user = Customers.objects.get(id=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('admin-customers')