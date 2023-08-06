from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import subprocess
import os

from .forms.xls_diff_form import XlsDiffForm


# Create your views here.
def index(request):
    context = {}

    form = XlsDiffForm()
    context["form"] = form

    return render(request, "xls_diffs_and_intersection/index.html", context)


def compute(request):
    context = {}

    if request.method == "POST":
        form = XlsDiffForm(request.POST, request.FILES)
        if form.is_valid():
            old_file_contents = form.cleaned_data["old_file"].read().decode()
            new_file_contents = form.cleaned_data["new_file"].read().decode()

            with open("xls_diffs_and_intersection/tmp/old_file.csv", "w", encoding="utf-8") as old_file_handle:
                old_file_handle.write(old_file_contents)
            with open("xls_diffs_and_intersection/tmp/new_file.csv", "w", encoding="utf-8") as new_file_handle:
                new_file_handle.write(new_file_contents)

            os.system("rm -rf xls_diffs_and_intersection/tmp/differences-intersection_*")
            output = subprocess.check_output(["python3", "xls_diffs_and_intersection/utilities/diff_and_intersection.py", "xls_diffs_and_intersection/tmp/old_file.csv", "xls_diffs_and_intersection/tmp/new_file.csv"]).decode().strip()
            os.system("rm xls_diffs_and_intersection/tmp/old_file.csv")
            os.system("rm xls_diffs_and_intersection/tmp/new_file.csv")

        filename = output.split("/")[-1]

        response = HttpResponse(open(output, "rb").read())
        response["Content-Type"] = "application/x-zip-compressed"
        response["Content-Disposition"] = f"attachment; filename={filename}"

        return response
    else:
        return render(request, "xls_diffs_and_intersection/index.html", context)
