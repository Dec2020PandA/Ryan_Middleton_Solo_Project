from django.db import models

class Category (models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    #products - a list of products that belong to this category
    #packages - a list of packages that belong to this category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
         return self.name

class ProductManager(models.Manager):
    def validate_data(self, postData):
        errors={}
        # if len(postData['name']) < 3:
        #      errors["author_txt"] = "The author must have at least 3 characters."
        # if len(postData['content_txt']) < 10:
        #      errors["content_txt"] = "The quote must have at least 10 characters."
        return errors

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, related_name="products", on_delete = models.CASCADE)
    accessories = models.ManyToManyField('self', blank=True)
    num_inventory = models.IntegerField(default=0)
    # quantity_in_order = models.IntegerField(default=0);
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

    def __str__(self): 
         return self.name

class Package(models.Model):
    name = models.CharField(max_length=255, default="No Name")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    num_inventory = models.IntegerField(default=1)
    category = models.ForeignKey(Category, null=True, related_name="packages", on_delete = models.CASCADE)
    products = models.ManyToManyField(Product, through='PackageItem')
    # quantity_in_order = models.IntegerField(default=0);
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self): 
        return str(self.name) 

class PackageItem(models.Model):
    package = models.ForeignKey(Package, null=True, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return str(self.package.name) + ": " + str(self.product.name) + " (" + str(self.quantity) + ")"

class OrderManager(models.Manager):
    def validate_data(self, postData):
        errors={}
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name_txt']) == 0:
             errors["name_txt"] = "The author must have at least 3 characters."
        if not EMAIL_REGEX.match(postData['email_txt']):
            errors['email'] = ("Invalid email address!")
        return errors  
  
class Order(models.Model):
    customer_id = models.CharField(null=True, max_length=255)
    customer_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='ProductsInOrder')
    packages = models.ManyToManyField(Package, through='PackagesInOrder')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()
    
    def __str__(self): 
        return "Order# " + str(self.id) + " for " + self.email
        
    def get_total(self):
        total = 0
        order_products = ProductsInOrder.objects.filter(order__id=self.id)
        order_packages = PackagesInOrder.objects.filter(order__id=self.id)
        for item in order_products:
            total += item.product.price * item.quantity
        for item in order_packages:
            total += item.package.price * item.quantity
        return total

class ProductsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return "Order#" + str(self.order.id) + ": " + str(self.product.name) + " (" + str(self.quantity) + ")"
    
    def get_total(self):
        return self.product.price * self.quantity

class PackagesInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return "Order#" + str(self.order.id) + ": " + str(self.package.name) + " (" + str(self.quantity) + ")"
    
    def get_total(self):
        return self.package.price * self.quantity
