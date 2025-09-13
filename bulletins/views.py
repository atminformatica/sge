from django.shortcuts import render, redirect
from .models import Boletim, BoletimEnvolvimento
from .forms import BoletimForm, BoletimEnvolvimentoForm
from django.forms import inlineformset_factory

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
                can_delete=True
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
                can_delete=True
            )
            envolvimento_formset = DynamicFormSet(
                request.POST,
                instance=Boletim()
            )

            if boletim_form.is_valid() and envolvimento_formset.is_valid():
                boletim = boletim_form.save()
                envolvimento_formset.instance = boletim
                envolvimento_formset.save()
                return redirect('criar_boletim')

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