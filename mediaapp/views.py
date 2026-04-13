from django.shortcuts import redirect, render

from mediaapp.forms import MediafileForm
from .models import Mediafile   

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = MediafileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'mediaapp/upload_success.html')
    form = MediafileForm()
    return render(request, 'mediaapp/upload.html', {'form': form})

def file_list(request):
    files = Mediafile.objects.all()
    return render(request, 'mediaapp/file_list.html', {'files': files})


def file_delete(request, pk):
    file = Mediafile.objects.get(pk=pk)
    file.file.delete()  # Delete the file from storage
    file.delete()

    return redirect('mediaapp:file_list')