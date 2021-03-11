from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from pictures.forms import UploadImageForm, ResizeImageForm
from pictures.models import Picture
from django.http import HttpResponse
from django.http import FileResponse
from django.core.files.base import ContentFile
import requests
import re

# Create your views here.


class PicturesListView(View):
    model = Picture
    template_name = 'pictures/picture_list.html'

    def get(self, request):
        # https://www.pythonanywhere.com/user/Rubikon/files/home/Rubikon/django_projects/mysite/ads/templates/ads/ad_list.html?edit
        objects = Picture.objects.all()
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
        form = UploadImageForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = UploadImageForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = Picture()
        if request.FILES:
            pic.picture = form.cleaned_data['picture']
            for filename in request.FILES:
                pic.picture_name = request.FILES[filename]
                pic.content_type = request.FILES[filename].content_type
            print(pic.picture.url)
        else:
            url = form.cleaned_data['url']
            resp = requests.get(url, stream=True)
            if resp.status_code == 200:
                fname = ''
                if "Content-Disposition" in resp.headers.keys():
                    fname = re.findall('filename=(.+)', resp.headers["Content-Disposition"])[0]
                else:
                    fname = url.split("/")[-1]
                pic.picture = ContentFile(resp.content, name=fname)
                pic.picture_name = fname
                pic.content_type = resp.headers['Content-Type']
                with open(f'media/images/{fname}', 'wb') as f:
                    for chunk in resp.iter_content(1024):
                        f.write(chunk)
        pic.save()
        return redirect(self.success_url)
# https://pbs.twimg.com/media/EwFdp2eXMAID98e.jpg

class PictureUpdateView(View):
    template_name = 'pictures/picture_create.html'
    success_url = reverse_lazy('pictures:all')

    def get(self, request, pk):
        picture = get_object_or_404(Picture, id=pk)
        form = ResizeImageForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        picture = get_object_or_404(Picture, id=pk)
        form = ResizeImageForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)


def stream_file(request, pk):
    pic = get_object_or_404(Picture, id=pk)
    response = HttpResponse()
    # response = FileResponse(io.BytesIO(bytes(pic.picture)))
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
