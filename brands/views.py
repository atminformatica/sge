from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics

from django.shortcuts import render, redirect
from .forms import ProjetoForm, ParticipacaoFormSet

def criar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        formset = ParticipacaoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            projeto = form.save()
            participacoes = formset.save(commit=False)
            for p in participacoes:
                nome = p.pessoa.nome
                telefone = p.pessoa.telefone
                pessoa, _ = models.Pessoa.objects.get_or_create(nome=nome, telefone=telefone)
                p.pessoa = pessoa
                p.projeto = projeto
                p.save()
            return redirect('novo_projeto')
    else:
        form = ProjetoForm()
        formset = ParticipacaoFormSet()
    return render(request, 'projeto_form.html', {'form': form, 'formset': formset})


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10
    permission_required = 'brands.view_brand'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
            
        return queryset
    

class BrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Brand
    template_name = 'brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brands_list')
    permission_required = 'brands.add_brand'

class BrandDetailView(DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'
    permission_required = 'brands.view_brand'

class BrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Brand
    template_name = 'brand_update.html' 
    form_class = forms.BrandForm
    success_url = reverse_lazy('brands_list')
    permission_required = 'brands.change_brand'

class BrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html' 
    success_url = reverse_lazy('brands_list')
    permission_required = 'brands.delete_brand'

class BrandCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer

class BrandRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
