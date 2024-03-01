import pygame
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Тест на устойчивость внимания")

# Цвета и шрифты
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 36)

# Текст инструкции
instructions = [
    "Нажмите '<-' для четных чисел, '->' для нечетных.",
    "Нажмите 'Пробел', чтобы начать."
]

# Показать начальный экран
def show_start_screen():
    screen.fill(BLACK)
    for i, line in enumerate(instructions):
        text = font_small.render(line, True, WHITE)
        screen.blit(text, (200, 150 + 30 * i))
    pygame.display.flip()

# Функция для отображения цифры
def show_number(number):
    screen.fill(BLACK)
    text = font.render(str(number), True, WHITE)
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()

# Начальный экран
show_start_screen()
start_test = False

# Ожидание начала теста
while not start_test:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_test = True

# Основной цикл теста
reaction_times = []
timestamps = []
errors = 0
test_duration = 60
start_time = time.time()
previous_number = None
error_count = []
current_errors = 0

while time.time() - start_time < test_duration:
    number = random.choice([n for n in range(10) if n != previous_number])
    show_number(number)

    correct_key = pygame.K_LEFT if number % 2 == 0 else pygame.K_RIGHT
    stimulus_start_time = time.time()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                reaction_time = time.time() - stimulus_start_time
                reaction_times.append(reaction_time)
                timestamps.append(time.time() - start_time)

                if event.key != correct_key:
                    errors += 1
                    current_errors += 1

                waiting_for_input = False
                previous_number = number

    if len(reaction_times) % 15 == 0 and len(reaction_times) != 0:
        error_count.append((len(reaction_times) // 15, current_errors))
        current_errors = 0

# Расчет устойчивости внимания
num_stimuli = len(reaction_times)
average_time = sum(reaction_times) / num_stimuli
time_variance = sum([abs(time - average_time) for time in reaction_times]) / average_time
stability = (num_stimuli / (num_stimuli - errors)) * time_variance

# Построение графиков
plt.figure(figsize=(10, 5))

# График времени реакции
plt.subplot(1, 2, 1)
plt.scatter(timestamps, reaction_times, alpha=0.5, label="Время реакции")
z = np.polyfit(timestamps, reaction_times, 1)
p = np.poly1d(z)
plt.plot(timestamps, p(timestamps), "r--", label="Аппроксимация")
plt.xlabel('Время (сек)')
plt.ylabel('Время реакции (сек)')
plt.title('Зависимость времени реакции от времени прохождения')
plt.legend()

# График ошибок
plt.subplot(1, 2, 2)
x, y = zip(*error_count)
plt.scatter(x, y, alpha=0.5, label="Ошибки")
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--", label="Аппроксимация")
plt.xlabel('Блок ответов (каждые 15)')
plt.ylabel('Ошибки')
plt.title('Ошибки на каждые 15 ответов')
plt.legend()

plt.tight_layout()
plt.show()

# Вывод результатов
pygame.quit()
print(f"Число повторений: {num_stimuli}")
print(f"Среднее время реакции: {average_time:.4f} сек.")
print(f"Разброс времени реакции: {time_variance:.4f}")
print(f"Устойчивость внимания: {stability:.4f}")
