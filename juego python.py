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
    def __init__(self, velocidad, imagen, especial=False, bonus=False):
        self.x = random.randint(0, ANCHO_PANTALLA - imagen.get_width())
        self.y = 0
        self.velocidad = velocidad
        self.imagen = imagen
        self.especial = especial
        self.bonus = bonus

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
        self.canasta_imagen = cargar_imagen("canasta.png", 150, 70)  
        self.fondo_imagen = cargar_imagen("fondo.jpg", ANCHO_PANTALLA, ALTO_PANTALLA)
        self.manzana_dorada_imagen = cargar_imagen("manzana_dorada.png", 30, 30) 

        if not self.manzana_imagen or not self.canasta_imagen or not self.fondo_imagen or not self.manzana_dorada_imagen:
            raise SystemExit("Error: No se pudieron cargar las imágenes necesarias.")

        self.manzanas = []
        self.canasta = Canasta(self.canasta_imagen)
        self.puntuacion = 0
        self.ejecutando = True
        self.intervalo_manzana = 2000  
        self.tiempo_ultimo = pygame.time.get_ticks()
        self.nivel = 1
        self.mostrar_nivel = False
        self.tiempo_mostrar_nivel = 0
        self.manzana_dorada = None
        self.ronda_rafaga = False
        self.tiempo_rafaga = 0

    def nueva_manzana(self, especial=False, bonus=False):
        velocidad_manzana = self.puntuacion // 5 + 5
        imagen = self.manzana_dorada_imagen if especial else self.manzana_imagen
        self.manzanas.append(Manzana(velocidad_manzana, imagen, especial, bonus))

    def verificar_colisiones(self):
        for manzana in self.manzanas:
            if self.canasta.y < manzana.y + manzana.imagen.get_height() and self.canasta.y + self.canasta.alto > manzana.y:
                if self.canasta.x < manzana.x + manzana.imagen.get_width() and self.canasta.x + self.canasta.ancho > manzana.x:
                    self.manzanas.remove(manzana)
                    if manzana.especial:
                        self.puntuacion += 5
                        self.iniciar_rafaga()
                    elif not manzana.bonus:
                        self.puntuacion += 1
                    if self.puntuacion % 5 == 0:  
                        self.incrementar_dificultad()
                        self.mostrar_nivel = True
                        self.tiempo_mostrar_nivel = pygame.time.get_ticks()

    def verificar_perdida(self):
        for manzana in self.manzanas:
            if manzana.y > ALTO_PANTALLA and not manzana.especial and not manzana.bonus:
                self.ejecutando = False

    def incrementar_dificultad(self):
        self.nivel += 1
        self.intervalo_manzana = max(500, self.intervalo_manzana - 200) 
        self.nueva_manzana(especial=True)  

    def iniciar_rafaga(self):
        self.ronda_rafaga = True
        self.tiempo_rafaga = pygame.time.get_ticks()

    def ejecutar_rafaga(self):
        if self.ronda_rafaga:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_rafaga <= 70:  
                self.nueva_manzana(bonus=True)
            else:
                self.ronda_rafaga = False

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
            if tiempo_actual - self.tiempo_ultimo > self.intervalo_manzana and not self.ronda_rafaga:
                self.nueva_manzana()
                self.tiempo_ultimo = tiempo_actual

            self.ejecutar_rafaga()

            for manzana in self.manzanas:
                manzana.caer()
                manzana.dibujar(self.pantalla)

            self.verificar_colisiones()
            self.verificar_perdida()
            self.canasta.dibujar(self.pantalla)
            self.mostrar_puntuacion()

            if self.mostrar_nivel:
                self.mostrar_mensaje_nivel()
                if tiempo_actual - self.tiempo_mostrar_nivel > 2000:  
                    self.mostrar_nivel = False

            pygame.display.flip()
            self.reloj.tick(FPS)

        self.mostrar_mensaje_perdida()

    def mostrar_puntuacion(self):
        fuente = pygame.font.SysFont(None, 36)
        texto = fuente.render(f"Puntuación: {self.puntuacion}", True, (255, 255, 255))
        self.pantalla.blit(texto, (10, 10))

    def mostrar_mensaje_nivel(self):
        fuente = pygame.font.SysFont(None, 72)
        texto = fuente.render(f"Nivel {self.nivel}", True, (0, 0, 0))
        self.pantalla.blit(texto, (ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 - 36))

    def mostrar_mensaje_perdida(self):
        self.pantalla.fill((0, 0, 0))
        fuente = pygame.font.SysFont(None, 72)
        texto = fuente.render(f"¡Perdiste! Nivel maximo:{self.nivel}", True, (255, 0, 0))
        self.pantalla.blit(texto, (ANCHO_PANTALLA // 5 - 50, ALTO_PANTALLA // 2 - 36))
        pygame.display.flip()
        pygame.time.wait(3000)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
    pygame.quit()


