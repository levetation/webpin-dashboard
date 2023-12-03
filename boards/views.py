from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Board, BoardBookmark
from boards import bookmark_functions

from UserProfile.models import UserProfileModel

import os

@login_required(login_url="/login_user")
def board_page(request, id):
    board = Board.objects.get(pk=id) # Get associated board
    profile = UserProfileModel.objects.get(account=board.author)
    boardbookmarks = BoardBookmark.objects.filter(board=id).order_by('-save_date') # Get bookmarks associated with selected board
    shortened_urls = [bookmark_functions.url_name(bookmark.address) for bookmark in boardbookmarks]
    bookmarks = zip(boardbookmarks, shortened_urls)
    context = {'board':board, 'boardbookmarks': boardbookmarks, 'bookmarks':bookmarks, 'profile':profile}

    # New bookmark
    if request.method == 'POST' and 'submit_new_bookmark' in request.POST:

        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']

        # set default bookmark title
        if new_bookmark_title == '': new_bookmark_title = bookmark_functions.url_name(request.POST['new_bookmark_address'])

        new_bookmark = BoardBookmark(
            title = new_bookmark_title,
            address = new_bookmark_address,
            note = new_bookmark_notes,
            board = Board.objects.get(pk=id),
        )

        new_bookmark.save()
        return redirect(request.META['HTTP_REFERER'])  

    # Deleting selected bookmarks    
    if request.method == 'POST' and 'delete_selected_bookmarks' in request.POST:
        bookmarks_to_delete = request.POST.getlist('bookmarks_checked_to_delete')
        for bookmark_id in bookmarks_to_delete:
            bookmark_to_delete = BoardBookmark.objects.get(pk=bookmark_id)
            bookmark_to_delete.delete()
        return redirect(request.META['HTTP_REFERER'])
    
    # Edit selected bookmark
    if request.method == 'POST' and 'edit_selected_bookmark' in request.POST:
        bookmark = BoardBookmark.objects.get(pk=request.POST.get('bookmark_id'))
        title = request.POST.get('new_bookmark_title')
        address = request.POST.get('new_bookmark_address')
        note = request.POST.get('new_bookmark_notes')

        bookmark.title = title
        bookmark.note = note
        bookmark.address = address
        
        bookmark.save()
        return redirect(request.META['HTTP_REFERER'])
    
    ## Private/Public board

    # Public
    if request.method == 'POST' and 'make_board_public' in request.POST:
        board = Board.objects.get(pk=id)
        board.public = True
        board.save()
        context['board_public'] = 'public'
        context['board_status'] = 'Public'
        return redirect(request.META['HTTP_REFERER'])
    
    # Private
    if request.method == 'POST' and 'make_board_private' in request.POST:
        board = Board.objects.get(pk=id)
        board.public = False
        board.save()
        context['board_private'] ='private'
        context['board_status'] = 'Private'
        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'boards/boardpage.html', context)

@login_required(login_url="/login_user")
def boards(request):
    boards = Board.objects.filter(author=request.user.id).order_by('-created_date')
    context = {'boards': boards}

    # New board
    if request.method == 'POST' and 'submit_new_board' in request.POST:
        board_title = request.POST['new_board_title']
        board_description = request.POST['new_board_description']
        if 'new_board_image' in request.FILES:
            board_image = request.FILES['new_board_image']
        else: 
            board_image = None
        new_board = Board(
            title = board_title,
            description = board_description,
            image = board_image,
            author = request.user,
            )
        new_board.save()
        return redirect('boards')
    
    # Edit board
    if request.method == 'POST' and 'edit_selected_board' in request.POST:
        board = Board.objects.get(pk=request.POST.get('board_id'))
        title = request.POST.get('new_board_title')
        description = request.POST.get('new_board_description')

        if 'new_board_image' in request.FILES:
            image = request.FILES.get('new_board_image')
        else:
            image = board.image
        
        board.title = title
        board.description = description
        board.image = image
        
        board.save()
        return redirect('boards')
    
    return render(request, 'boards/boards.html', context)

@login_required(login_url="/login_user")
def delete_board(request, id):
    board_to_delete = Board.objects.get(pk=id)
    # delete image before board
    image_path = board_to_delete.image.path
    if os.path.isfile(image_path):
        os.remove(image_path)
    board_to_delete.delete()
    return redirect('boards')