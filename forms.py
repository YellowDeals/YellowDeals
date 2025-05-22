from django import forms
import re
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import StoreOwner, TypeStore,Admin, GeneralUser, StoreOwner,TypeComplaint
from .models import Product, TypeProduct, Categories
from django.forms.widgets import FileInput

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกชื่อผู้ใช้'})
    )
    password = forms.CharField(
        label="รหัสผ่าน",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกรหัสผ่าน', 'id': 'password'})
    )
class GeneralUserRegistrationForm(forms.ModelForm):
    # กำหนดฟอร์มลงทะเบียนสำหรับลูกค้า
    class Meta:
        model = GeneralUser
        fields = ['customer_id', 'customer_username', 'customer_pass', 'customer_email']
        widgets = {
            'customer_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกหมายเลขลูกค้า'}),
            'customer_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกชื่อผู้ใช้'}),
            'customer_pass': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกรหัสผ่าน'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกอีเมล'}),
        }
    
    # เพิ่ม validation สำหรับรหัสผ่านเพื่อความปลอดภัย
    def clean_customer_pass(self):
        password = self.cleaned_data.get('customer_pass')
        if len(password) < 6:
            raise forms.ValidationError("รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร")
        return password
    
class StoreOwnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = StoreOwner
        fields = ['store_username', 'store_pass', 'store_name', 'store_email', 'store_tel', 'store_address', 'store_branch', 'typeStore']
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกชื่อร้าน'}),
            'store_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกชื่อผู้ใช้ร้าน'}),
            'store_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกอีเมลร้าน'}),
            'store_tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'กรุณากรอกหมายเลขโทรศัพท์',
                'pattern': r'^\d{10}$',  # กำหนดให้กรอกได้แค่ตัวเลข 10 หลัก
                'inputmode': 'numeric',  # ช่วยให้แป้นพิมพ์แสดงเฉพาะตัวเลขในมือถือ
                'required': True
            }),
            'store_pass': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกรหัสผ่านอย่างน้อย 8 ตัวอักษร','id': 'password'}),
            'store_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกที่อยู่ร้านให้ครบถ้วน', 'style': 'height: 150px; width: 100%;'}),
            'store_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรุณากรอกสาขาร้าน (ถ้ามี)', 'required': False}),
            'typeStore': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_store_tel(self):
        store_tel = self.cleaned_data.get('store_tel')
        if not re.match(r'^\d{10}$', store_tel):
            raise ValidationError('กรุณากรอกหมายเลขโทรศัพท์ 10 หลักเท่านั้น')
        return store_tel

    def clean_store_pass(self):
        password = self.cleaned_data.get('store_pass')
        if len(password) < 8:
            raise ValidationError("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValidationError("รหัสผ่านต้องประกอบด้วยตัวอักษรและตัวเลข")
        return password

    def clean_store_email(self):
        email = self.cleaned_data.get('store_email')
        if StoreOwner.objects.filter(store_email=email).exists():
            raise ValidationError("อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้เมลใหม่")
        return email

    
class TypeStoreSelectionForm(forms.ModelForm):
    class Meta:
        model = TypeStore
        fields = ['typeStore_name']
        widgets = {
            'typeStore_name': forms.Select(attrs={'class': 'form-control'}),
        }
class AdminRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="รหัสผ่าน")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="ยืนยันรหัสผ่าน")

    class Meta:
        model = Admin
        fields = ['admin_username', 'admin_email', 'password', 'confirm_password']
        labels = {
            'admin_username': 'ชื่อผู้ใช้',
            'admin_email': 'อีเมล',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่")
        

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="อีเมล", max_length=254)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # ตรวจสอบในตาราง Admin
        if Admin.objects.filter(admin_email=email).exists():
            return email
        # ตรวจสอบในตาราง GeneralUser
        elif GeneralUser.objects.filter(customer_email=email).exists():
            return email
        # ตรวจสอบในตาราง StoreOwner
        elif StoreOwner.objects.filter(store_email=email).exists():
            return email
        else:
            raise ValidationError("อีเมลนี้ไม่ได้ลงทะเบียนในระบบ")
        

class CustomSetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="รหัสผ่านใหม่",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label="ยืนยันรหัสผ่านใหม่",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่อีกครั้ง")
        
        return cleaned_data

class TypeComplaintForm(forms.ModelForm):
    class Meta:
        model = TypeComplaint
        fields = ['typeComplaint_name']
        labels = {
            'typeComplaint_name': 'ชื่อประเภทคำร้อง',
        }
        widgets = {
            'typeComplaint_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'กรุณากรอกชื่อประเภทคำร้อง',
                'style': 'font-size: 18px; border: 2px solid #000;'
            }),
        }


class TypeProductForm(forms.ModelForm):
    class Meta:
        model = TypeProduct
        fields = ['productType_name']
        labels = {
            'productType_name': 'ชื่อประเภทสินค้า',
        }
        widgets = {
            'productType_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'กรุณากรอกชื่อประเภทสินค้า',
                'style': 'font-size: 18px; border: 2px solid #000;'
            }),
        }

class TypeStoreForm(forms.ModelForm):
    class Meta:
        model = TypeStore
        fields = ['typeStore_name']
        labels = {
            'typeStore_name': 'ชื่อประเภทของร้าน',
        }
        widgets = {
            'typeStore_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'กรุณากรอกชื่อประเภทของร้าน',
                'style': 'font-size: 18px; border: 2px solid #000;'
            }),
        }

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['categories_name']
        labels = {
            'categories_name': 'ชื่อหมวดหมู่',
        }
        widgets = {
            'categories_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'กรุณากรอกชื่อหมวดหมู่',
                'style': 'font-size: 18px; border: 2px solid #000;'
            }),
        }


class ProductForm(forms.ModelForm):
    product_image = forms.ImageField(
        required=False,
        label='รูปสินค้า',
        widget=FileInput  # เปลี่ยน widget เพื่อไม่แสดงลิงก์ URL
    )

    class Meta:
        model = Product
        fields = [
            'product_name',
            'original_price',
            'product_price',
            'product_details',
            'product_image',
            'product_type',
            'categories',
            'start_time',
            'end_time',
        ]
        widgets = {
            'product_details': forms.Textarea(attrs={
            'class': 'custom-textarea',
            'style': 'min-height: 100px; max-height: 200px; width: 100%;',
            'rows': 4,
        }),
            'start_time': forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
            'end_time': forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        }
        labels = {
            'product_name': 'ชื่อสินค้า',
            'original_price': 'ราคาก่อนลดราคา',
            'product_price': 'หลังลดราคา',
            'product_details': 'รายละเอียดสินค้า',
            'product_image': 'รูปสินค้า',
            'product_type': 'ประเภทสินค้า',
            'categories': 'หมวดหมู่สินค้า',
            'start_time': 'วันเริ่มขาย',
            'end_time': 'วันหมดเวลาขาย',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.start_time:
                self.fields['start_time'].initial = self.instance.start_time.strftime('%Y-%m-%dT%H:%M')
            if self.instance.end_time:
                self.fields['end_time'].initial = self.instance.end_time.strftime('%Y-%m-%dT%H:%M')

                
class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = StoreOwner
        fields = [
            'store_name',
            'store_email',
            'store_tel',
            'store_address',
            'store_image_url',
            'store_branch',
            'typeStore',
        ]
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control'}),
            'store_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'store_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'store_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'store_image_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'store_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'typeStore': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'store_name': 'ชื่อร้าน',
            'store_email': 'อีเมล',
            'store_tel': 'เบอร์โทร',
            'store_address': 'ที่อยู่',
            'store_image_url': 'รูปโปรไฟล์ร้าน',
            'store_branch': 'สาขา',
            'typeStore': 'ประเภทร้าน',
        }

    def clean_store_tel(self):
        tel = self.cleaned_data.get('store_tel')
        if not re.fullmatch(r'0\d{9}', tel):
            raise forms.ValidationError("เบอร์โทรต้องขึ้นต้นด้วย 0 และมีทั้งหมด 10 หลัก")
        return tel