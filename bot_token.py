import platform

def TOKEN():
    sistema = platform.platform()
    if sistema.startswith('Windows-10'):
        # Desarrollo
        token = 'NzI3OTExMzA2Mjg3MzgyNjU4.XxiOzg.3Vott2ezR3sotgMrukP1QYOzZYA'
    else:
        # Produccion
        token = 'NzExOTkwMzYxMTY5NDYxMjk4.Xxhn4w.PxtSwlvIWaxmk-dJMzxrzxs4gIw'
    return token