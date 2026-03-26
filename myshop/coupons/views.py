from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CouponApplyForm
from .models import Coupon

# Create your views here.
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        coupon_status = is_coupon_valid(code)
        if coupon_status["is_valid"]:
            request.session['coupon_id'] = coupon_status["coupon_id"]
        else:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

# my own addition to make coupon validation easier and more detailed across the project
def is_coupon_valid(coupon_id):
    now = timezone.now()
    
    # Check if coupon exists
    try:
        coupon = Coupon.objects.get(code__iexact=coupon_id)
    except Coupon.DoesNotExist:
        # add warning message
        return {"is_valid": False, "reason": "Coupon not found"}
    
    if not (coupon.valid_from <= now <= coupon.valid_to):
        # add warning message
        return {"is_valid": False, "reason": f"Coupon expired. Valid until {coupon.valid_to.strftime('%d/%m/%Y %H:%M')}"}
    
    if not coupon.active:
        # add warning message
        return {"is_valid": False, "reason": "Coupon is inactive"}
    
    return {"is_valid": True, "coupon_id": coupon.id}