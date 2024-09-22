from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import Listing
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from .decorators import seller_required


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import LoginForm  # Import your login form

def custom_login_view(request):
    User = get_user_model()  # Get the custom user model
    next_url = request.GET.get('next', '')
    show_contact = request.GET.get('show_contact', '')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if the username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Username is not registered.')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_authenticated:
                        if next_url:
                            redirect_url = next_url
                            if show_contact == '1':
                                redirect_url += '?show_contact=1'
                            return redirect(redirect_url)
                        if user.is_buyer:
                            return redirect('buyer_dashboard')  # Redirect buyer to buyer dashboard
                        elif user.is_seller:
                            return redirect('seller_dashboard')  # Redirect seller to seller dashboard
                else:
                    messages.error(request, 'Invalid password.')  # Display error message for invalid password
    else:
        form = LoginForm()
    return render(request, 'accounts/custom_login.html', {'form': form})




def buyer_dashboard(request):
    return render(request, 'accounts/buyer_dashboard.html')


def seller_dashboard(request):
    return render(request, 'accounts/seller_dashboard.html')



from django.contrib.auth import get_user_model

def register_view(request):
    error_message = None  # Initialize error message variable
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            role = form.cleaned_data['role']

            User = get_user_model()  # Get the custom user model
            if User.objects.filter(username=username).exists():
                error_message = "Username already exists. Please choose a different username."
            else:
                user = User.objects.create_user(username=username, password=password, email=email, phone_number=phone_number, full_name=full_name)
                if role == 'buyer':
                    user.is_buyer = True
                elif role == 'seller':
                    user.is_seller = True
                user.save()
                if user.is_buyer:
                    return redirect('buyer_dashboard')
                elif user.is_seller:
                    return redirect('seller_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form, 'error_message': error_message})



def add_listing(request):
    # from .models import Category
    # categories = Category.objects.all()

    if request.method == 'POST':
        # Extract the data from the POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        # property_type = request.POST.get('property_type')
        # category_name_id = request.POST.get('category_name')  # Assuming you have a select input for categories
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        square_feet = request.POST.get('square_feet')
        year_built = request.POST.get('year_built')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        photo_main = request.FILES.get('photo_main')  # Assuming the main photo is uploaded as a file
        # Assuming other photos are uploaded similarly
        photo_1 = request.FILES.get('photo_1')
        photo_2 = request.FILES.get('photo_2')
        photo_3 = request.FILES.get('photo_3')
        photo_4 = request.FILES.get('photo_4')
        photo_5 = request.FILES.get('photo_5')
        photo_6 = request.FILES.get('photo_6')

        # Get the currently logged-in user as the seller
        seller = request.user

        # Create the listing object
        Listing.objects.create(
            seller=seller,
            title=title,
            description=description,
            # property_type=property_type,
            # category_name_id=category_name_id,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            square_feet=square_feet,
            year_built=year_built,
            phone_number=phone_number,
            email=email,
            photo_main=photo_main,
            photo_1=photo_1,
            photo_2=photo_2,
            photo_3=photo_3,
            photo_4=photo_4,
            photo_5=photo_5,
            photo_6=photo_6
        )

        # Display a success message
        messages.success(request, 'Listing added successfully')

        # Redirect to the seller dashboard
        return redirect('seller_dashboard')

    return render(request, 'accounts/add_listing.html')


def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo_main']:
        # Process file upload
        uploaded_photo = request.FILES['photo_main']
        # Save the uploaded photo to the appropriate location
        # You may need to adjust the save path based on your settings
        # Example: with open('path/to/uploaded/photo.jpg', 'wb+') as destination:
        #              for chunk in uploaded_photo.chunks():
        #                  destination.write(chunk)

        # Now that the file is saved, you can check if it exists in the database
        if Listing.objects.filter(photo_main='path_to_uploaded_image').exists():
            print("Uploaded photo exists in the database.")
        else:
            print("Uploaded photo does not exist in the database.")

        # Redirect or render a response
        return render(request, 'upload_success.html')
    else:
        return render(request, 'upload_form.html')


@login_required(login_url='/login/')
@seller_required 
def seller_dashboard(request):
    if request.user.is_authenticated:
        # Filter listings to only include those owned by the current user
        listings = Listing.objects.filter(seller=request.user)
        # print("User:", request.user)
        # print("Listings:", listings)
        return render(request, 'accounts/seller_dashboard.html', {'listings': listings})
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')


def buyer_dashboard(request):
    # Retrieve all listings for display on the buyer dashboard
    listings = Listing.objects.all()
    return render(request, 'accounts/buyer_dashboard.html', {'listings': listings})


def book_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    # Logic to handle booking action (redirect to booking form or perform booking)
    # (You can define the logic as per your requirements)
    return redirect(reverse('buyer_dashboard'))  # Redirect back to buyer dashboard after booking


def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        # Update the listing with the form data
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.address = request.POST.get('address')
        listing.city = request.POST.get('city')
        listing.state = request.POST.get('state')
        listing.zipcode = request.POST.get('zipcode')
        listing.price = request.POST.get('price')
        listing.bedrooms = request.POST.get('bedrooms')
        listing.bathrooms = request.POST.get('bathrooms')
        listing.square_feet = request.POST.get('square_feet')
        listing.year_built = request.POST.get('year_built')
        # listing.photo_main = request.POST.get('photo_main')
        listing.save()
        # Redirect back to the seller dashboard after updating
        return redirect('seller_dashboard')
    return render(request, 'accounts/edit_listing.html', {'listing': listing})


def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    # Logic to handle deleting the listing
    listing.delete()
    return redirect('seller_dashboard')


def custom_logout(request):
    logout(request)
    # Redirect to the home page or any other page after logout
    return redirect('buyer_dashboard')


def listing_detail_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'accounts/listing_detail.html', {'listing': listing})




from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Inquiry

# views.py

from django.shortcuts import render, redirect
from .forms import InquiryForm

def contact_us(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page after submission
    else:
        form = InquiryForm()
    return render(request, 'accounts/contact_us.html', {'form': form})
 
def success_page(request):
    return render(request, 'accounts/success.html')



from .forms import PropertySearchForm

def search_listings(request):
    form = PropertySearchForm(request.GET or None)
    listings = Listing.objects.all()

    if form.is_valid():
        if form.cleaned_data['city']:
            listings = listings.filter(city__icontains=form.cleaned_data['city'])
        if form.cleaned_data['min_price']:
            listings = listings.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            listings = listings.filter(price__lte=form.cleaned_data['max_price'])
        if form.cleaned_data['bedrooms']:
            listings = listings.filter(bedrooms__gte=form.cleaned_data['bedrooms'])
        if form.cleaned_data['bathrooms']:
            listings = listings.filter(bathrooms__gte=form.cleaned_data['bathrooms'])

    return render(request, 'accounts/search_results.html', {'form': form, 'listings': listings})