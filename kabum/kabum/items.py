# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"




class KabumItem(scrapy.Item):
    url = scrapy.Field() 				# Url do produto sendo extraído
    nome = scrapy.Field() 				# Nome do produto
    descricao = scrapy.Field()			# Texto contendo a descrição do produto
    categoria = scrapy.Field()			# Categoria em que o produto se enquadra
    marca = scrapy.Field()				# Marca do produto
    navegacao = scrapy.Field() 			# (string list) Lista de categorias e subcategorias de navegação, indo do mais geral para mais específico
    valor = scrapy.Field() 				# (float) Valor atual do produto
    valor_antigo = scrapy.Field() 		# (float) Valor do produto sem desconto, se houver
    imagem_principal = scrapy.Field() 	# (string) URL da imagem do produto
    imagens_secundarias = scrapy.Field()# (string list) Lista de URL das imagens secundárias
    caracteristicas = scrapy.Field() 	# (list dict) Lista de dicionários contendo as caracteristicas do produto Ex.: [{'name': 'Cor', 'value': 'Preto'}]



class StackItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
