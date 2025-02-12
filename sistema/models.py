from django.db import models
# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    ano = models.CharField(max_length=4)
    preco = models.FloatField()
    foto = models.ImageField()

    def __str__(self):
        return f'{self.modelo} R${self.preco}'

class Vendedor(models.Model):
    nome = models.CharField(max_length=40)
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name='Vendedore'

class Venda(models.Model):
    data_venda = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pendente')

    def __str__(self):
        return f"{self.veiculo} Status : {self.status}"

class TipoPagamento(models.Model):
    descricao = models.CharField(max_length=100)
    desconto = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.descricao}'


class Pagamento(models.Model):
    valor = models.FloatField()
    data_pagamento = models.DateTimeField()
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    tipo_pag = models.ForeignKey(TipoPagamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venda concluida no valor de R${self.valor}"

    class Meta:
        verbose_name='Pagamento'


