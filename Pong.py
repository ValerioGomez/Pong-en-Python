import sys
import pygame
import random
from tkinter.font import ITALIC
#Pantalla 900 x 480
ANCHO = 900
ALTO = 480
#Asignamos algunos colores
BLANCO = (255, 255, 255)
ColorPantalla = (0, 0, 0)
ColorBola = (255, 0, 0)
#Cargamos imagenes para icono, lofo y fondo
fondo = pygame.image.load("imagen/logo2.png")
tecla= pygame.image.load("imagen/tecla.png")
icono = pygame.image.load("imagen/logo.png")
pygame.display.set_icon(icono)
#funcion de ayuda para mostrar el puntaje y jugadores
def texto(texto, tam=20, color=(0, 0, 0)):
    #Pasamos como parametros el tipo de letra y tamaño
    fuente = pygame.font.SysFont("comicsanz", tam)
    #retornamos la Funcion con los mismos parametros
    return fuente.render(texto, True, color)
#Creamos la Clase Barra
class Barra():
    def __init__(pong, jugador):#pasamos parametros el objeto y jugador
        #tmaño de la barra [horizontal,vertical]
        pong.TamanoBarra = [10, 150]
        #La posicion Vertical sera igual a (480/2 - 150/2) = 165
        pos_vertical = ALTO / 2 - pong.TamanoBarra[1] / 2
        #Creamos Jugadores
        if jugador == 1:
            #Para el jugador 1 la posicion sera [0,165] a la izquierda
            pong.pos = [0, pos_vertical]
        elif jugador == 2:#posicion [900-10,165]
            #Para el jugador 2 la posicion sera [890,165] a la derecha
            pong.pos = [ANCHO - pong.TamanoBarra[0], pos_vertical]
        #La velocidad de la Barra sera 0 estatico
        pong.velocidad = 0
        #definimos la aceleracion cada cierto numero de colisiones
        pong.aceleracion = 6
        #verificamos visualizando los datos en la consola
        print(pos_vertical)
    #Definimos las funciones posicion, alrgo y ancho de la barra, retornando sus valores
    def posicion(pong):
        return pong.pos[1]#retornamos posicion_vertical = 165
    def largo(pong):
        return pong.TamanoBarra[1]#retornamos el tamaño de la barra = 150 largo
    def ancho(pong):
        return pong.TamanoBarra[0]#retornamos el tamaño de la barra = 10 ancho
    #creamos la funcion para mover la barra, pasando como parametros el objeto y la direccion
    def mover(pong, direccion):
        if direccion == "no":#sino hay direccion, la velocidad es 0
            pong.velocidad = 0
        elif direccion == "arriba":
            #la velocidad disminuira en funcion a la aceleracion, hacia arriba
            #velocidad = 0 entonces, desacelera con 6, o velocidad = -6
            pong.velocidad = pong.velocidad - pong.aceleracion
        elif direccion == "abajo":
            #la velocidad sera igual a la aceleracion, hacia abajo
            pong.velocidad = pong.aceleracion
    #ahora actualizamos el objeto
    def actualizar(pong):
        #la posicion dela barra se le sumara la velocidad
        #en este caso, 165 +6 = 173, simulando el movimiento
        pong.pos[1] = pong.pos[1] + pong.velocidad
        if pong.pos[1] < 0:#la posicion es negativa se vuelve 0
            pong.pos[1] = 0
        #si si la posicion de largo es mayor al alto(si se pasa)
        elif pong.pos[1] + pong.largo() > ALTO:
            #la posicion sera 480-150 = 330(linea 47)
            pong.pos[1] = ALTO - pong.largo()       
    #ahora dibujamos las dos barras de lsi jugadores
    def dibujar1(pong, pantalla):
        pygame.draw.rect(pantalla, (255,0,0), [pong.pos, pong.TamanoBarra])
    def dibujar2(pong, pantalla):
        pygame.draw.rect(pantalla, (0,0,255), [pong.pos, pong.TamanoBarra])
    def reiniciarPaleta(pong,jugador):
        pos_vertical = ALTO / 2 - pong.TamanoBarra[1] / 2
        if jugador == 1:
            #Para el jugador 1 la posicion sera [0,165] a la izquierda
            pong.pos = [0, pos_vertical]
        elif jugador == 2:#posicion [900-10,165]
            #Para el jugador 2 la posicion sera [890,165] a la derecha
            pong.pos = [ANCHO - pong.TamanoBarra[0], pos_vertical]
#Creamos la Clase Bola
class Pelota():
    def __init__(pong):  #iniciamos el constructor
        #aleatorio genera un decimal entre 0 y 1
        aleatorio = random.random()
        #Definimos la la variable Posicion con la mitad del ancho y el largo      
        pong.pos = [ANCHO / 2, ALTO / 2]
        #Ledamos valor al Radio de la pelotita
        pong.radio = 10
        #iniciamos la velocidad horizontal x y vertical y [x,y]
        pong.velocidad = [4, 4 * aleatorio + 4]
        #el incremento aumentara la velocidad cada vez que toque la barra      
        pong.incremento_velocidad = 1.1
        #generamos el lado del impacto donde colisionara lal pelota
        pong.lado_impacto = ""
        pong.sonido_rebote = pygame.mixer.Sound("audio/rebote.wav")
    #definimosla funcion si hay impacto, devolviendo el lado del impacto
    def hayImpacto(pong):
        return pong.lado_impacto       
    #Creamos la Logica del Objeto en Pantalla de la pelota
    def actualizar(pong, barra1, barra2):
        pong.pos[0] += int(pong.velocidad[0])
        pong.pos[1] += int(pong.velocidad[1])

        if pong.pos[1] <= pong.radio or pong.pos[1] >= ALTO - pong.radio:
            pong.velocidad[1] *= -1        
            pong.sonido_rebote.play()
        elif pong.pos[0] < pong.radio + barra1.ancho():
            if pong.pos[1] > barra1.posicion() and pong.pos[1] < barra1.posicion() + barra1.largo():
                
                pong.pos[0] = barra1.ancho() + pong.radio
                pong.velocidad[0] *= -1 * pong.incremento_velocidad
                pong.sonido_rebote.play()
            else:                           
                pong.lado_impacto = "izquierda"
                pong.sonido_rebote.play()              

        elif pong.pos[0] >= ANCHO - pong.radio - barra2.ancho():
            if pong.pos[1] > barra2.posicion() and pong.pos[1] < barra2.posicion() + barra2.largo():
                pong.pos[0] = ANCHO - barra2.ancho() - pong.radio
                pong.velocidad[0] *= -1 * pong.incremento_velocidad
                pong.sonido_rebote.play()
            else:                
                pong.lado_impacto = "derecho"
                pong.sonido_rebote.play()                
    def reiniciar(pong):
        pong.pos = [ANCHO / 2, ALTO / 2]
        pong.velocidad = [4, 4 * random.random() + 4]
        if pong.lado_impacto == "derecho":
            pong.velocidad[0] *= -1
        pong.lado_impacto = "" 
    def dibujar(pong, pantalla):
        pygame.draw.circle(pantalla, BLANCO, pong.pos, pong.radio)  
#Funcion Principal
def main():
    # Iniciamos PyGame
    pygame.init()
    
    # TamanoBarraes y etiqueta de la pantalla    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PONG Por Valerio Gomez") 
    pygame.display.set_icon(icono)
    

   # Se usa para establecer cuan rápido se actualiza la pantalla
    reloj = pygame.time.Clock()
    barra1 = Barra(1)    
    barra2 = Barra(2)
    bola = Pelota()

    sonido_pierdes = pygame.mixer.Sound("audio/pierdes.wav")
    sonido_inicio = pygame.mixer.Sound("audio/inicio.wav")

    pausa = True
    #declaramos la puntuacion de los jugadores donde la puntuacion de los jugadores 1 y 2 son puntuacion[0] y puntuacion[1] respectivamente
    puntuacion = [0, 0]
    #iniciamos el bucle 
    InicioJuego = True
    while InicioJuego:
        # establece los frames por segundo
        reloj.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                InicioJuego = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    InicioJuego = False

                elif pausa and event.key == pygame.K_SPACE:
                    pausa = False

                if event.key == pygame.K_w:
                    barra1.mover("arriba")
                elif event.key == pygame.K_s:
                    barra1.mover("abajo")

                if event.key == pygame.K_UP:
                    barra2.mover("arriba")
                elif event.key == pygame.K_DOWN:
                    barra2.mover("abajo")

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    barra1.mover("no")
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    barra2.mover("no")       
        barra1.actualizar()
        barra2.actualizar()

        if not pausa:
            bola.actualizar(barra1, barra2)            
            if bola.hayImpacto():                
                sonido_pierdes.play()
                reloj.tick(1)
                sonido_inicio.play()
                pausa = True                
                if bola.hayImpacto() == "izquierda":
                    puntuacion[1] += 1
                else:
                    puntuacion[0] += 1
                bola.reiniciar()
               # Barra.reiniciarPaleta()
        # pintamos la pantalla de ColorPantalla
        pantalla.fill(ColorPantalla) 
        
        # dibujar cancha
        pygame.draw.line(pantalla, BLANCO, (barra1.ancho(), 0), (barra1.ancho(), ALTO))
        pygame.draw.line(pantalla, BLANCO, (ANCHO - barra2.ancho(), 0), (ANCHO - barra2.ancho(),  ALTO))
        
        #Dibujamos la puntuacion
        pantalla.blit(texto("Jugador A = "+str(puntuacion[0]), 40, (255,0,0)), (ANCHO / 8+20, 10))
        pantalla.blit(texto("Jugador B = "+str(puntuacion[1]), 40, (0,0,255)), ((ANCHO * 3 / 4) - 100, 10))
        
        # dibujar barras                
        barra1.dibujar1(pantalla)
        barra2.dibujar2(pantalla)
        
        # dibujar Pelota
        bola.dibujar(pantalla)  

        if pausa:
            pantalla.blit(tecla,(ANCHO / 4+25, 400))
            pantalla.blit(fondo,(ANCHO/2-130,5))
            pygame.draw.line(pantalla, BLANCO, (ANCHO / 2, 0), (ANCHO / 2, ALTO),3) 
        pygame.display.flip()
if __name__ == "__main__":
    main()
    pygame.quit() 
    sys.exit()    
