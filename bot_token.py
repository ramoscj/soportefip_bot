import platform

def TOKEN():
    sistema = platform.platform()
    if sistema.startswith('Windows-10'):
        # Desarrollo
        token = 'NzI3OTExMzA2Mjg3MzgyNjU4.Xvy-GA.V1I7jAtOvunlD9I2_J-DZyDRGcg'
    else:
        # Produccion
        token = 'NzExOTkwMzYxMTY5NDYxMjk4.Xv4SZQ.sQOuiP9yqLz6xb8FJSQSWFrq9Jk'
    return token