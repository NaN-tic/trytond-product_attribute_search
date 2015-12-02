# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__metaclass__ = PoolMeta
__all__ = ['Product']


class Product:
    __name__ = 'product.product'
    attributes_string = fields.Function(fields.Char('Attributes'),
        'get_attributes_string', searcher='search_attributes_string')

    @classmethod
    def get_attributes_string(cls, products, name):
        result = {}.fromkeys([x.id for x in products], '')
        for product in products:
            if not product.attributes:
                continue
            result[product.id] = ','.join(['%s:%s' % (key, value)
                    for key, value in product.attributes.iteritems()])
        return result

    @classmethod
    def search_attributes_string(cls, name, clause):
        pool = Pool()
        Attribute = pool.get('product.attribute')
        domains = []
        keys = [x.name for x in Attribute.search([])]
        for value in str(clause[2]).split(' '):
            for key in keys:
                domains.append(('attributes', clause[1], {key: value}))
        if not domains:
            return domains
        domains.insert(0, 'OR')
        return domains
