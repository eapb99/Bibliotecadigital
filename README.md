# Bibliotecadigital

Biblioteca Digital con la finalidad de ayudar tanto a los estudiantes como al 
administrador de la biblioteca a mantener un seguimiento constante de todos 
los libros disponibles y de hacer préstamos de estos recursos bibliográficos.

Tabla de Contenido
-----------------

  * [Requerimientos](#requirements)
  * [Como funciona]((#funciona)
  
Requerimientos
------------

BibliotecaDigital requiere las siguientes librerias para funcionar:

  * [Django][django] 4.0+
  * [Django Rest Framework][django-rest] 3.13
  
  
  * Para instalar todas las librerias necesarias para ejecutar el proyecto, ejecute el siguiente comando:
    pip -r install requirements.txt


Como funciona
------------

    Usuarios:
        La biblioteca tendra 2 tipos de usuario
              Administrador
              - Puede agregar nuevos libros al sistema
              - Puede buscar la información de un libro por el código (extra).
              Estudiante
              - Puede ver los libros que están disponibles (código, título, autor, cantidad disponible) y
              hacer préstamo de los mismos.
              - Puede ver la información de los libros que ha prestado (título, autor, fecha de emisión y
              fecha de devolución)
    
    Procesos: 
        Agregar nuevos libros al sistema.
          - Solo se debe solicitar los datos del libro a ingresar (código, título, autor, cantidad disponible). 
          - En caso de que se intente registrar un código ya existente, se deberá aumentar la cantidad de tomos disponibles.
        Préstamo de libros consiste de dos pasos. 
          - El estudiante podrá ver el catálogo y seleccionar un libro a la vez, cada vez que un libro se seleccione este quedará temporalmente reservado. 
          - Para completar el proceso, el estudiante puede confirmar el préstamo o cancelar el proceso. En caso de cancelar el proceso, la cantidad reservada regresará al inventario.
    Requisitos:
          - La fecha de devolución de un libro es igual a 30 días después de haberlo prestado.
          - El estudiante no puede prestar más de un ejemplar del mismo título. 
              Ejemplo: Si ya prestó el libro Física con código 001 durante la reserva o anteriormente y aún no ha sido devuelto, no puede prestar otro libro con el mismo código.


[django]: https://www.djangoproject.com/
[django-rest]: https://www.django-rest-framework.org/
