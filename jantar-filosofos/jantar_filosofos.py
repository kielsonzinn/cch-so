import random
import threading
import time

import pygame

LARGURA, ALTURA = 600, 600
RAIO_MESA = 200
CENTRO_X, CENTRO_Y = LARGURA // 2, ALTURA // 2
RAIO_FILOSOFO = 40

BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jantar dos Filósofos")

NUM_FILOSOFOS = 5

garfos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

estados = ["Pensando"] * NUM_FILOSOFOS
mutex = threading.Lock()

angulos = [i * (360 / NUM_FILOSOFOS) for i in range(NUM_FILOSOFOS)]
posicoes = [
    (CENTRO_X + RAIO_MESA * pygame.math.Vector2(1, 0).rotate(angle)[0],
     CENTRO_Y + RAIO_MESA * pygame.math.Vector2(1, 0).rotate(angle)[1])
    for angle in angulos
]


def filosofo(index):
    global estados
    while True:
        with mutex:
            estados[index] = "Pensando"
        time.sleep(random.uniform(1, 3))

        with mutex:
            estados[index] = "Esperando"

        garfo_esquerda = garfos[index]
        garfo_direita = garfos[(index + 1) % NUM_FILOSOFOS]

        pegou_esquerda = garfo_esquerda.acquire(timeout=1)
        pegou_direita = garfo_direita.acquire(timeout=1) if pegou_esquerda else False

        if pegou_esquerda and pegou_direita:
            with mutex:
                estados[index] = "Comendo"
            time.sleep(random.uniform(2, 4))
            garfo_esquerda.release()
            garfo_direita.release()
        else:
            if pegou_esquerda:
                garfo_esquerda.release()
            if pegou_direita:
                garfo_direita.release()
            with mutex:
                estados[index] = "Pensando"


def main():
    for i in range(NUM_FILOSOFOS):
        threading.Thread(target=filosofo, args=(i,), daemon=True).start()

    rodando = True
    while rodando:
        tela.fill(BRANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        for i, (x, y) in enumerate(posicoes):
            with mutex:
                estado = estados[i]

            if estado == "Pensando":
                cor = AZUL
            elif estado == "Esperando":
                cor = AMARELO
            else:
                cor = VERDE

            pygame.draw.circle(tela, cor, (int(x), int(y)), RAIO_FILOSOFO)
            fonte = pygame.font.Font(None, 24)
            texto = fonte.render(f"{i + 1}", True, PRETO)
            tela.blit(texto, (int(x) - 10, int(y) - 10))

        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()


if __name__ == '__main__':
    main()
