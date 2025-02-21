import queue
import random
import threading
import time

import pygame

LARGURA, ALTURA = 400, 200
TAMANHO_ITEM = 50
ESPACO_ENTRE_ITENS = 10
POSICAO_Y = ALTURA // 2

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

BUFFER_MAX = 5
buffer = queue.Queue(maxsize=BUFFER_MAX)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Produtor/Consumidor")


def produtor():
    while True:
        item_produzido = random.randint(1, 100)
        buffer.put(item_produzido)
        print(f"Produzido: {item_produzido}")
        time.sleep(random.uniform(0.5, 2))


def consumidor():
    while True:
        item_consumido = buffer.get()
        print(f"\tConsumido: {item_consumido}")
        time.sleep(random.uniform(1, 3))
        buffer.task_done()


if __name__ == '__main__':
    threading.Thread(target=produtor, daemon=True).start()
    threading.Thread(target=consumidor, daemon=True).start()

    rodando = True
    while rodando:
        tela.fill(BRANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        itens = list(buffer.queue)
        x_pos = 50

        for item in itens:
            pygame.draw.rect(tela, AZUL, (x_pos, POSICAO_Y, TAMANHO_ITEM, TAMANHO_ITEM))
            fonte = pygame.font.Font(None, 30)
            texto = fonte.render(str(item), True, BRANCO)
            tela.blit(texto, (x_pos + 10, POSICAO_Y + 10))
            x_pos += TAMANHO_ITEM + ESPACO_ENTRE_ITENS

        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()

if __name__ == '__main__':
    main()
