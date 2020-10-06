from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, CustomUserCreationForm
from accounts.serializers import ProjectSerializer
from accounts.utils import LoginErrorList
from django.contrib.auth import logout, login
import xlrd
from accounts.models import (
    get_shot_by_name,
    get_project_by_name,
    get_sequence_by_name,
    Project,
    Sequence,
    Shot,
    Task,
)

excel_var = {"Sheet1": "link", "Sheet2": "sequence", "Sheet3": "project"}
# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("loginsimple")


@login_required(login_url="/account/loginsimple/")
def index(request):
    form = PasswordResetForm()
    return render(request, "index.html", {"form": form})


def Login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user.usertype)
            login(request, user)
            print("hereaftervalid")
            return redirect("index1")  # user is redirected to dashboard
        else:
            print(form.errors)
    else:
        form = UserLoginForm(error_class=LoginErrorList)
        print("here")
    return render(request, "login.html", {"form": form,})


def loginsimple(request):
    print("here")
    print(request)
    if request.method == "POST":
        print("hereafterpost")
        form = AuthenticationForm(
            request=request, data=request.POST, error_class=LoginErrorList
        )
        print("hereafterform")

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("hereaftervalid")
            return redirect("index1")  # user is redirected to dashboard
        else:
            print(form.errors)
            print("hereafternotvalid")
    else:
        form = AuthenticationForm(error_class=LoginErrorList)
        print("hereafternotpost")
    return render(request, "index.html", {"form": form,})


def dashboardIT(request):
    if request.method == "POST":
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usertype = UserType.objects.get(type=form.cleaned_data["usercriteria"])
            user = User(
                email=form.cleaned_data["email"],
                usertype=usertype,
                username=form.cleaned_data["username"],
            )
            user.set_password(form.clean_password2())
            user.save()
        return HttpResponse("data was recieved successfully")
    else:
        form = CustomUserCreationForm()

    return render(request, "index.html", {"form": form,})


def formupload(request):
    if request.method == "POST":
        input_excel = request.FILES["input_excel"]
        book = xlrd.open_workbook(file_contents=input_excel.read())
        print(book._sheet_names)
        for sheet in reversed(book.sheets()):
            headers = sheet.row_values(0)
            for i in range(1, sheet.nrows):
                keyArgs = {}
                row_list = sheet.row_values(i)
                for ind in range(len(row_list)):

                    if sheet.name in excel_var and (
                        headers[ind] == excel_var[sheet.name]
                    ):
                        if sheet.name == "Sheet3":
                            project = get_project_by_name(row_list[ind])
                            keyArgs[headers[ind]] = project
                            print("new project %s:%s" % (headers[ind], row_list[ind]))
                        if sheet.name == "Sheet2":
                            sequence = get_sequence_by_name(row_list[ind])
                            keyArgs[headers[ind]] = sequence
                            print("new Sequence %s:%s" % (headers[ind], row_list[ind]))
                        if sheet.name == "Sheet1":
                            link = get_shot_by_name(row_list[ind])
                            keyArgs[headers[ind]] = link
                            print("new Link %s:%s" % (headers[ind], row_list[ind]))
                    else:
                        if sheet.cell(i, ind).ctype == xlrd.XL_CELL_DATE:
                            exc_date = date(
                                xlrd.xldate_as_tuple(row_list[ind], book.datemode)[0],
                                xlrd.xldate_as_tuple(row_list[ind], book.datemode)[1],
                                xlrd.xldate_as_tuple(row_list[ind], book.datemode)[2],
                            )

                            keyArgs[headers[ind]] = exc_date
                            print(
                                "%s....%s.....%s"
                                % (headers[ind], book.datemode, exc_date)
                            )
                        else:
                            keyArgs[headers[ind]] = row_list[ind]
                            print("%s:%s" % (headers[ind], row_list[ind]))
                if sheet.name == "Sheet4":
                    Project.objects.create(**keyArgs)
                if sheet.name == "Sheet3":
                    Sequence.objects.create(**keyArgs)
                if sheet.name == "Sheet2":
                    Shot.objects.create(**keyArgs)
                if sheet.name == "Sheet1":
                    Task.objects.create(**keyArgs)
        return HttpResponse("completed")

    return render(request, "upload.html")


def getdata(request):
    if request.method == "POST":
        print(request)
        return JsonResponse({"result": "success"})

    data = ProjectSerializer(Project.objects.all(), many=True).data

    return JsonResponse(data, safe=False)
