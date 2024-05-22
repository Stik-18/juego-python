import pygame
import random

pygame.init()


ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60


def cargar_imagen(ruta, ancho=None, alto=None):
    try:
        imagen = pygame.image.load(ruta)
        if ancho and alto:
            imagen = pygame.transform.scale(imagen, (ancho, alto))
        return imagen
    except pygame.error as e:
        print(f"No se pudo cargar la imagen en {ruta}: {e}")
        return None

# Clase Manzana
class Manzana:
    def __init__(self, velocidad, imagen):
        self.x = random.randint(0, ANCHO_PANTALLA - imagen.get_width())
        self.y = 0
        self.velocidad = velocidad
        self.imagen = imagen

    def caer(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

# Clase Canasta
class Canasta:
    def __init__(self, imagen):
        self.x = ANCHO_PANTALLA // 2
        self.y = ALTO_PANTALLA - imagen.get_height() - 10
        self.ancho = imagen.get_width()
        self.alto = imagen.get_height()
        self.velocidad = 10
        self.imagen = imagen

    def mover(self, direccion):
        if direccion == "izquierda" and self.x > 0:
            self.x -= self.velocidad
        if direccion == "derecha" and self.x < ANCHO_PANTALLA - self.ancho:
            self.x += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

# Clase Juego
class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Juego de Atrapar Manzanas")
        self.reloj = pygame.time.Clock()
        self.manzana_imagen = cargar_imagen("manzana.png", 50, 50)  
        self.canasta_imagen = cargar_imagen("canasta.png", 150, 50)  
        self.fondo_imagen = cargar_imagen("fondo.jpg", ANCHO_PANTALLA, ALTO_PANTALLA)

        if not self.manzana_imagen or not self.canasta_imagen or not self.fondo_imagen:
            raise SystemExit("Error: No se pudieron cargar las imágenes necesarias.")

        self.manzanas = []
        self.canasta = Canasta(self.canasta_imagen)
        self.puntuacion = 0
        self.ejecutando = True
        self.intervalo_manzana = 2000  # el Intervalo inicial es en milisegundos
        self.tiempo_ultimo = pygame.time.get_ticks()

    def nueva_manzana(self):
        self.manzanas.append(Manzana(self.puntuacion // 5 + 5, self.manzana_imagen))

    def verificar_colisiones(self):
        for manzana in self.manzanas:
            if self.canasta.y < manzana.y + self.manzana_imagen.get_height() and self.canasta.y + self.canasta.alto > manzana.y:
                if self.canasta.x < manzana.x + self.manzana_imagen.get_width() and self.canasta.x + self.canasta.ancho > manzana.x:
                    self.manzanas.remove(manzana)
                    self.puntuacion += 1
                    if self.puntuacion % 5 == 0: #se aumenta la dificultad cada 5 manzanas
                        self.incrementar_dificultad()

    def verificar_perdida(self):
        for manzana in self.manzanas:
            if manzana.y > ALTO_PANTALLA:
                self.ejecutando = False

    def incrementar_dificultad(self):
        self.intervalo_manzana = max(500, self.intervalo_manzana - 200)  # Reducir intervalo

    def ejecutar(self):
        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.canasta.mover("izquierda")
            if teclas[pygame.K_RIGHT]:
                self.canasta.mover("derecha")

            self.pantalla.blit(self.fondo_imagen, (0, 0))

            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo > self.intervalo_manzana:
                self.nueva_manzana()
                self.tiempo_ultimo = tiempo_actual

            for manzana in self.manzanas:
                manzana.caer()
                manzana.dibujar(self.pantalla)

            self.verificar_colisiones()
            self.verificar_perdida()
            self.canasta.dibujar(self.pantalla)
            self.mostrar_puntuacion()

            pygame.display.flip()
            self.reloj.tick(FPS)

        self.mostrar_mensaje_perdida()

    def mostrar_puntuacion(self):
        fuente = pygame.font.SysFont(None, 36)
        texto = fuente.render(f"Puntuación: {self.puntuacion}", True, (255, 255, 255))
        self.pantalla.blit(texto, (10, 10))

    def mostrar_mensaje_perdida(self):
        self.pantalla.fill((0, 0, 0))
        fuente = pygame.font.SysFont(None, 72)
        texto = fuente.render("¡Perdiste!", True, (255, 0, 0))
        self.pantalla.blit(texto, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 - 36))
        pygame.display.flip()
        pygame.time.wait(3000)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
    pygame.quit()


