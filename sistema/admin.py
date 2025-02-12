from django.contrib import admin
from .models import *

class PagamentoAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # Atualiza o status da venda
        venda = Venda.objects.get(id=obj.venda.id)
        if venda.status == 'Pendente':
            venda.status = 'Aprovada'
            venda.save()
            # Registrar o status
            super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Cliente)
admin.site.register(Veiculo)
admin.site.register(Vendedor)
admin.site.register(Venda)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(TipoPagamento)







