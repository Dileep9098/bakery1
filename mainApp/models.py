from django.db import models

    
class Flavour(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=50)       

     def __str__(self) :
         return self.name
     
class CakeType(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=50)       

     def __str__(self) :
         return self.name

class Shape(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=50)       

     def __str__(self) :
         return self.name
     
class Product(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=50) 

     flavour=models.ForeignKey(Flavour,on_delete=models.CASCADE)      
     cakeType=models.ForeignKey(CakeType,on_delete=models.CASCADE)      
     shape=models.ForeignKey(Shape,on_delete=models.CASCADE)
     weight=models.IntegerField() 
     color=models.CharField(max_length=50) 
     stack=models.CharField(max_length=50,default="In Stock",null=True,blank=True) 

     description=models.TextField()
     baseprice=models.IntegerField() 
     discount=models.IntegerField() 
     finalprice=models.IntegerField() 
     pic1=models.ImageField(upload_to="upload",default="",null=True,blank=True)

     def __str__(self) :
         return self.name
     
class Buyer(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=50) 
     username=models.CharField(max_length=50) 
     email=models.EmailField(max_length=50) 
     phone=models.CharField(max_length=15) 
     addressline1=models.CharField(max_length=150) 
     addressline2=models.CharField(max_length=150) 
     addressline3=models.CharField(max_length=150) 
     pin=models.CharField(max_length=10) 
     city=models.CharField(max_length=50) 
     state=models.CharField(max_length=50) 
     pic=models.ImageField(upload_to="upload",default="",null=True,blank=True)
     otp=models.IntegerField(default=-121123)

     def __str__(self):
         return str(self.id)+" "+self.username

     
class Wishlist(models.Model):
     id=models.AutoField(primary_key=True)
     user=models.ForeignKey(Buyer,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     
     def __str__(self):
         return str(self.id)+" "+self.user.username+" "+self.product.name


status = ((0,"Order Placed"),(1,"Not Packed"),(2,"Packed"),(3,"Ready to Ship"),(4,"Shipped"),(5,"Out For Delivery"),(6,"Delivered"),(7,"Cancelled"))
payment = ((0,"Pending"),(1,"Done"))
mode = ((0,"COD"),(1,"Net Banking"))
class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    total = models.IntegerField()
    shipping = models.IntegerField()
    final = models.IntegerField()
    rppid = models.CharField(max_length=30,default="",null=True,blank=True)
    date = models.DateTimeField(auto_now=True)
    paymentmode = models.IntegerField(choices=mode,default=0)
    paymentstatus = models.IntegerField(choices=payment,default=0)
    orderstatus = models.IntegerField(choices=status,default=0)

    def __str__(self):
        return str(self.id)+" "+self.user.username


class CheckoutProducts(models.Model):
    id = models.AutoField(primary_key=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    p = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)+" "+str(self.checkout.id)


conatctstatus = ((0,"Active"),(1,"Done"))
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=500,null=True)
    status = models.IntegerField(choices=conatctstatus,default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.subject