from django.shortcuts import redirect

def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('buyer_dashboard')  # Redirect to buyer dashboard if not a seller
    return wrapper
