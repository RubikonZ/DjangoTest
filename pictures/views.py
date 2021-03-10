from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from pictures.forms import CreateForm
from pictures.models import Picture
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.

class PicturesListView(View):
    model = Picture
    template_name = 'pictures/picture_list.html'

    def get(self, request):
        # https://www.pythonanywhere.com/user/Rubikon/files/home/Rubikon/django_projects/mysite/ads/templates/ads/ad_list.html?edit
        objects = Picture.objects.all().order_by('-created_at')
        ctx = {'picture_list': objects}
        return render(request, self.template_name, ctx)


class PictureDetailView(View):
    model = Picture
    template_name = 'pictures/picture_detail.html'

    def get(self, request, pk):
        x = Picture.objects.get(id=pk)
        context = {'picture': x}
        return render(request, self.template_name, context)


class PictureCreateView(View):
    template_name = 'pictures/picture_create.html'
    success_url = reverse_lazy('pictures:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # form.save(commit=False)
        picture = form.save(commit=False)
        # Need to add filename info into picture
        for filename in request.FILES:
            picture.file_name = request.FILES[filename]
        picture.save()
        return redirect(self.success_url)


class PictureUpdateView(View):
    template_name = 'pictures/picture_create.html'
    success_url = reverse_lazy('pictures:all')

    def get(self, request, pk):
        picture = get_object_or_404(Picture, id=pk)
        form = CreateForm(instance=picture)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        picture = get_object_or_404(Picture, id=pk)
        form = CreateForm(request.POST, request.FILES or None, instance=picture)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)