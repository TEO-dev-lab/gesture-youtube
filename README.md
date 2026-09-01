# Gesture YouTube

Управление YouTube Shorts жестами правой руки через веб-камеру.
Работает на **Linux** и **Windows**. ОС определяется автоматически.

## Жесты

- Свайп влево → следующее видео (клавиша Down)
- Свайп вправо → предыдущее видео (клавиша Up)
- Для выхода нажмите `q`

## Установка

1. Скачайте репозиторий и распакуйте в любое удобное место.
2. Откройте консоль в папке проекта и выполните команды:

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate

# системная зависимость для эмуляции нажатий клавиш
# (Arch/Manjaro:)
sudo pacman -S xdotool
# (Debian/Ubuntu:)
# sudo apt install xdotool

pip install -r requirements.txt
```

### Windows

```pwsh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> На Windows ничего дополнительно ставить не нужно — нажатия имитируются через `pyautogui`.

## Запуск

```bash
python main.py
```

Программа сама определит операционную систему и выберет нужный модуль нажатий:
автоматически. Используйте **правую руку**.

## Структура

| Файл | Назначение |
|---|---|
| `main.py` | Точка входа |
| `key_simulator.py` | Автовыбор нажатий: `xdotool` (Linux) / `pyautogui` (Windows) |
| `gesture_detector.py` | Детекция руки и свайпов через MediaPipe |
| `config.py` | Настройки (порог чувствительности, камера и т.д.) |
| `requirements.txt` | Общие зависимости для обеих ОС |