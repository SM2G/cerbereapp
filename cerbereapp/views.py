from django.http import HttpResponse, request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from .models import *
from .forms import *

from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

def clean_content(self):
    content = self.cleaned_data['content']
    content_type = content.content_type.split('/')[0]
    if content_type in settings.CONTENT_TYPES:
        if content._size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
    else:
        raise forms.ValidationError(_('File type is not supported'))
    return content


## Index
## #############################################################################
def index(request):
    return render(request, "index.html")


## Account
## #############################################################################
@login_required
def account(request):
    account_name = AccountType.objects.get(user_id = request.user.id)
    ctx = {}
    ctx["page_title"] = 'Account'
    ctx["employee_counter"] = Employee.objects.all().filter(user_id=request.user).count
    ctx["username"] = request.user.username
    ctx["account_name"] = AccountType.objects.get(user_id = request.user.id)
    ctx["limit_employees"] = account_name.limit_employees
    ctx["message"] = messages.add_message(request, messages.INFO, 'Hello world.')
    return render(request, 'account.html', ctx)


## Dashboard
## #############################################################################
@login_required
def dashboard(request):
    ctx = {}
    ctx["employee_counter"] = Employee.objects.all().filter(user_id=request.user).count
    ctx["profile_counter"] = Profile.objects.all().filter(user_id=request.user).count
    ctx["documentmodel_counter"] = DocumentModel.objects.all().filter(user_id=request.user).count

    ctx["expired_counter"] = 0
    ctx["critical_counter"] = 0
    ctx["warning_counter"] = 0

    for employee in Employee.objects.all().filter(user_id=request.user):
        print('===== Checking ',employee,'...')
        for document in ActualDocument.objects.all().filter(employee=employee):
            document_status = document.get_document_status()
            if document_status == 'expired':
                ctx["expired_counter"] += 1
            if document_status == 'critical':
                ctx["critical_counter"] += 1
            if document_status == 'warning':
                ctx["warning_counter"] += 1

    ctx["username"] = request.user.username
    return render(request, 'dashboard.html', ctx)


## Document models
## #############################################################################
@login_required
def documentmodels_list(request, template_name='documentmodels_list.html'):
    logged_user=str(request.user.id)
    documentmodels = DocumentModel.objects.all().filter(user_id=request.user)
    for documentmodel in documentmodels:
        print(documentmodel)
        print(documentmodel.profile_set.all())
    ctx = {}
    ctx['documentmodels'] = documentmodels
    return render(request, template_name, ctx)


@login_required
def documentmodel_create(request, template_name='documentmodel_create.html'):
    logged_user=str(request.user.id)
    form = DocumentModelForm(request.POST or None)
    if form.is_valid():
        form.instance.user_id = request.user
        form.save()
        return redirect('documentmodels_list')
    ctx = {}
    ctx["form"] = form
    return render(request, template_name, ctx)


@login_required
def documentmodel_update(request, documentmodel_id, template_name='documentmodel_update.html'):
    documentmodel = get_object_or_404(DocumentModel, pk=documentmodel_id)
    form = DocumentModelForm(request.POST or None, instance=documentmodel)
    if form.is_valid():
        form.save()
        return redirect('documentmodels_list')
    ctx = {}
    ctx["form"] = form
    ctx["documentmodel"] = documentmodel
    return render(request, template_name, ctx)


@login_required
def documentmodel_delete(request, documentmodel_id):
    logged_user=str(request.user.id)
    trash = DocumentModel.objects.get(pk=documentmodel_id)
    trash.delete()
    ctx = {
        #'page_title': 'Document Models',
        'documentmodels': DocumentModel.objects.all().filter(user_id=request.user),
        'form': DocumentModelForm(request.POST)
    }
    return render(request, 'documentmodels_list.html', ctx)


## Profiles
## #############################################################################
@login_required
def profiles_list(request, template_name='profiles_list.html'):
    logged_user=str(request.user.id)
    profiles = Profile.objects.all().filter(user_id=request.user)
    ctx = {}
    ctx['profiles'] = profiles
    return render(request, template_name, ctx)


@login_required
def profile_create(request, template_name='profile_create.html'):
    logged_user=int(request.user.id)
    print('======= logged_user: ', logged_user)
    form = ProfileForm(request.POST or None, logged_user=logged_user)
    if form.is_valid():
        form.instance.user_id = request.user
        form.save()
        return redirect('profiles_list')
    ctx = {}
    ctx["form"] = form
    return render(request, template_name, ctx)


@login_required
def profile_update(request, pk, template_name='profile_update.html'):
    logged_user=str(request.user.id)
    profile = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(request.POST or None, logged_user=logged_user, instance=profile)
    if form.is_valid():
        form.save()
        # Loop on all employees
        for employee in profile.employee_set.all():
            print('=======',employee,'should have:')
            employee.check_employee()

        return redirect('profiles_list')
    return render(request, template_name, {'form':form})


@login_required
def profile_delete(request, profile_id):
    logged_user=str(request.user.id)
    trash = Profile.objects.get(pk=profile_id)
    trash.delete()
    ctx = {
        'logged_user': logged_user,
        'username': request.user.username,
        'profiles': Profile.objects.all().filter(user_id=request.user),
        'form': ProfileForm(request.POST, logged_user=logged_user, instance=trash)
    }
    return render(request, 'profiles_list.html', ctx)


## Employees
## #############################################################################
@login_required
def employees_list(request, template_name='employees_list.html'):
    logged_user = str(request.user.id)
    employees = Employee.objects.all().filter(user_id=request.user).order_by("-is_active")
    ctx = {}
    ctx['employees'] = employees
    ctx['employee_counter'] = Employee.objects.all().filter(user_id=request.user).count
    ctx['limit_employees'] =  AccountType.objects.get(user_id=request.user.id).limit_employees
    return render(request, template_name, ctx)


@login_required
def employee_create(request, template_name='employee_create.html'):
    logged_user = str(request.user.id)
    employee_counter = Employee.objects.all().filter(user_id=request.user).count
    limit_employees = AccountType.objects.get(user_id=request.user.id).limit_employees
    form = EmployeeForm(request.POST or None, logged_user=logged_user)
    if form.is_valid():
        form.instance.user_id = request.user
        print('======= Using profile', form.instance.profile_id.id)
        form.save()
        employee_id = form.instance
        print('======= Creating agent', form.data)
        for documentmodel in form.instance.profile_id.documentmodels_list.all():
            print('======= creating actual document', documentmodel,'...')
            new_document = ActualDocument(employee=employee_id, documentmodel=documentmodel)
            new_document.save()
        return redirect('employees_list')
    ctx = {}
    ctx["form"] = form
    ctx['employee_counter'] = employee_counter
    ctx['limit_employees'] =  limit_employees
    return render(request, template_name, ctx)


@login_required
def employee_update(request, employee_id, template_name='employee_update.html'):
    logged_user = str(request.user.id)
    employee = get_object_or_404(Employee, pk = employee_id)
    form = EmployeeForm(request.POST or None, logged_user = logged_user, instance = employee)
    print('======= Employee id', employee.id)
    actualdocument_list = ActualDocument.objects.all().filter(employee_id = employee.id)
    #print('======= actualdocument_list', actualdocument_list)

    actualdocuments = {}
    for actualdocument in actualdocument_list:
        k = get_object_or_404(ActualDocument, pk = actualdocument.id)
        #print('======= actualdocument.id', actualdocument.id)
        actualdocuments[k] = ActualDocumentForm(request.POST or None\
                                                , request.FILES or None\
                                                , logged_user = logged_user\
                                                , instance = k\
                                                , prefix=actualdocument.id)

    if form.is_valid():
        print('======= EMPLOYEE FORM:',form)
        form.save()
        employee.check_employee()
        return redirect('employees_list')

    endsave = len(actualdocuments.keys())
    for k, v in actualdocuments.items():
        if v.is_valid():
            print('======= SAVING FORM!!!', v)
            actualdocuments[k].save()
            #print('======= Remains to save ',endsave,'...')
            endsave -= 1
        if endsave == 0:
            return redirect('employees_list')

    ctx = {}
    ctx["employee"] = employee
    ctx["form"] = form
    ctx["actualdocuments"] = actualdocuments
    #print('======= DICT ', actualdocuments)
    return render(request, template_name, ctx)


@login_required
def employee_delete(request, employee_id):
    logged_user=str(request.user.id)
    employee = Employee.objects.get(pk=employee_id)
    ctx = {}
    ctx['employee_counter'] = Employee.objects.all().filter(user_id=request.user).count
    ctx['limit_employees'] =  AccountType.objects.get(user_id=request.user.id).limit_employees
    ctx['logged_user'] = logged_user
    ctx['username'] = request.user.username
    ctx['employees'] = Employee.objects.all().filter(user_id=request.user)
    employee_documents = ActualDocument.objects.filter(employee=employee.id).all()
    for employee_document in employee_documents:
        print('======= drop document', employee_document,'...')
        employee_document.delete()
    employee.delete()
    print('======= drop employee', employee)
    return render(request, 'employees_list.html', ctx)
