from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Board, BoardBookmark

@login_required(login_url="/login_user")
def board_page(request, id):
    board = Board.objects.get(pk=id) # Get associated board
    boardbookmarks = BoardBookmark.objects.filter(board=id).order_by('-save_date') # Get bookmarks associated with selected board
    context = {'board':board, 'boardbookmarks': boardbookmarks}
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
    board_to_delete.delete()
    return redirect('boards')