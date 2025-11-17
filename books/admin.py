from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_display = ('title', 'description', 'isbn')

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    list_display = ('first_name', 'last_name', 'email')

class BookAuthorAdmin(admin.ModelAdmin):
    pass

class BookReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)