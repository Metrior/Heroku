from django.shortcuts import render, render_to_response, redirect
from models import Article, Comments
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from forms import CommentForm
from django.core.context_processors import csrf
from django.contrib import auth

def articles(request):
    return render_to_response('articles.html', {'articles':Article.objects.all(), 'username':auth.get_user(request)})

def article(request, article_id=1):
    comment_form=CommentForm
    args={}
    args.update(csrf(request))
    args['article']=Article.objects.get(id=article_id)
    args['comment']=Comments.objects.filter(comments_article_id=article_id)
    args['form']=comment_form
    args['username']=auth.get_user(request).username

    return render_to_response('article.html', args)

def addlike(request, article_id):
    try:
        if article_id in request.COOKIES:
            redirect('/')
        else:
            article=Article.objects.get(id=article_id)
            article.article_likes+=1
            article.save()
            response=redirect('/')
            response.set_cookie(article_id,"test")
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')

def addcomment(request, article_id):
    if request.POST:
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.comments_article=Article.objects.get(id=article_id)
            form.save()
    return redirect('/articles/get/%s'%article_id)