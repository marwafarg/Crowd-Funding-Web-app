from .models import *
import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectsForm, ImageForm
from django.http.response import HttpResponse, JsonResponse,HttpResponseForbidden
from .models import *
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.db.models import Q, Avg, Sum
# Create your views here.
from taggit.models import Tag
from decimal import Decimal, ROUND_HALF_UP
from django.template.loader import render_to_string
from datetime import datetime
from django.views.generic.list import ListView



def showProject(request, id):
    item = Project.objects.get(id=id)
    pPics = ProjectPicture.objects.all().filter(project_id=id)
    relatedProjects = Project.objects.all().filter(category_id=item.category)
    rate = item.rate_set.all().aggregate(Avg("value"))["value__avg"]
    rate = rate if rate else 0
    rate = Decimal(rate).quantize(0, ROUND_HALF_UP)
    today = datetime.now()
    start_date = item.start_date
    end_date = item.end_date
    myFormat = "%Y-%m-%d %H:%M:%S"
    today = today.strftime(myFormat)
    today = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
    start_date = start_date.strftime(myFormat)
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date = end_date.strftime(myFormat)
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    donate = item.donation_set.all().aggregate(Sum("amount"))
    context = {'pData': item,
               'pPics': pPics,
               'rate': rate,
               'today': today,
               'start_date': start_date,
               'end_date': end_date,
               'relatedProjs': relatedProjects,
               'donations_amount': donate["amount__sum"] if donate["amount__sum"] else 0}

    return render(request, "projects/viewProject.html", context)

def showCategoryProjects(request,name):
    category = Category.objects.get(name=name)
    context = {'catName': category}
    return render(request, "projects/viewCategory.html", context)


def create(request):

    ImageFormSet = modelformset_factory(
        ProjectPicture, form=ImageForm, min_num=1, extra=3)

    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=ProjectPicture.objects.none())

        if form.is_valid() and formset.is_valid():
            new_form = form.save(commit=False)
            # new_form.user = User.objects.get(user=request.user)
            new_form.save()
            form.save_m2m()
            for form in formset.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['img_url']
                    photo = ProjectPicture(project=new_form, img_url=image)
                    photo.save()
            return redirect(f'/projects/projectDetails/{new_form.id}')
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'projects/create.html', context)
    else:

        form = ProjectsForm()
        formset = ImageFormSet(queryset=ProjectPicture.objects.none())
        context = {
            'form': form,
            'formset': formset,
        }
    return render(request, 'projects/create.html', context)


def create_comment(request, id):
    if request.method == 'POST':
        if request.POST['content']:
            comment = Comment()
            comment.content = request.POST['content']
            comment.project_id = id

            comment.save()
        return redirect(f'/projects/projectDetails/{id}')



# class show(ListView):
#     model = Project
#     template_name = 'projects/show.html'
def list_categories(request):
    categories = Category.objects.all()
    return {
        'categs': categories
    }



def home(request):
    projectRates = Rate.objects.all().values('project').annotate(
        Avg('value')).order_by('-value__avg')[:5]
    print(projectRates)

    hRatedProjects = []
    for p in projectRates:
        print(p.get('project'))
        hRatedProjects.extend(
            list(Project.objects.filter(id=p.get('project'))))
        print(hRatedProjects)

    lFiveList = Project.objects.extra(order_by=['-created_at'])
    featuredList = Project.objects.all().filter(is_featured='True')
    context = {
        'latestFiveList': lFiveList,
        'fProject': featuredList,
        'hRProjects': hRatedProjects,
    }

    return render(request, 'projects/Home.html', context)


def show_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    projects = Project.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'projects': projects,
    }
    return render(request, 'projects/tag.html', context)


def report_project(request, id):
    if request.method == 'POST':
        report_pro = ProjectReport.objects.create(
            content=request.POST['report'],
            project_id=id,

        )

        return redirect(f'/projects/projectDetails/{id}')


def report_comment(request, id):
    if request.method == 'POST':
        if len(list(CommentReport.objects.filter(comment_id=request.POST['comment_id']))) == 0:
            report_com = CommentReport.objects.create(

                comment_id=request.POST['comment_id'],
            )
        else:
            messages.error(request, 'You reported this comment before!')
        return redirect(f'/projects/projectDetails/{id}')


def search(request):
    inp = request.GET.get('searchBox')
    if inp:
        project = Project.objects.filter(Q(title__icontains=inp))[:1]
    else:
        inp = ' '
    return showProject(request, project)


def rate_project(request, id, value):
    if request.method == 'POST':
        print(f"{id} {value}")

        Rate.objects.update_or_create(
            project_id=id,
            defaults={"value": value},
        )
        data = {
            'msg': "success"
        }
        return JsonResponse(data)


def donate(request, id):
    if request.method == 'POST':
        donate = Donation.objects.create(
            amount=request.POST['donate'],
            project_id=id,
        )
        return redirect(f'/projects/projectDetails/{id}')

def delete_project(request, id):
    if request.method == 'POST':
        project = get_object_or_404(Project,id=id)

        project.delete()
        return redirect(f'profile/')