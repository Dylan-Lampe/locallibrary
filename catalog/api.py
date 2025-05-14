from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import django_auth
from ninja.security import django_auth
from ninja.orm import create_schema

from .models import Author, Genre, Language, Book, BookInstance

router = Router(
    auth=django_auth,    # ← pass the callable itself, not django_auth()
)

# ––– Schemas –––
AuthorOut    = create_schema(Author,   name="AuthorOut")
AuthorIn     = create_schema(Author,   exclude=["id"],       name="AuthorIn")
GenreSchema  = create_schema(Genre,    name="GenreSchema")
LangSchema   = create_schema(Language, name="LangSchema")

# For nested and FK relations on Book & BookInstance:
BookOut      = create_schema(Book,     name="BookOut")
BookIn       = create_schema(Book,     exclude=["id"],       name="BookIn")
BookInstOut  = create_schema(BookInstance, name="BookInstanceOut")
BookInstIn   = create_schema(BookInstance, exclude=["id"],   name="BookInstanceIn")

# ––– CRUD for Author –––
@router.get("/authors/", response=List[AuthorOut])
def list_authors(request):
    return Author.objects.all()

@router.get("/authors/{id}/", response=AuthorOut)
def get_author(request, id: int):
    return get_object_or_404(Author, pk=id)

@router.post("/authors/", response=AuthorOut, auth=[django_auth])
def create_author(request, payload: AuthorIn):
    return Author.objects.create(**payload.dict())

@router.put("/authors/{id}/", response=AuthorOut, auth=[django_auth])
def update_author(request, id: int, payload: AuthorIn):
    author = get_object_or_404(Author, pk=id)
    for attr, val in payload.dict().items():
        setattr(author, attr, val)
    author.save()
    return author

@router.delete("/authors/{id}/", auth=[django_auth])
def delete_author(request, id: int):
    author = get_object_or_404(Author, pk=id)
    author.delete()

# ––– CRUD for Genre & Language –––
@router.get("/genres/", response=List[GenreSchema])
def list_genres(request):
    return Genre.objects.all()

@router.post("/genres/", response=GenreSchema, auth=[django_auth])
def create_genre(request, payload: GenreSchema):
    return Genre.objects.create(**payload.dict())

@router.get("/languages/", response=List[LangSchema])
def list_languages(request):
    return Language.objects.all()

@router.post("/languages/", response=LangSchema, auth=[django_auth])
def create_language(request, payload: LangSchema):
    return Language.objects.create(**payload.dict())

# ––– CRUD for Book –––
@router.get("/books/", response=List[BookOut])
def list_books(request):
    return Book.objects.all()

@router.get("/books/{id}/", response=BookOut)
def get_book(request, id: int):
    return get_object_or_404(Book, pk=id)

@router.post("/books/", response=BookOut, auth=[django_auth])
def create_book(request, payload: BookIn):
    return Book.objects.create(**payload.dict())

@router.put("/books/{id}/", response=BookOut, auth=[django_auth])
def update_book(request, id: int, payload: BookIn):
    book = get_object_or_404(Book, pk=id)
    for k, v in payload.dict().items():
        setattr(book, k, v)
    book.save()
    return book

@router.delete("/books/{id}/", auth=[django_auth])
def delete_book(request, id: int):
    get_object_or_404(Book, pk=id).delete()

# ––– CRUD for BookInstance –––
@router.get("/instances/", response=List[BookInstOut])
def list_instances(request):
    return BookInstance.objects.all()

@router.get("/instances/{id}/", response=BookInstOut)
def get_instance(request, id: int):
    return get_object_or_404(BookInstance, pk=id)

@router.post("/instances/", response=BookInstOut, auth=[django_auth])
def create_instance(request, payload: BookInstIn):
    return BookInstance.objects.create(**payload.dict())

@router.put("/instances/{id}/", response=BookInstOut, auth=[django_auth])
def update_instance(request, id: int, payload: BookInstIn):
    inst = get_object_or_404(BookInstance, pk=id)
    for k, v in payload.dict().items():
        setattr(inst, k, v)
    inst.save()
    return inst

@router.delete("/instances/{id}/", auth=[django_auth])
def delete_instance(request, id: int):
    get_object_or_404(BookInstance, pk=id).delete()