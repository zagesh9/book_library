from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, BookForm
from .models import Book
from django.contrib import messages
from .scraper import BookScraper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('books')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('books')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('books')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('books')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def books(request):
    category = request.GET.get('category', '')
    
    # Get books filtered by category or all books
    if category:
        books = Book.objects.filter(genre=category)
    else:
        books = Book.objects.all()
    
    # Paginate the books (10 books per page)
    paginator = Paginator(books, 9)
    
    # Get the current page number
    page = request.GET.get('page', 1)
    
    try:
        # Get the books for the current page
        books_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        books_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        books_page = paginator.page(paginator.num_pages)
    
    # Get unique genres for dropdown
    genres = Book.objects.values_list('genre', flat=True).distinct()
    
    return render(request, 'user/books.html', {
        'books': books_page,
        'genres': genres,
        'category': category
    })

@login_required
def add_book(request):
	if request.method == 'POST':
	    form = BookForm(request.POST)
	    if form.is_valid():
	        try:
	            book = form.save()
	            messages.success(request, f'Book "{book.title}" added successfully!')
	            return redirect('books')
	        except Exception as e:
	            messages.error(request, f'Error adding book: {str(e)}')
	else:
	    form = BookForm()
	genre_choices = Book.genre

	return render(request, 'admin/add_book.html', {'form': form,'genre_choices': genre_choices})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                book = form.save()
                messages.success(request, f'Book "{book.title}" updated successfully!')
                return redirect('books')
            except Exception as e:
                messages.error(request, f'Error updating book: {str(e)}')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'admin/edit_book.html', {
        'form': form,
        'book': book
    })

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'user/book_details.html', {'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        try:
            book_title = book.title
            book.delete()
            messages.success(request, f'Book "{book_title}" deleted successfully!')
            return redirect('books')
        except Exception as e:
            messages.error(request, f'Error deleting book: {str(e)}')
    
    return redirect('books')


@login_required
def scrape_books(request):
    # Get all categories when the page loads
    categories = BookScraper.get_all_categories()
    
    # Optional: Update the Book model's GENRE_CHOICES
    Book.GENRE_CHOICES = [
        (
            category['name'].lower().replace(' ', '-'), 
            category['name']
        ) for category in categories
    ]
    
    context = {
        'categories': categories
    }
    
    if request.method == 'POST':
        category_name = request.POST.get('category')
        
        # Find the full category info
        category_info = next(
            (cat for cat in categories if cat['name'] == category_name), 
            None
        )
        
        if category_info:
            # Perform scraping for the selected category
            scraped_books = BookScraper.scrape_category(category_info)
            
            context.update({
                'scraped_books': scraped_books,
                'selected_category': category_name
            })
    
    return render(request, 'admin/scrape_books.html', context)