def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            total += len(request.session["carrito"])
    return {"total_carrito": total}
