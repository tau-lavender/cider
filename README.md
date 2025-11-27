# Cider: Введение
[![python](https://img.shields.io/badge/Python-3.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

<img src="cider.png" alt="drawing" width="100"/>


Self-Deploy: standalone скрипт для Jenkins CI/CD пайплайнов для создания пайплайнов для репозитория проекта на основе шаблонов. Языки программирования и фреймворки в проекте автоматически определяются, и в соответствии со стеком выбираются шаблоны.

---
# Поддерживаемые языки и фреймворки

### Python

Доступные фреймворки:
- FastAPI
- Django
- Pytest

### TypeScript


### Go


### Java


---
# Запуск скрипта
## Требования для запуска проекта
- python >=3.14
- uv

## Запуск c uv
```bash
uv venv
uv sync

uv run python -m src.main <ссылка на git-репозиторий> --dir <путь до папки>
```
## Запуск c requirements.txt
```bash
pip install -r /path/to/requirements.txt

python -m src.main <ссылка на git-репозиторий> --dir <путь до папки>
```

- Скрипт клонирует репозиторий, анализирует его, собирает и рендерит конечный целый Jenkins файл.
- Параметр `--dir` опциональный - если требуется клонировать репозиторий в определенный путь, иначе клонирует в рабочую директорию

# Пример

# Главная структура
<pre>
    .
    ├── src/
    │   ├── languages/                  # Модули и конфиги поддерживаемых языков с фреймворками
    │   │   ├── python/   
    │   │   ├── java_kotlin/  
    │   │   ├── js_ts/  
    │   │   ├── go/
    │   ├── main.py                     # Точка запуска
    │   ├── analyzer.py                 # Все анализаторы, включая основной (main).
    │   ├── default_class.py            # ?
    │   ├── render.py                   # Точка рендера файла
    │   ├── singleton.py                # ?
</pre>