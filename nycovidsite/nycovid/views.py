from . import nymap
from . import utils


dl = DataLoader()
dfs = dl.fetch_virus_data()
ny = NYMap()
l = ny.feature_by_zip(dl.df_zip, feature="weighted_positivity")

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse(l)