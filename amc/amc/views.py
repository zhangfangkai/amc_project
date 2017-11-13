# coding=utf8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def total_view(req):
    return HttpResponse("HELLO WORLD!")
