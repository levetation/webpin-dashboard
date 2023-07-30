from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'dashboardhome/index.html', context={})

def sample(request):
    return render(request, 'dashboardhome/sample.html', context={})

def alerts(request):
    return render(request, 'dashboardhome/ui-alerts.html', context={})

def buttons(request):
    return render(request, 'dashboardhome/ui-buttons.html', context={})

def cards(request):
    return render(request, 'dashboardhome/ui-card.html', context={})

def forms(request):
    return render(request, 'dashboardhome/ui-forms.html', context={})

def typography(request):
    return render(request, 'dashboardhome/ui-typography.html', context={})