from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Board

@login_required(login_url="/login_user")
def boards(request):
    boards = Board.objects.filter(author=request.user.id).order_by('-created_date')
    context = {'boards': boards}
    return render(request, 'boards/boards.html', context)

def delete_board(request):
    return None