from django.contrib import admin
from .models import *
from django.contrib import messages

class VendaAdmin(admin.ModelAdmin):
    readonly_fields = ('status',)
class PagamentoAdmin(admin.ModelAdmin):
    readonly_fields = ('saldo',)
    def save_model(self, request, obj, form, change):
        venda = obj.venda

        # Calcular o total já pago antes desse pagamento
        total_pago = sum(pag.valor for pag in Pagamento.objects.filter(venda=venda))
        # Calcular o novo saldo considerando este pagamento
        saldo_atualizado = venda.veiculo.preco - (total_pago + obj.valor)




        obj.saldo = obj.venda.veiculo.preco - obj.valor

        if venda.status == 'Aprovada':  # Ver se a venda já está aprovada
            messages.set_level(request, messages.ERROR)
            messages.error(request, "ERRO, Esse pagamento já está aprovado!")
            return

        if saldo_atualizado == 0:  # Pagamento total concluído
            venda.status = 'Aprovada'
            venda.save()
            obj.saldo = saldo_atualizado  # Atualiza saldo
            super().save_model(request, obj, form, change)
            messages.success(request, f"Pagamento completo! A venda foi aprovada.")

        elif saldo_atualizado > 0:  # Pagamento Parcelado
            venda.status = 'Pendente'
            venda.save()
            obj.saldo = saldo_atualizado  # Atualiza saldo
            super().save_model(request, obj, form, change)
            messages.set_level(request, messages.WARNING)
            messages.warning(request, f"Pagamento parcial! Ainda falta pagar R${saldo_atualizado:.2f}.")


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







