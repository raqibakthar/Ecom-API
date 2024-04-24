from django.urls import path
from products.views import *
from accounts.views import MyTokenobtainPairView,RegisterUser
from users.views import getUserProfile,getUsers,updateUser,DeleteUser,UserUpdateById
from payments.views import PayPalPaymentView,PayPalPaymentExecuteView

urlpatterns = [

    path('users/login/', MyTokenobtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/',RegisterUser,name='user-register'),

    path('Products/',getProducts,name='Products'),
    path('Product/<str:pk>/',getProduct,name='Product'),
    path('top/product/',getTopProducts,name='top-Product'),

    # **Userside urls**
    path('users/profile/',getUserProfile,name='user-profile'),
    path('users/profile/update/',updateUser,name='user-update'),

    path('addorder/',addOrderItems,name='orders-add'),
    path('getorder/<str:pk>/',getOrderById,name='user-order'),
    path('<str:pk>/pay/',updateOrderToPaid,name='pay'),

    path('myorders/',getMyOrder,name='myorders'),

    path('Product/review/<str:pk>/',CreateProductReview,name='Product-review'),

    #PAYMENT
    path('payment/',PayPalPaymentView,name='payment-view'),
    path('payment/execute/',PayPalPaymentExecuteView,name='payment-execute-view'),



    # **Adminside urls**
    path('users/',getUsers,name='user'),
    path('user/update/<str:pk>/',UserUpdateById,name='user-update-by-id'),
    path('user/delete/<str:pk>/',DeleteUser,name='user-delete'),

    path('product/create/',CreateProduct,name='Product-create'),
    path('product/update/<str:pk>/',UpdateProduct,name='Product-update'),
    path('product/upload/image/',uploadImage,name='upload-image'),
    path('product/delete/<str:pk>/',DeleteProduct,name='Product-delete'),

    path('orders/',getOrder,name='orders'),
    path('orders/delivered/<str:pk>/',updateOrderToDelivered,name='orders-delivered'),

    

]
