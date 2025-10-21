from django.shortcuts import render, redirect
from .models import Boletim, BoletimEnvolvimento, Envolvido
from .forms import BoletimForm, BoletimEnvolvimentoForm, BoletimEnvolvimentoFormSet
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.views import View

# usado pra pegar caminho da pasta static pra usar no pdf
from django.shortcuts import render
from django.contrib.staticfiles import finders

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class BulletinListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Boletim
    template_name = 'bulletin_list.html'
    context_object_name = 'bulletins'
    paginate_by = 10
    permission_required = 'bulletins.view_boletim'

    def get_queryset(self):
        queryset = super().get_queryset()
        filtro_nome_envolvido = self.request.GET.get('filtro_nome_envolvido')
        filtro_endereco_envolvido = self.request.GET.get('filtro_endereco_envolvido')
        filtro_numero_bi = self.request.GET.get('filtro_numero_bi')
        filtro_endereco_bo = self.request.GET.get('filtro_endereco_bo')
        filtro_bairro_bo = self.request.GET.get('filtro_bairro_bo')
        filtro_secao = self.request.GET.get('filtro_secao')
        filtro_cpf = self.request.GET.get('filtro_cpf')
        filtro_nome_relator = self.request.GET.get('filtro_nome_relator')
        filtro_documento_relator = self.request.GET.get('filtro_documento_relator')
        filtro_destinatario = self.request.GET.get('filtro_destinatario')

        if filtro_numero_bi:
            queryset = queryset.filter(numero_bi__icontains=filtro_numero_bi)

        if filtro_nome_envolvido:
            queryset = queryset.filter(boletimenvolvimento__envolvido__nome__icontains=filtro_nome_envolvido)
              
        if filtro_endereco_envolvido:
            queryset = queryset.filter(boletimenvolvimento__envolvido__endereco__icontains=filtro_endereco_envolvido)

        if filtro_endereco_bo:
            queryset = queryset.filter(endereco_dofato__icontains=filtro_endereco_bo)
        
        if filtro_bairro_bo:
            queryset = queryset.filter(bairro_dofato__icontains=filtro_bairro_bo)
        
        if filtro_secao:
            queryset = queryset.filter(secao__icontains=filtro_secao)

        if filtro_cpf:
            filtro_cpf=filtro_cpf.strip().replace('.', '').replace('-', '')
            queryset = queryset.filter(boletimenvolvimento__envolvido__cpf__icontains=filtro_cpf)
             
        if filtro_nome_relator:
            queryset = queryset.filter(relatornome__icontains=filtro_nome_relator)
       
        if filtro_documento_relator:
            queryset = queryset.filter(relatordocumento__icontains=filtro_documento_relator)
        
        if filtro_destinatario:
            queryset = queryset.filter(destinatario__icontains=filtro_destinatario)

        return queryset

class BulletinDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Boletim
    template_name = 'bulletin_delete.html' 
    success_url = reverse_lazy('bulletin_list')
    permission_required = 'bulletins.delete_boletim'

class BulletinDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Boletim
    context_object_name = 'bulletin'
    template_name = 'bulletin_detail.html'
    permission_required = 'bulletins.view_boletim'

    def get_queryset(self):
        # Otimiza a busca para carregar os envolvidos e o envolvimento de uma só vez
        return super().get_queryset().prefetch_related('boletimenvolvimento_set__envolvido')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O objeto do boletim já tem os envolvidos carregados
        context['envolvimentos'] = self.object.boletimenvolvimento_set.all()
        return context
   
class BulletinUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Boletim
    form_class = BoletimForm
    template_name = 'bulletin_update.html'
    context_object_name = 'bulletin'
    permission_required = 'bulletins.change_boletim'

    # def get_queryset(self):
    #     # Otimiza a busca para carregar os envolvidos e o envolvimento de uma só vez
    #     return super().get_queryset().prefetch_related('boletimenvolvimento_set__envolvido')

    def get_success_url(self):
        return reverse_lazy('bulletin_list')
        # return reverse_lazy('bulletin_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            print('post')
            context['envolvimentos'] = BoletimEnvolvimentoFormSet(self.request.POST, instance=self.object)
            print('post post')
        else:
            context['envolvimentos'] = BoletimEnvolvimentoFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        envolvimento_formset = context['envolvimentos']
        if form.is_valid() and envolvimento_formset.is_valid():
            self.object = form.save()

            envolvimentos = envolvimento_formset.save(commit=True)
            for envolvimento in envolvimentos:
                if envolvimento is not None:
                    # Atualiza/Salva o envolvido explicitamente ANTES
                    if envolvimento.envolvido:
                        envolvido = envolvimento.envolvido
                        # Atualize os campos do envolvido com os dados do formulário
                        form_for_envolvido = next(
                            (f for f in envolvimento_formset.forms if f.instance == envolvimento), None
                        )
                        if form_for_envolvido:
                            # Campos do envolvido no form customizado são 'envolvido_nome', etc
                            envolvido.nome = form_for_envolvido.cleaned_data.get('envolvido_nome', envolvido.nome)
                            envolvido.naturalidade = form_for_envolvido.cleaned_data.get('envolvido_naturalidade', envolvido.naturalidade)
                            envolvido.datanascimento = form_for_envolvido.cleaned_data.get('envolvido_datanascimento', envolvido.datanascimento)
                            envolvido.endereco = form_for_envolvido.cleaned_data.get('envolvido_endereco', envolvido.endereco)
                            envolvido.numero = form_for_envolvido.cleaned_data.get('envolvido_numero', envolvido.numero)
                            envolvido.bairro = form_for_envolvido.cleaned_data.get('envolvido_bairro', envolvido.bairro)
                            envolvido.cidade = form_for_envolvido.cleaned_data.get('envolvido_cidade', envolvido.cidade)
                            envolvido.uf = form_for_envolvido.cleaned_data.get('envolvido_uf', envolvido.uf)
                            envolvido.cep = form_for_envolvido.cleaned_data.get('envolvido_cep', envolvido.cep)
                            envolvido.telefone = form_for_envolvido.cleaned_data.get('envolvido_telefone', envolvido.telefone)
                            envolvido.estadocivil = form_for_envolvido.cleaned_data.get('envolvido_estadocivil', envolvido.estadocivil)
                            envolvido.cpf = form_for_envolvido.cleaned_data.get('envolvido_cpf', envolvido.cpf)
                            envolvido.identidade = form_for_envolvido.cleaned_data.get('envolvido_identidade', envolvido.identidade)
                            envolvido.profissao = form_for_envolvido.cleaned_data.get('envolvido_profissao', envolvido.profissao)
                            envolvido.email = form_for_envolvido.cleaned_data.get('envolvido_email', envolvido.email)
                            envolvido.escolaridade = form_for_envolvido.cleaned_data.get('envolvido_escolaridade', envolvido.escolaridade)
                            envolvido.save()

                    # Define a relação com o boletim e salva o BoletimEnvolvimento
                    envolvimento.boletim = self.object
                    envolvimento.save()

            # Deleta os marcados para exclusão
            for obj in envolvimento_formset.deleted_objects:
                obj.delete()

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def form_valid_old(self, form):
        print('ooooooooooooooooooooooooooooooooooooooo')
        context = self.get_context_data()
        envolvimento_formset = context['envolvimentos']
        if form.is_valid():
            if envolvimento_formset.is_valid():
                # Salva o boletim
                print('envolvimento_formset esta valido')
                self.object = form.save()            
                # Salva os envolvidos
                envolvimentos = envolvimento_formset.save(commit=False)
                for envolvimento in envolvimentos:
                    if envolvimento is not None:
                        envolvimento.boletim = self.object
                        envolvimento.save()
               
                # Não chame save_m2m aqui, pois não há campos ManyToMany
                # envolvimento_formset.save_m2m()
                # Salva os objetos marcados para exclusão, se houver
                for obj in envolvimento_formset.deleted_objects:
                    obj.delete()

                return redirect(self.get_success_url())
            else:
                # Em caso de erro, adicione os formulários (agora com erros) ao contexto
                # e renderize o template novamente
                #print("Erros do formulário Boletim:", self.object.errors)
                # print("Erros não específicos do formset:", envolvimento_formset.non_form_errors())
                print('algum erro aconteceu nos envolvidos++++++++++++++++++')    
                print("Erros do formset de Envolvimento:", envolvimento_formset.errors)
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return self.render_to_response(self.get_context_data(form=form))
   
class BulletinCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Boletim
    form_class = BoletimForm
    template_name = 'bulletin_create2.html'
    context_object_name = 'bulletin'
    permission_required = 'bulletins.change_boletim'

    def get_success_url(self):
        return reverse_lazy('bulletin_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['envolvimentos'] = BoletimEnvolvimentoFormSet(self.request.POST)
        else:
            context['envolvimentos'] = BoletimEnvolvimentoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        envolvimento_formset = context['envolvimentos']
        if form.is_valid() and envolvimento_formset.is_valid():
            self.object = form.save()
            print('boletim foi salvo agora ,,,,,,,,,,,,,,')
            envolvimentos = envolvimento_formset.save(commit=False)
            print('boletim foi salvo agora ,,,,,,,,,,,,,*********,')
            for envolvimento in envolvimentos:
                if envolvimento is not None:
                    if envolvimento.envolvido:
                        envolvido = envolvimento.envolvido
                        form_for_envolvido = next(
                            (f for f in envolvimento_formset.forms if f.instance == envolvimento), None
                        )
                        if form_for_envolvido:
                            envolvido.nome = form_for_envolvido.cleaned_data.get('envolvido_nome', envolvido.nome)
                            envolvido.naturalidade = form_for_envolvido.cleaned_data.get('envolvido_naturalidade', envolvido.naturalidade)
                            envolvido.datanascimento = form_for_envolvido.cleaned_data.get('envolvido_datanascimento', envolvido.datanascimento)
                            envolvido.endereco = form_for_envolvido.cleaned_data.get('envolvido_endereco', envolvido.endereco)
                            envolvido.numero = form_for_envolvido.cleaned_data.get('envolvido_numero', envolvido.numero)
                            envolvido.bairro = form_for_envolvido.cleaned_data.get('envolvido_bairro', envolvido.bairro)
                            envolvido.cidade = form_for_envolvido.cleaned_data.get('envolvido_cidade', envolvido.cidade)
                            envolvido.uf = form_for_envolvido.cleaned_data.get('envolvido_uf', envolvido.uf)
                            envolvido.cep = form_for_envolvido.cleaned_data.get('envolvido_cep', envolvido.cep)
                            envolvido.telefone = form_for_envolvido.cleaned_data.get('envolvido_telefone', envolvido.telefone)
                            envolvido.estadocivil = form_for_envolvido.cleaned_data.get('envolvido_estadocivil', envolvido.estadocivil)
                            envolvido.cpf = form_for_envolvido.cleaned_data.get('envolvido_cpf', envolvido.cpf)
                            envolvido.identidade = form_for_envolvido.cleaned_data.get('envolvido_identidade', envolvido.identidade)
                            envolvido.profissao = form_for_envolvido.cleaned_data.get('envolvido_profissao', envolvido.profissao)
                            envolvido.email = form_for_envolvido.cleaned_data.get('envolvido_email', envolvido.email)
                            envolvido.escolaridade = form_for_envolvido.cleaned_data.get('envolvido_escolaridade', envolvido.escolaridade)
                            envolvido.save()

                    envolvimento.boletim = self.object
                    envolvimento.save()

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# buscarcpf aceita apenas post por seguranca pois get envia o cpf na url
@require_POST 
@login_required
def buscar_envolvido_por_cpf(request):
    cpf = request.POST.get('cpf', '').strip().replace('.', '').replace('-', '')

    if not cpf.isdigit() or len(cpf) != 11:
        return JsonResponse({'error': 'CPF inválido'}, status=400)

    envolvido = Envolvido.objects.filter(cpf=cpf).first()
    if not envolvido:
        return JsonResponse({'error': 'Envolvido não encontrado'}, status=404)

    # Retorne só os campos que você precisa preencher
    data = {
        'nome': envolvido.nome,
        'naturalidade': envolvido.naturalidade,
        'datanascimento': envolvido.datanascimento.strftime('%Y-%m-%d') if envolvido.datanascimento else '',
        'endereco': envolvido.endereco,
        'numero': envolvido.numero,
        'bairro': envolvido.bairro,
        'cidade': envolvido.cidade,
        'uf': envolvido.uf,
        'cep': envolvido.cep,
        'telefone': envolvido.telefone,
        'estadocivil': envolvido.estadocivil,
        'identidade': envolvido.identidade,
        'profissao': envolvido.profissao,
        'email': envolvido.email,
        'escolaridade': envolvido.escolaridade,
    }

    return JsonResponse(data)

class BulletinPDFView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'bulletins.view_boletim'

    def get(self, request, pk):
        bulletin = Boletim.objects.prefetch_related('boletimenvolvimento_set__envolvido').get(pk=pk)
        template_path = 'bulletin_pdf.html'
        #caminhologolocal = caminho fisico da pasta static no servidor local pra usar no pdf usando xhtml2pdf
        caminhologolocal = finders.find('images/brasao.png')
        envolvimentos = bulletin.boletimenvolvimento_set.all()
        print(bulletin.historico)
        
        total_envolvimentos = envolvimentos.count()
        array_envolvidosvazios = []
        if total_envolvimentos < 5:
            for i in range(total_envolvimentos + 1, 6):
                array_envolvidosvazios.append(i)

        conteudo_historico = bulletin.historico
        if conteudo_historico:
            # Conta o número de linhas
            total_linhas_historico = conteudo_historico.count('\n') + 1            
        else:
            total_linhas_historico = 0
        linhas_para_loop = range(1,  56-total_linhas_historico)

        context = {
            'bulletin': bulletin,
            'envolvimentos': envolvimentos,
            'array_envolvidosvazios': array_envolvidosvazios,
            'caminho_local_logo': caminhologolocal,
            'linhas_para_loop': linhas_para_loop,
        }

        template = get_template(template_path)
        html = template.render(context)

        # Cria um buffer de memória
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="boletim.pdf"'

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)

        if not pdf.err:
            response.write(result.getvalue())
            return response
        else:
            return HttpResponse('Erro ao gerar PDF', status=500)

def criar_boletim(request):
    extra_forms = 1  # default

    if request.method == 'POST':
        print('post post post post')
        if 'adicionar_envolvido' in request.POST:
            print('@@@@@@@@add envolvido @@@@@@@@@@@@@@@@@@@@@@@@@@@')
            extra_forms = int(request.POST.get('boletimenvolvimento_set-TOTAL_FORMS', 0)) +1
            boletim_form = BoletimForm(request.POST)
            DynamicFormSet = inlineformset_factory(
                Boletim,
                BoletimEnvolvimento,
                form=BoletimEnvolvimentoForm,
                extra=extra_forms,
                can_delete=True,
            )
            envolvimento_formset = DynamicFormSet()
            envolvidoscadastrados = DynamicFormSet(request.POST)
            X = 0
            for form in envolvidoscadastrados:
                #if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                envolvimento_formset.forms[X]=(form)
                X = X +1
            #leva o focu para o primeiro campo do novo formulario envolvido vazio
            campo_alvo = envolvimento_formset.forms[X].fields['envolvido_nome']
            campo_alvo.widget.attrs.update({'autofocus': 'autofocus'})

            return render(request, 'bulletin_create.html', {
                'boletim_form': boletim_form,
                'envolvimento_formset': envolvimento_formset,
            })

        elif 'salvar' in request.POST:
            print('salvar salvar salvar salvar salvar')
            extra_forms = int(request.POST.get('boletimenvolvimento_set-TOTAL_FORMS', 0))
            boletim_form = BoletimForm(request.POST)
            DynamicFormSet = inlineformset_factory(
                Boletim,
                BoletimEnvolvimento,
                form=BoletimEnvolvimentoForm,
                extra=extra_forms,
                can_delete=True,
            )
            envolvimento_formset = DynamicFormSet(
                request.POST,
                instance=Boletim()
            )
            print('ate aqui ok++++++++++')
            if boletim_form.is_valid() and envolvimento_formset.is_valid():
                print('e aqui 2222222222222222222222')
                boletim = boletim_form.save()
                envolvimento_formset.instance = boletim
                envolvimento_formset.save()
                return redirect('criar_boletim')
            else:
                # Em caso de erro, adicione os formulários (agora com erros) ao contexto
                # e renderize o template novamente
                print("Erros do formulário Boletim:", boletim_form.errors)
                print("Erros do formset de Envolvimento:", envolvimento_formset.errors)
                print("Erros não específicos do formset:", envolvimento_formset.non_form_errors())
                

        # fallback: re-render with errors
        print('Não salvou - deu erro deu erro veriricar ???????????????????')
        return render(request, 'bulletin_create.html', {
            'boletim_form': boletim_form,
            'envolvimento_formset': envolvimento_formset,
        })

    else:# metodo GET
        boletim_form = BoletimForm()
        DynamicFormSet = inlineformset_factory(
            Boletim,
            BoletimEnvolvimento,
            form=BoletimEnvolvimentoForm,
            extra=extra_forms,
            can_delete=True
        )
        envolvimento_formset = DynamicFormSet(instance=Boletim())

        return render(request, 'bulletin_create.html', {
            'boletim_form': boletim_form,
            'envolvimento_formset': envolvimento_formset,
        })