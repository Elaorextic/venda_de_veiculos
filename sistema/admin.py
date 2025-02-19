from django.contrib import admin
from .models import *
from django.contrib import messages

class VendaAdmin(admin.ModelAdmin):
    readonly_fields = ('status',)
class PagamentoAdmin(admin.ModelAdmin):
    readonly_fields = ('saldo',)
    def save_model(self, request, obj, form, change):
        # Atualiza o status da venda
        venda = Venda.objects.get(id=obj.venda.id)




        obj.saldo = obj.venda.veiculo.preco - obj.valor

        if venda.status == 'Aprovada':  # Ver se a venda já está aprovada
            messages.set_level(request, messages.ERROR)
            messages.error(request, "ERRO, Esse pagamento já está aprovado!")
            return

        if venda.status == 'Pendente':


            if obj.valor == obj.venda.veiculo.preco: # Ver se o valor e igual ao valor do veiculo
                venda.status = 'Aprovada'
                venda.save()
                # Registrar o status
                super().save_model(request, obj, form, change)

            elif obj.venda.veiculo.preco > obj.valor: # Ver se o valor do veiculo e maior do que o pagamento
                venda.status = 'Pendente'
                venda.save()
                #Registrar o status Novamente
                super().save_model(request, obj, form, change)
                messages.set_level(request, messages.INFO)
                messages.info(request, f"Seu pagamento não foi totalmente concluido, ainda esta pendente o valor de {obj.saldo} ")


            elif obj.valor > obj.venda.veiculo.preco: # Ver se o valor do pagamento e maior do que o do veiculo
                messages.set_level(request, messages.ERROR)
                messages.error(request, "ERRO, Esse pagamento esta acima do valor da venda!")
                return





# Register your models here.
admin.site.register(Cliente)
admin.site.register(Veiculo)
admin.site.register(Vendedor)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(TipoPagamento)







