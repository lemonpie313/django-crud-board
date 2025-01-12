from django.shortcuts import render, redirect, reverse
from .models import Board

def index(request):
    return render(request, 'board/index.html')

def list(request):
    board_list = Board.objects.all().order_by('-id')
    context = {
        'board_list':board_list,
    }
    return render(
        request,
        'board/list.html',
        context
    )
    
def read(request, id):
    board = Board.objects.get(pk=id)
    board.incrementReadCount()
    return render(request, 'board/read.html', {'board':board})

def regist(request):
    if request.method == 'POST': # post형식이면 데이터 저장 후 list 보여줌줌
        title = request.POST['title'] # title 키 값이 없으면 에러
        writer = request.POST.get('writer') # writer 키 값이 없으면 None
        content = request.POST['content'] # content 키 값이 없으면 에러
        Board(title=title, writer=writer, content=content).save()
        return redirect(reverse('board:list'))
    else:
        return render(request, 'board/regist.html') #post가 아니면 게시글 등록 양식 보여줌
    
def edit(request, id):
    board = Board.objects.get(pk=id)
    if request.method == 'POST': # post형식이면 데이터 저장 후 list 보여줌줌
        board.title = request.POST['title'] # title 키 값이 없으면 에러
        board.writer = request.POST.get('writer', 'default') # writer 키 값이 없으면 None
        board.content = request.POST['content'] # content 키 값이 없으면 에러
        board.save()
        return redirect(reverse('board:read', args=(id,)))
    else:
        return render(request, 'board/edit.html', {'board':board}) #post가 아니면 게시글 등록 양식 보여줌
    
def remove(request, id):
    board = Board.objects.get(pk=id)
    if request.method == 'POST':
        board.delete()
        return redirect(reverse('board:list'))
    else:
        return render(request, 'board/remove.html',{'board':board})