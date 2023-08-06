from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .bookmark_functions import url_name 

from .models import Bookmark



@login_required(login_url="/login_user")
def bookmark_gallery(request):
    context = {}
    bookmarks = Bookmark.objects.filter(author=request.user.id).order_by('-save_date')
    context['bookmarks'] = bookmarks

    # New bookmark
    if request.method == 'POST' and 'submit_new_bookmark' in request.POST:

        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']
        new_bookmark_category = request.POST['new_bookmark_category']

        # set default bookmark title
        if new_bookmark_title == '': new_bookmark_title = url_name(request.POST['new_bookmark_address'])

        new_bookmark = Bookmark(
            title = new_bookmark_title,
            address = new_bookmark_address,
            notes = new_bookmark_notes,
            category = new_bookmark_category,
            author = request.user,
        )

        new_bookmark.save()
        return redirect('bookmark_gallery')  
    
    # Quick add url
    if request.method == 'POST' and 'quickaddurl' in request.POST:
        quick_url = request.POST['quickaddurl']
        if len(quick_url) > 0: # catches empty submissions
            default_title = url_name(request.POST['quickaddurl'])
            new_bookmark = Bookmark(
                title = default_title,
                address = quick_url,
                notes = None,
                category = None,
                author = request.user,
            )
            new_bookmark.save()
            return redirect('bookmark_gallery')
    
    # Catagories
    bookmark_list = [bookmark for bookmark in bookmarks]
    catagories = list(set([entry.category for entry in bookmark_list if entry.category != '']))
    if request.method =='POST' and 'select_category' in request.POST:
        if request.POST['selected_bookmark_category'] == 'View all':
            redirect('bookmark_gallery')
        else:
            bookmarks = Bookmark.objects.filter(
                category=request.POST['selected_bookmark_category'],
                author=request.user.id
            ).order_by('-save_date')

            context['bookmarks'] = bookmarks
            return render(request, 'bookmarks/bookmark_gallery.html', context)  
    
    # Sort by
    if request.method == 'POST' and 'sort' in request.POST:
        if request.POST['sort'] == 'Oldest':
            bookmarks = Bookmark.objects.filter(author=request.user.id).order_by('save_date')
        else:
            return redirect('bookmark_gallery')
        context = {'bookmarks': bookmarks, 'sortby': request.POST['sort']}
        return render(request, 'bookmarks/bookmark_gallery.html', context)

    # Edit bookmark
    if request.method == 'POST' and 'edit_selected_bookmark' in request.POST:
        bookmark = Bookmark.objects.get(pk=request.POST.get('bookmark_id'))
        new_title = request.POST.get('new_bookmark_title')
        new_address = request.POST.get('new_bookmark_address')
        new_notes = request.POST.get('new_bookmark_notes')
        new_category = request.POST.get('new_bookmark_category')
        
        bookmark.title = new_title
        bookmark.address = new_address
        bookmark.notes = new_notes
        bookmark.category = new_category
        
        bookmark.save()
        return redirect('bookmark_gallery')

    
    context['catagories'] = catagories
    return render(request, 'bookmarks/bookmark_gallery.html', context)

@login_required(login_url="/login_user")
def delete_bookmark(request, id):
    bookmark_to_delete = Bookmark.objects.get(pk=id)
    bookmark_to_delete.delete()
    return redirect('bookmark_gallery')

@login_required(login_url="/login_user")
def edit_bookmark(request, id):
    
    bookmark = Bookmark.objects.get(pk=id)
    
    if request.method == 'POST':
        new_title = request.POST.get('new_bookmark_title')
        new_address = request.POST.get('new_bookmark_address')
        new_notes = request.POST.get('new_bookmark_notes')
        new_category = request.POST.get('new_bookmark_category')
        
        bookmark.title = new_title
        bookmark.address = new_address
        bookmark.notes = new_notes
        bookmark.category = new_category
        
        bookmark.save()
        return redirect('bookmark_gallery')
    else:
        return redirect('bookmark_gallery')