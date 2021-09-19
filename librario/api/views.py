from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Book, Review, Author
from .serializers import BookSerializer,ReviewSerializer,AuthorSerializer


# Create your views here.
@api_view(['GET'])
def listBooks(request):
    books = Book.objects.all()
    serialized_books = BookSerializer(books,many=True).data
    return Response({'success':True,'books':serialized_books})

@api_view(['POST'])
def addBook(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    pages = request.POST.get('pages')
    image = request.POST.get('image')
    category = request.POST.get('category')
    tag = request.POST.get('tag')
    
    if not all([title,author,pages,category,tag]):
        return Response({'success':False,'Message':'params missing'})
    
    author_obj = Author.objects.get(id=int(author))

    new_book = Book.objects.create(title=title, author=author_obj, pages=pages)
    serialized_book = BookSerializer(new_book).data

    return Response({'success':True,'new_book':serialized_book})

@api_view(['GET'])
def listAuthors(request):
    authors = Author.objects.all()
    serialized_authors = AuthorSerializer(authors,many=True).data
    return Response({'success':True,'authors':serialized_authors})

@api_view(['POST'])
def addAuthor(request):
    name = request.POST.get('name')
    age = request.POST.get('age')
    
    if not all([name,age]):
        return Response({'success':False})
    
    new_author = Author.objects.create(name=name,age=age)
    serialized_author = AuthorSerializer(new_author).data

    return Response({'success':True,'author':serialized_author})

@api_view(['GET'])
def listReviews(request):
    reviews = Review.objects.all()
    serialized_reviews = ReviewSerializer(reviews,many=True).data

    return Response({'success':True,'reviews':serialized_reviews})


@api_view(['GET'])
def listReviewsFromBook(request,book_id):
    if book_id:
        reviews = Review.objects.all().filter(book=book_id)
    else:
        reviews = Review.objects.all()
    serialized_reviews = ReviewSerializer(reviews,many=True).data

    return Response({'success':True,'reviews':serialized_reviews})

@api_view(['POST'])
def addReview(request,book_id):
    stars = request.POST.get('stars')
    description = request.POST.get('description')
    recomends = request.POST.get('recomends')

    if not all([stars,description,recomends]):
        return Response({'Success':False})
    
    user = User.objects.get(id=1)
    book = Book.objects.get(id=book_id)

    new_review = Review.objects.create(stars=stars,description=description,recomends=bool(recomends),user=user,book=book)
    serialized_review = ReviewSerializer(new_review).data
    
    return Response({'success':True,'review':serialized_review})