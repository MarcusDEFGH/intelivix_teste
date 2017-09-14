# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider
from kabum.items import KabumItem


class KabumSpider(CrawlSpider):
    name = "kabumspider"
    allowed_domain = ["www.kabum.com.br"]

    start_urls = [
        "https://www.kabum.com.br/"]

    next_url = "?string=&pagina=X&ordem=5&limite=100"

    # pega o link de cada categoria
    def parse(self, response):

        links = response.xpath(
            '//p[@class = "bot-categoria"]/a/@href').extract()

        for j in range(len(links)):
            for i in range(1, 10):
                links.append(links[j].encode('ascii', 'ignore') +
                             (str(i).join(self.next_url.split("X"))))
        for link in links:
            yield Request(url=link.encode('ascii', 'ignore'), callback=self.parseCategoria)

    # pega os links dos produtos de cada categoria
    def parseCategoria(self, response):
        links = response.xpath('//span[@class = "H-titulo"]/a/@href').extract()
        for link in links:
            yield Request(url=link.encode('ascii', 'ignore'), callback=self.parseProduto)

    # pega as informacoes dos produtos
    # mongodb por algum motivo não permite o caractere '.', logo eu removi ele de todos os lugares onde aparecia
    def parseProduto(self, response):
        item = KabumItem()
        if response.url != "https://www.kabum.com.br/404":

            if ('oferta' not in response.url):
                valor = response.xpath(
                    '//meta[@itemprop = "price"]/@content').extract_first()
                if (valor != None):
                	item['valor'] = float(valor)
                valor_antigo = response.xpath(
                    '//div[@class="preco_normal"]/text()').extract_first()
                if (valor_antigo != None):
                    valor_antigo = float(valor_antigo.replace('.', '').replace(
                        'R$', '').replace('\t', '').replace('\n', '').replace(',', '.').strip())
                item['valor_antigo'] = valor_antigo
            else:
                valor = response.xpath(
                    '//div[@class="preco_desconto-cm"]/span/strong/text()').extract_first()
                if (valor != None):
                    valor = float(valor.split(' ')[1].replace('.', '').replace(',', '.'))
                item['valor'] = valor

                valor_antigo = response.xpath(
                    '//div[@class="preco_antigo-cm"]/text()').extract_first()
                if (valor_antigo != None):
                    valor_antigo = float(valor_antigo.split(" ")[
                                         2].replace('.', '').replace(',', '.'))
                item['valor_antigo'] = valor_antigo

            item['url'] = response.url
            item['nome'] = response.xpath(
                '//div[@id="titulo_det"]/h1/text()').extract()[0].encode('ascii', 'ignore')
            item['descricao'] = response.xpath(
                '//p[@itemprop="description"]/text()').extract()[0].encode('ascii', 'ignore')
            item['categoria'] = response.xpath(
                './/*[@itemscope]/*[@itemprop]/text()').extract()[1].split(' ')[0].encode('ascii', 'ignore')
            item['marca'] = response.xpath(
                '//div[@class="marcas"]/meta/@content').extract_first()
            navegacao = response.xpath(
                './/*[@itemscope]/*[@itemprop]/text()').extract()
            item['navegacao'] = ' '.join([x for x in (navegacao) if any(
                '>' == c for c in x)]).encode('ascii', 'ignore')
            item['nome_vendedor'] = 'Kabum eletronicos'
            item['imagem_principal'] = response.xpath(
                '//ul[@class = "slides"]/li/img/@src').extract_first()
            imagens = response.xpath(
                '//ul[@class = "slides"]/li/img/@src').extract()[1:]
            item['imagens_secundarias'] = [x for x in imagens if '_g.jpg' in x]
            # item['dimensoes'] = já em caracteristicas
            caracteristicas = ''.join(response.xpath(
                './/div[@class = "content_tab"]/p')[4:].extract()).split('<p>')
            titulos = [caracteristicas.index(
                x) for x in caracteristicas if('strong' in x)]
            carac = {}
            for titulo in titulos:
                subconjunto = ''
                if (titulos.index(titulo) + 1 != len(titulos)):
                    for i in range(titulo + 1, titulos[titulos.index(titulo) + 1]):
                        subconjunto += caracteristicas[i].encode(
                            'ascii', 'ignore').replace('.', '')
                    carac_limpa = caracteristicas[titulo].replace('<strong>', '').replace('<span>', '').replace(
                        '</strong>', '').replace('.', '').replace('</p>', '').encode('ascii', 'ignore')
                    carac[carac_limpa] = subconjunto.replace(
                        '</p>', '').replace('.', '').encode('ascii', 'ignore')
                item['caracteristicas'] = carac

        yield item
