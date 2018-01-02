from curris.block import _check_unorder_list_item, _check_order_list_item

def list_item(symbol):
    if symbol.isdigit():
        return symbol + '. item'
    return symbol + ' item'


def test_order_list_item():
    for i in ['1', '2', '3', '4', '5']:
        content = [i for i in 'item']
        result = {'block_type': 'order_list_item',
                  'content': [[{'span_type': 'text', 'content': content}]]}
        target = list_item(i)
        assert _check_order_list_item(target, len(target)) == result

def test_unorder_list_item():
    for i in ['-']:
        content = [i for i in 'item']
        result = {'block_type': 'unorder_list_item',
                  'content': [[{'span_type': 'text', 'content': content}]]}
        target = list_item(i)
        assert _check_unorder_list_item(target, len(target)) == result
