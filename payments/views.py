from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from paypalrestsdk import Payment

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PayPalPaymentView(request):
        
        data = request.data
        order_id = data.get('order_id')
        total_amount = data.get('total_price')
        print(total_amount)

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/payment/cancel/"
            },
            "transactions": [{
                    "amount": {
                        "total": total_amount,
                        "currency": "USD"  # Use a valid ISO currency code here
                    },
                    "description": "Payment for order {}".format(order_id)
            }]
        })

        if payment.create():
            # Redirect user to PayPal approval URL
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    return Response({"redirect_url": redirect_url})
        else:
            return Response({"error": payment.error})
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PayPalPaymentExecuteView(request):
        payer_id = request.GET.get('PayerID')
        payment_id = request.GET.get('paymentId')

        payment = Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            
            return Response({"status": "success"})
        else:
            return Response({"status": "error", "error": payment.error})