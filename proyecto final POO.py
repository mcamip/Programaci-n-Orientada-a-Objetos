# sistema_reserva_cine_final.py
import sys
import traceback

# Intentar usar pygame; si falla, usaremos modo consola para selección de sillas
USE_PYGAME = True
try:
    import pygame
except Exception:
    USE_PYGAME = False

# ------------------------
# CLASES (POO BÁSICA)
# ------------------------
class Pelicula:
    def __init__(self, nombre, genero, duracion, clasificacion):
        self.nombre = nombre
        self.genero = genero
        self.duracion = duracion
        self.clasificacion = clasificacion

class Usuario:
    def __init__(self, nombre, celular, cedula):
        self.nombre = nombre
        self.celular = celular
        self.cedula = cedula

class Cine:
    def __init__(self):
        self.peliculas = [
            Pelicula("Harry Potter y el cáliz de fuego", "Fantasía", "2h 37min", "7+"),
            Pelicula("Buscando a Nemo", "Animación", "1h 40min", "TP"),
            Pelicula("Infinity War", "Acción", "2h 40min", "12+")
        ]
        # 5 filas x 4 columnas: 0 libre, 1 ocupada
        self.salas = [[0]*4 for _ in range(5)]

    def mostrar_peliculas(self):
        print()
        for i, p in enumerate(self.peliculas, start=1):
            print(f"{i}. {p.nombre} | Género: {p.genero} | Duración: {p.duracion} | Clasificación: {p.clasificacion}")
        print()

    def asientos_disponibles(self):
        return sum(1 for fila in self.salas for c in fila if c == 0)

# ------------------------
# VALIDACIONES
# ------------------------
def validar_nombre(prompt="Ingrese su nombre: "):
    while True:
        v = input(prompt).strip()
        if v and v.replace(" ", "").isalpha():
            return v
        print("❌ Nombre inválido. Solo letras y espacios. Intente de nuevo.")

def validar_digitos(prompt):
    while True:
        v = input(prompt).strip()
        if v.isdigit():
            return v
        print("❌ Entrada inválida. Solo dígitos permitidos. Intente de nuevo.")

def validar_entero_positivo(prompt):
    while True:
        v = input(prompt).strip()
        if v.isdigit() and int(v) > 0:
            return int(v)
        print("❌ Entrada inválida. Ingrese un número entero positivo.")

def validar_opcion_pelicula():
    # Fuerza que la entrada sea 1, 2 o 3 y no sale hasta que lo sea
    while True:
        v = input("Seleccione una película (1-3): ").strip()
        if v.isdigit():
            iv = int(v)
            if iv in (1,2,3):
                return iv
        print("❌ Opción inválida. Solo 1, 2 o 3.")

def validar_binario_si_no(prompt):
    # Solo acepta "1" o "0"
    while True:
        v = input(prompt).strip()
        if v in ("1","0"):
            return v
        print("❌ Entrada inválida. Ingrese 1 para Sí o 0 para No.")

# ------------------------
# SELECCIÓN DE SILLAS
# ------------------------
def seleccionar_sillas_pygame(cantidad, sala):
    """Abre ventana pygame para seleccionar sillas. Retorna lista de [fila,col] o None si canceló."""
    filas, cols = 5, 4
    tam = 80
    margin = 12
    width = cols * tam + margin*2
    height = filas * tam + margin*2 + 30

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Seleccionar sillas - clic para seleccionar/deseleccionar")
    font = pygame.font.SysFont(None, 22)
    seleccion = []
    clock = pygame.time.Clock()
    instrucciones = f"Seleccione {cantidad} sillas. (verde=seleccionado, rojo=ocupado)"
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                seleccion = None
                running = False
                break
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx,my = pygame.mouse.get_pos()
                # verificar si clic dentro del área de asientos
                if margin <= mx < margin + cols*tam and margin <= my < margin + filas*tam:
                    col = (mx - margin) // tam
                    fila = (my - margin) // tam
                    if 0 <= fila < filas and 0 <= col < cols:
                        if sala[fila][col] == 1:
                            # asiento ocupado: ignorar
                            pass
                        else:
                            coord = [fila, col]
                            if coord in seleccion:
                                seleccion.remove(coord)
                            else:
                                if len(seleccion) < cantidad:
                                    seleccion.append(coord)
        # dibujar
        screen.fill((35,35,35))
        text = font.render(instrucciones, True, (240,240,240))
        screen.blit(text, (10, height-28))
        for r in range(filas):
            for c in range(cols):
                x = margin + c*tam
                y = margin + r*tam
                rect = pygame.Rect(x+6, y+6, tam-12, tam-12)
                if sala[r][c] == 1:
                    color = (170,40,40)
                elif [r,c] in seleccion:
                    color = (40,170,60)
                else:
                    color = (200,200,200)
                pygame.draw.rect(screen, color, rect)
                lbl = font.render(f"{r+1},{c+1}", True, (10,10,10))
                screen.blit(lbl, (x+12, y+12))
        pygame.display.flip()
        clock.tick(30)
        if seleccion is not None and len(seleccion) == cantidad:
            pygame.time.delay(180)
            pygame.quit()
            return seleccion
    # si llegó aquí: cerró ventana
    try:
        pygame.quit()
    except:
        pass
    return None

def seleccionar_sillas_consola(cantidad, sala):
    """Modo consola: mostrar mapa y pedir coordenadas hasta completar o cancelar."""
    filas, cols = 5,4
    seleccion = []
    while True:
        # imprimir mapa simple
        print("\nMapa de asientos (0=libre, X=ocupado):")
        for r in range(filas):
            rowstr = []
            for c in range(cols):
                if sala[r][c] == 1:
                    rowstr.append(" X ")
                elif [r,c] in seleccion:
                    rowstr.append("[S]")
                else:
                    rowstr.append(f"{r+1},{c+1}")
            print(" | ".join(rowstr))
        print(f"Seleccionadas: {len(seleccion)}/{cantidad}")
        if len(seleccion) == cantidad:
            return seleccion
        entrada = input("Ingrese asiento en formato fila,col (ej: 2,3) o 'cancelar': ").strip()
        if entrada.lower() == "cancelar":
            return None
        if "," in entrada:
            parts = entrada.split(",")
            if len(parts)==2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                fr = int(parts[0].strip())-1
                co = int(parts[1].strip())-1
                if 0<=fr<filas and 0<=co<cols:
                    if sala[fr][co]==1:
                        print("Ese asiento ya está ocupado. Elija otro.")
                    else:
                        coord = [fr,co]
                        if coord in seleccion:
                            seleccion.remove(coord)
                            print("Asiento deseleccionado.")
                        else:
                            if len(seleccion) < cantidad:
                                seleccion.append(coord)
                                print("Asiento seleccionado.")
                            else:
                                print("Ya seleccionó la cantidad solicitada.")
                    continue
        print("Entrada inválida. Use el formato fila,col (por ejemplo 1,1) o 'cancelar'.")

def seleccionar_sillas(cantidad, sala):
    # Si pygame disponible intentar modo gráfico, si hay problema usar consola
    if USE_PYGAME:
        try:
            res = seleccionar_sillas_pygame(cantidad, sala)
            if res is not None:
                return res
            # si res es None (canceló), devolvemos None para que el flujo lo maneje
            return None
        except Exception as e:
            print("⚠️ Ocurrió un problema con pygame. Cayendo a modo consola.")
            traceback.print_exc()
            return seleccionar_sillas_consola(cantidad, sala)
    else:
        print("Modo consola activado (pygame no disponible).")
        return seleccionar_sillas_consola(cantidad, sala)

# ------------------------
# LÓGICA PRINCIPAL
# ------------------------
def sistema_cine():
    cine = Cine()
    PRECIO = 8000
    print("\n--- SISTEMA DE RESERVA DE CINE ---\n")
    while True:
        try:
            cine.mostrar_peliculas()
            nombre = validar_nombre("Ingrese su nombre: ")
            celular = validar_digitos("Ingrese su número de celular (solo dígitos): ")
            cedula = validar_digitos("Ingrese su número de cédula (solo dígitos): ")
            usuario = Usuario(nombre, celular, cedula)

            # validar película (1-3)
            opcion = validar_opcion_pelicula()
            pelicula = cine.peliculas[opcion-1]  # seguro, porque validar_opcion_pelicula garantiza 1..3

            disponibles = cine.asientos_disponibles()
            if disponibles == 0:
                print("No hay asientos disponibles.")
                v = validar_binario_si_no("¿Desea intentar otra reserva? (1=Sí,0=No): ")
                if v == "1":
                    continue
                else:
                    print("Saliendo. Gracias.")
                    break

            # cantidad
            while True:
                cantidad = validar_entero_positivo("¿Cuántas sillas desea reservar?: ")
                if cantidad <= disponibles:
                    break
                print(f"❌ Solo quedan {disponibles} asientos disponibles. Intente con un número menor o igual.")

            print("\nSe abrirá la selección de sillas. Si cierra la ventana antes de terminar, podrá elegir si intenta otra reserva.")
            seleccion = seleccionar_sillas(cantidad, cine.salas)
            if seleccion is None:
                print("No se completó la selección de sillas.")
                v = validar_binario_si_no("¿Desea intentar otra reserva? (1=Sí,0=No): ")
                if v == "1":
                    continue
                else:
                    print("Saliendo. Gracias.")
                    break

            # marcar ocupadas
            for (r,c) in seleccion:
                cine.salas[r][c] = 1

            total = cantidad * PRECIO
            print("\n--- RESERVA CONFIRMADA ---")
            print(f"Cliente: {usuario.nombre}")
            print(f"Teléfono: {usuario.celular}")
            print(f"Cédula: {usuario.cedula}")
            print(f"Película: {pelicula.nombre}")
            print(f"Sillas (fila,col): {seleccion}")
            print(f"Total a pagar: ${total:,}")
            print("--------------------------")

            repetir = validar_binario_si_no("¿Desea realizar otra reserva? (1=Sí,0=No): ")
            if repetir == "1":
                continue
            else:
                print("Compra finalizada. ¡Disfrute su película!")
                break

        except Exception as e:
            print("Ocurrió un error inesperado:", e)
            traceback.print_exc()
            v = validar_binario_si_no("¿Desea intentar de nuevo? (1=Sí,0=No): ")
            if v == "1":
                continue
            else:
                print("Saliendo. Adiós.")
                break

if __name__ == "__main__":
    sistema_cine()
