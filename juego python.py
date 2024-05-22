import pygame
import random

pygame.init()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
COLOR_FONDO = (0, 0, 0)
COLOR_MANZANA = (255, 0, 0)
COLOR_CANASTA = (0, 255, 0)
FPS = 60

# Clase Manzana
class Manzana:
    def __init__(self, velocidad):
        self.x = random.randint(0, ANCHO_PANTALLA - 20)
        self.y = 0
        self.velocidad = velocidad

    def caer(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_MANZANA, (self.x, self.y, 20, 20))

# Clase Canasta
class Canasta:
    def __init__(self):
        self.x = ANCHO_PANTALLA // 2
        self.y = ALTO_PANTALLA - 50
        self.ancho = 100
        self.alto = 20
        self.velocidad = 10

    def mover(self, direccion):
        if direccion == "izquierda" and self.x > 0:
            self.x -= self.velocidad
        if direccion == "derecha" and self.x < ANCHO_PANTALLA - self.ancho:
            self.x += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_CANASTA, (self.x, self.y, self.ancho, self.alto))

# Clase Juego
class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Juego de Atrapar Manzanas")
        self.reloj = pygame.time.Clock()
        self.manzanas = []
        self.canasta = Canasta()
        self.puntuacion = 0
        self.ejecutando = True
        self.intervalo_manzana = 2000  
        self.tiempo_ultimo = pygame.time.get_ticks()

    def nueva_manzana(self):
        self.manzanas.append(Manzana(self.puntuacion // 5 + 5))

    def verificar_colisiones(self):
        for manzana in self.manzanas:
            if self.canasta.y < manzana.y + 20 and self.canasta.y + self.canasta.alto > manzana.y:
                if self.canasta.x < manzana.x + 20 and self.canasta.x + self.canasta.ancho > manzana.x:
                    self.manzanas.remove(manzana)
                    self.puntuacion += 1
                    if self.puntuacion % 5 == 0:
                        self.incrementar_dificultad()

    def verificar_perdida(self):
        for manzana in self.manzanas:
            if manzana.y > ALTO_PANTALLA:
                self.ejecutando = False

    def incrementar_dificultad(self):
        self.intervalo_manzana = max(500, self.intervalo_manzana - 200)  # Reducir intervalo, mínimo 500ms

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

            self.pantalla.fill(COLOR_FONDO)

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
        self.pantalla.fill(COLOR_FONDO)
        fuente = pygame.font.SysFont(None, 72)
        texto = fuente.render("¡Perdiste!", True, (255, 0, 0))
        self.pantalla.blit(texto, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 - 36))
        pygame.display.flip()
        pygame.time.wait(3000)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
    pygame.quit()