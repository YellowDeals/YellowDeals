from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
import os
from geopy.distance import geodesic

class Admin(models.Model):
    admin_id = models.CharField(max_length=6, primary_key=True)
    admin_username = models.CharField(max_length=50)
    admin_pass = models.CharField(max_length=128)
    admin_email = models.CharField(max_length=50)
    admin_tel = models.CharField(max_length=10, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.admin_username
    
    def get_email_field_name(self):
        return 'admin_email'
    
    @property
    def password(self):
        return self.admin_pass

    class Meta:
        db_table = "Admin"
        ordering = ['admin_id']

class GeneralUser(models.Model):
    customer_id = models.CharField(max_length=6, primary_key=True)
    customer_username = models.CharField(max_length=50)
    customer_pass = models.CharField(max_length=128)
    customer_email = models.CharField(max_length=50)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.customer_username

    def get_email_field_name(self):
        return 'customer_email'

    @property
    def password(self):
        return self.customer_pass

    class Meta:
        db_table = "GeneralUser"
        ordering = ['customer_id']

class TypeStore(models.Model):
    typeStore_id = models.CharField(max_length=6, primary_key=True)
    typeStore_name = models.CharField(max_length=50)

    def __str__(self):
        return self.typeStore_name

    class Meta:
        db_table = "TypeStore"
        ordering = ['typeStore_id']

class Categories(models.Model):
    categories_id = models.AutoField(primary_key=True)
    categories_name = models.CharField(max_length=50)

    def __str__(self):
        return self.categories_name

    class Meta:
        db_table = "Categories"
        ordering = ['categories_id']

class TypeProduct(models.Model):
    productType_id = models.AutoField(primary_key=True)
    productType_name = models.CharField(max_length=50)

    def __str__(self):
        return self.productType_name

    class Meta:
        db_table = "TypeProduct"
        ordering = ['productType_id']
        
class TypeComplaint(models.Model):
    typeComplaint_id = models.AutoField(primary_key=True)
    typeComplaint_name = models.CharField(max_length=50)

    def __str__(self):
        return self.typeComplaint_name

    class Meta:
        db_table = "TypeComplaint"
        ordering = ['typeComplaint_id']

        
def store_image_upload_to(instance, filename):
    # ตั้งชื่อโฟลเดอร์เป็นชื่อร้าน
    store_name = instance.store_name if instance.store_name else 'default_store'
    return os.path.join('documents', 'shop', store_name, filename)

class StoreOwner(models.Model):
    store_owner_id = models.CharField(max_length=6, primary_key=True)
    store_username = models.CharField(max_length=50)
    store_pass = models.CharField(max_length=128)
    store_name = models.CharField(max_length=100)
    store_email = models.CharField(max_length=50)
    store_tel = models.CharField(max_length=10)
    store_address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True) 
    longitude = models.FloatField(null=True, blank=True)

    # ใช้ ImageField สำหรับเก็บ URL ของรูปภาพ
    store_image_url = models.ImageField(
        upload_to=store_image_upload_to,
        blank=True,  # สามารถเว้นว่างได้
        null=True,   # สามารถเก็บค่า null ได้
        default='../static/images/Default1.png'  # รูปเริ่มต้น
    )

    store_branch = models.CharField(max_length=50, blank=True, null=True)  # ปรับให้สามารถเป็นค่าว่างได้
    typeStore = models.ForeignKey('TypeStore', on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'รอการตรวจสอบ'), # ร้านรอการตรวจสอบจากแอดมิน
            ('need_info', 'รอข้อมูลเพิ่มเติม'), # กรณีแอดมินปฎิเสธการสมัคร
            ('active', 'กำลังใช้งาน'),     # ร้านที่แอดมินยอมรับแล้ว
            ('banned', 'ถูกแบน'),          # ร้านที่ถูกแบน
        ],
        default='pending',  # ค่าเริ่มต้นเป็น 'รอการตรวจสอบ'
    )

    note = models.TextField(blank=True, null=True)  
    last_login = models.DateTimeField(null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)
    
    def has_location(self):
            return self.latitude is not None and self.longitude is not None

    def distance_to(self, lat, lng):
        if not self.has_location():
            return None
        return geodesic((self.latitude, self.longitude), (lat, lng)).km

    def __str__(self):
        return self.store_name

    def get_email_field_name(self):
        return 'store_email'

    @property
    def password(self):
        return self.store_pass

    class Meta:
        db_table = "StoreOwner"
        ordering = ['store_owner_id']

def product_image_upload_to(instance, filename):
    return os.path.join('static', 'images', 'products', str(instance.store_owner.store_owner_id), filename)

class Product(models.Model):
    product_id = models.CharField(max_length=12, primary_key=True)
    store_owner = models.ForeignKey('StoreOwner', on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_date = models.DateTimeField(auto_now_add=True)
    product_details = models.CharField(max_length=255)
    view_count = models.IntegerField(default=0)
    product_image = models.ImageField(
    upload_to=product_image_upload_to,
    blank=True,
    null=True,
    default='../static/images/product.png'
)
    product_type = models.ForeignKey('TypeProduct', on_delete=models.CASCADE)
    categories = models.ForeignKey('Categories', on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)  
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        """กำหนดรหัสสินค้าอัตโนมัติหากยังไม่มี และเรียงตามลำดับสินค้าในร้านนั้น"""
        if not self.product_id:
            # ดึงร้านค้าปัจจุบัน
            store_owner_id = self.store_owner.store_owner_id

            # หาค่าสูงสุดของรหัสสินค้าของร้านนี้
            last_product = Product.objects.filter(store_owner=self.store_owner).order_by('product_id').last()

            # ถ้ามีสินค้าในร้านนั้นแล้ว ให้เพิ่ม 1 ให้กับลำดับ
            if last_product:
                last_number = int(last_product.product_id[-3:])  # ดึง 3 ตัวสุดท้ายจากรหัสสินค้า
                new_number = last_number + 1
            else:
                new_number = 1

            # สร้างรหัสสินค้าใหม่
            self.product_id = f'{store_owner_id}{new_number:03d}'

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "Product"
        ordering = ['product_id']

def complaint_image_upload_to(instance, filename):
    # ถ้าไม่มีร้านค้าให้ใช้ชื่อ 'general'
    if instance.store_owner and instance.store_owner.store_name:
        store_name = instance.store_owner.store_name
    else:
        store_name = 'general'

    # sanitize: ลบอักขระไม่ปลอดภัยจากชื่อร้าน
    store_name = re.sub(r'[^\w\s-]', '', store_name).strip().replace(' ', '_')

    return os.path.join('documents', 'complaint', store_name, filename)

class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(GeneralUser, on_delete=models.CASCADE)
    store_owner = models.ForeignKey(StoreOwner, on_delete=models.SET_NULL, null=True, blank=True)
    store_complainer = models.ForeignKey(StoreOwner, on_delete=models.SET_NULL, null=True, blank=True, related_name='store_complaints')
    complaint_text = models.CharField(max_length=255)
    complaint_status = models.CharField(max_length=50)
    type_complaint = models.ForeignKey(TypeComplaint, on_delete=models.CASCADE, default=1)
    complaint_date = models.DateTimeField()
    complaint_image = models.ImageField(
        upload_to=complaint_image_upload_to,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Complaint {self.complaint_id}"

    class Meta:
        db_table = "Complaint"
        ordering = ['complaint_id']

class SavedProduct(models.Model):
    saved_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(GeneralUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    saved_date = models.DateTimeField()
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"Saved {self.product.product_name} by {self.customer.customer_username}"

    class Meta:
        db_table = "SavedProduct"
        ordering = ['saved_id']



