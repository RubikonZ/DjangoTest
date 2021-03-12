from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from pictures.forms import UploadImageForm, ResizeImageForm
from pictures.models import Picture
from django.http import HttpResponse
from django.core.files.base import ContentFile
import requests
import re
from PIL import Image, ImageOps
import io

# Create your views here.


class PicturesListView(View):
    model = Picture
    template_name = 'pictures/picture_list.html'

    def get(self, request):
        objects = Picture.objects.all()
        ctx = {'picture_list': objects}
        return render(request, self.template_name, ctx)


class PictureDetailView(View):
    model = Picture
    template_name = 'pictures/picture_detail.html'
    success_url = reverse_lazy('pictures:all')

    def get(self, request, pk):
        form = ResizeImageForm()
        pic = Picture.objects.get(id=pk)
        context = {'form': form, 'picture': pic}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        # Here we get resize form
        form = ResizeImageForm(request.POST)
        pic = Picture.objects.get(id=pk)

        if not form.is_valid():
            ctx = {'form': form, 'picture': pic}
            return render(request, self.template_name, ctx)

        image = Image.open(pic.parent_picture)
        image = image.convert('RGB') # Needed incase our picture has alpha/transparency
        if form.cleaned_data['width'] and not form.cleaned_data['height']:
            width = form.cleaned_data['width']
            height = image.height
        elif form.cleaned_data['height'] and not form.cleaned_data['width']:
            height = form.cleaned_data['height']
            width = image.width
        else:
            # The only issue is picture doesn't fit in this new given field
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']

        # Calculating ratio to resize image (works for both scale down and upper)
        if width < image.width or height < image.height:
            resize_ratio = min(width/image.width, height/image.height)
        elif width > image.width or height > image.height:
            resize_ratio = max(width/image.width, height/image.height)
        else:
            resize_ratio = 1

        new_width = int(image.width*resize_ratio)
        new_height = int(image.height*resize_ratio)
        img_copy = image.resize((new_width, new_height), Image.ANTIALIAS)
        img_fit = ImageOps.fit(img_copy, (1000, 1000), centering=(0.5, 0.5))
        filename, extension = pic.picture_name.split('.')
        # Turning edited picture into byte array
        byte_img = io.BytesIO()
        # img_copy.save(byte_img, format='JPEG')
        img_fit.save(byte_img, format='JPEG')
        byte_img = byte_img.getvalue()
        pic.picture = ContentFile(byte_img, name=f'resize/{filename}/{filename}_{new_width}x{new_height}.{extension}')
        pic.save()
        context = {'form': form, 'picture': pic}
        return render(request, self.template_name, context)


class PictureCreateView(View):
    template_name = 'pictures/picture_create.html'
    success_url = reverse_lazy('pictures:all')

    def get(self, request, pk=None):
        form = UploadImageForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        # Here we add new image to db
        form = UploadImageForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = Picture()
        if request.FILES:
            pic.parent_picture = form.cleaned_data['picture']
            pic.parent = form.cleaned_data['picture']
            for filename in request.FILES:
                pic.picture_name = request.FILES[filename]
                pic.content_type = request.FILES[filename].content_type
        else:
            url = form.cleaned_data['url']
            resp = requests.get(url, stream=True)
            if resp.status_code == 200:
                fname = ''
                if "Content-Disposition" in resp.headers.keys():
                    fname = re.findall('filename=(.+)', resp.headers["Content-Disposition"])[0]
                else:
                    fname = url.split("/")[-1]
                pic.parent_picture = ContentFile(resp.content, name=fname)
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
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
