from django.contrib import admin
from models import Article, Comments

class ArticleInLine(admin.StackedInline):
    model = Comments
    extra = 2

class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_date', 'article_text']
    inlines = [ArticleInLine]
    list_filter = ['article_date']

admin.site.register(Article, ArticleAdmin)
