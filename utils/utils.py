def format_prices(val):
    #to format the product price
    return f'{val:.2f} €'.replace('.',',')

def cart_total_qtd(cart):
    return sum([item['quantity'] for item in cart.values()])

def cart_totals(cart):
    return sum(
        [
            item.get('price_quantity_promotion')
            if item.get('price_quantity_promotion')
            else item.get('price_quantity')
            for item
            in cart.values()
        ]
    )
 
