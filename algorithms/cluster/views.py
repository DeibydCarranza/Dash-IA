from django.shortcuts import render

# Create your views here.
def cluster_algorithm(request):
    return render(request, 'cluster.html')