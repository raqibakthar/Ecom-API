from rest_framework.response import  Response
from rest_framework.decorators import api_view,permission_classes

from .models import Product,Order,ShippingAddress,OrderItems,Review
from .serializers import ProductSerializer,OrderSerializer

from rest_framework import status

from rest_framework.permissions import IsAuthenticated,IsAdminUser

from datetime import datetime
from django.core.paginator import Paginator



@api_view(['GET'])
def getProducts(request):
        try:
            products = Product.objects.all()
            if request.GET.get('search'):
                search = request.GET.get('search')
                products = products.filter(name__icontains=search)
            page_naumber = request.GET.get('page',1)
            paginator = Paginator(products,100)
            serializer = ProductSerializer(paginator.page(page_naumber), many=True)
            if serializer.is_valid:
                return Response({
                    'data': serializer.data,
                    'message': 'products fetched successfully'
                })
            else:
                return Response({
                    'data': serializer.errors,
                    'message': 'validation error'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProduct(request,pk):
    try:
        products = Product.objects.get(product_id=pk)
        serializer = ProductSerializer(products, many=False)
        if serializer.is_valid:
            return Response({
                'data': serializer.data,
                'message': 'product fetched successfully'
            })
        else:
            return Response({
                'data': serializer.errors,
                'message': 'validation error'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(e)
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getTopProducts(request):
        try:
            products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
            serializer = ProductSerializer(products, many=True)
            if serializer.is_valid:
                return Response({
                    'data': serializer.data,
                    'message': 'top products fetched successfully'
                })
            else:
                return Response({
                    'data': serializer.errors,
                    'message': 'validation error'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# **Userside functionalities**

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):

    user = request.user
    data = request.data

    orderItems = data['orderitems']

    if orderItems and len(orderItems) == 0:

        return Response({
            'data':{},
            'massage':'No order items'
        },status=status.HTTP_400_BAD_REQUEST)
    
    else:
        
        order = Order.objects.create(
            user=user,
            payment_method = data['payment_method'],
            tax_price = data['tax_price'],
            shipping_price = data['shipping_price'],
            total_price = data['total_price']
        )

        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['address'],
            city = data['city'],
            postal_code = data['postal_code'],
            country = data['country']
        )

        for item in orderItems:
            product = Product.objects.get(product_id=item['product'])
            item = OrderItems.objects.create(
                product = product,
                order=order,
                name = product.name,
                qty = item['qty'],
                price = item['price'],
                image = product.image.url,   
            )

            product.countInStock = product.countInStock-item.qty
            product.save()
        
        serializer = OrderSerializer(order,many=False)
        return Response(
            {
                'data': serializer.data,
                'message':'done'
            },status=status.HTTP_200_OK
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request,pk):

    user = request.user

    try:
        order = Order.objects.get(order_id=pk)
        
        if user.is_staff or order.user == user :
            serializer =  OrderSerializer(order,many=False)
            return Response({
                "data":serializer.data,
                "message":"order fetched"
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "data":{},
                "message":"Not authorized to view this order"
            },status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrder(request):
    try:
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders,many=True)
        return Response({
                    "data":serializer.data,
                    "message":"your orders fetched"
                },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request,pk):
     try:
        order = Order.objects.get(order_id=pk)

        order.is_paid = True
        order.paid_at = datetime.now()

        order.save()

        return Response({
            "data":{},
            "message":"Order Paid"
        },status=status.HTTP_200_OK)
     except Exception as e:
         return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateProductReview(request,pk):
    try:
        data = request.data
        user = request.user
        product = Product.objects.get(product_id=pk)

        alredyExist = product.review_set.filter(user=user).exists()

        if alredyExist:
            return Response({
                'data': {},
                'message': 'Reviewed already'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif data['rating'] == 0:
            return Response({
                'data': {},
                'message': 'Put your rating first'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            review = Review.objects.create(

                user=user,
                product = product,
                name = user.first_name,
                rating = data['rating'],
                comment = data['comment']

            )

            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            total=0
            for i in reviews:
                total = total+i.rating
            
            product.rating = total / len(reviews)

            product.save()

            return Response(
                {
                    'data':{},
                    'message':"review added successful"
                },status=status.HTTP_201_CREATED
            )
            
    except Exception as e:
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# **Adminside functionalities**
    
@api_view(['POST'])     
@permission_classes([IsAdminUser])
def CreateProduct(request):
    try:
        user = request.user

        product=Product.objects.create(

            user=user,
            name = 'sample_name',
            price = 0000,
            brand = 'sample_brand',
            countInStock = 0,
            category = 'sample_category',
            description = ''

        )
        serializer = ProductSerializer(product,many=False)
        return Response({
            'data': serializer.data,
            'message': 'product created successful'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
         print(e)
         return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def UpdateProduct(request,pk):
    try:
        product = Product.objects.get(product_id=pk)

        product.name = request.data['name']
        product.price = request.data['price']
        product.brand = request.data['brand']
        product.countInStock = request.data['countInStock']
        product.category = request.data['category']
        product.description = request.data['description']

        product.save()

        serializer = ProductSerializer(product,many=False,partial=True)

        return Response({
            'data': serializer.data,
            'message': 'product updated successful'
        }, status=status.HTTP_200_OK)

    except Exception as e:
         return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def uploadImage(request):
    try:
        data = request.data

        product_id = data['product_id']
        product=Product.objects.get(product_id=product_id)
        product.image = request.FILES.get('image')

        product.save()

        return Response({
            'data': {},
            'message': 'product image uploaded'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
         return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def DeleteProduct(request,pk):
    try:
        product = Product.objects.get(product_id=pk)
        product.delete()
        return Response({
                "data":{},
                "message":"Product deleted successful"
            },status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrder(request):
    try:
        orders = Order.objects.all()
        serializer = OrderSerializer(orders,many=True)
        return Response({
                    "data":serializer.data,
                    "message":"all orders fetched"
                },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request,pk):
     try:
        order = Order.objects.get(order_id=pk)

        order.is_delivered = True
        order.delivered_at = datetime.now()

        order.save()

        return Response({
            "data":{},
            "message":"Order delivered"
        },status=status.HTTP_200_OK)
     except Exception as e:
         return Response({
            'data': {},
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

