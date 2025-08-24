from datetime import datetime, timedelta

class Estudiantes:
    def __init__(self, estudiante):
        self.estudiante= estudiante
        self.nombre= input("Digite su nombre: ")
        self.apellido= input("Digite su apellido: ")
        self.codigoestudiante= int(input("Digitu su codigo estudiantil: "))
        self.numerocelular= int(input("Digite su numero celular: "))
Estudiante1= Estudiantes(Estudiantes)
    
class Prestamo:
        def __init__(self,id_libro, id_prestamo):
            self.id_prestamo= id_prestamo
            self.id_libro=id_libro
            self.fecha_prestamo = datetime.now()
            self.fecha_devolucion= self.fecha_prestamo + timedelta(days=7)
        def get_id_prestamo(self):
            return self.id_prestamo
        def set_id_prestamo(self, id_prestamo):
            self.id_prestamo = id_prestamo
        def get_id_libro(self):
            return self.id_libro
        def set_id_libro(self, id_libro):
            self.id_libro = id_libro

Cant= int(input("Digite la cantidad de libros a prestar: "))
for i in range(Cant):
    id_prestamo= int(input("Digite el ID del prestamo: "))
    id_libro= int(input("Digite el ID del libro: "))
    Prestamo1= Prestamo(id_libro, id_prestamo)
    print(f"El ID del prestamo es: {Prestamo1.get_id_prestamo()} y el ID del libro es: {Prestamo1.get_id_libro()}")
    
class Libro:
    def __init__(self, id_libro ):
        self.id_libro = id_libro
        self.ISBN = input("Digite ISBN: ")
        self.titulo = input("Digite Titulo: ")
        self.autor = input("Digite Autor: ")

    def desde_datos(cls, isbn, titulo, autor):
        libro = cls(0)
        libro.ISBN = isbn
        libro.titulo = titulo
        libro.autor = autor
        return libro

    def get_id_libro(self):
        return self.id_libro

    def set_id_libro(self, id_libro):
        self.id_libro = id_libro

    def get_ISBN(self):
        return self.ISBN

    def set_ISBN(self, isbn):
        self.ISBN = isbn

    def get_titulo(self):
        return self.titulo

    def set_titulo(self, titulo):
        self.titulo = titulo

    def get_autor(self):
        return self.autor

    def set_autor(self, autor):
        self.autor = autor

    def editar_campos(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
class Biblioteca:
    def __init__(self):
        self.nro_ejemplares = 0
        self.nombre_colegio = ""
        self.direccion = ""
        self.isbn = ""
        self.tit = ""
        self.aut = ""
        self.estanteria = {}

        try:
            for i in range(Cant):
                self.estanteria[i] = Libro(i)
                self.nro_ejemplares += 1
        except Exception as e:
            print("Error en adición de libro:", e)

    def generar_reporte(self):
        aux = ""
        for posicion in range(Cant):
            libro = self.estanteria[posicion]
            aux += f"{libro.get_id_libro()} - {libro.get_ISBN()} - {libro.get_autor()} - {libro.get_titulo()}\n"

        print("----- Reporte de Libros -----")
        print("Estos libros han sido prestados al estudiane ",Estudiante1.nombre, Estudiante1.apellido, "con codigo estudiantil ",Estudiante1.codigoestudiante, "con fecha ", Prestamo1.fecha_prestamo, "\n La devolución de el/los libros es en la fecha", Prestamo1.fecha_devolucion)
        print(aux)
if __name__ == "__main__":
    solucion = Biblioteca()
    solucion.generar_reporte()