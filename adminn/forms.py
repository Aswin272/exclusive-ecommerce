from django.forms import ModelForm
from products.models import Category,Product,ProductImage

class UpdateCategoryForm(ModelForm):
    class Meta:
        model=Category
        fields='__all__'
        
class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields=['name','description','price','Category','quantity','image']
        
class ProductImageForm(ModelForm):
    class Meta:
        model=ProductImage
        fields=['image']
        
class ProductUpdateForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'