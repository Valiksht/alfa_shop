# API для Интернет-магазина

## Описание функционала

Данное приложение представляет собой API для интернет-магазина, позволяющее управлять следующими сущностями:

- **Категории товаров:** Главное представление категорий для группировки продуктов.
- **Подкатегории:** Более детальное разделение внутри категорий, позволяющее лучше организовать товары.
- **Товары:** Полная информация о продуктах, включая свзи с подкатегориями.
- **Корзина:** Возможность добавления, удаления товаров и расчёт общего количества и стоимости товаров в корзине.

### Основные функции

1. **Управление категориями:**
   - CRUD операции для главных категорий товаров.

2. **Управление подкатегориями:**
   - CRUD операции для подкатегорий с фильтрацией по категории.

3. **Управление товарами:**
   - CRUD операции для товаров с фильтрацией по подкатегории.
   - Взаимодействие с корзиной для добавления и удаления товаров.

4. **Корзина:**
   - Возможность добавления товаров в корзину and управления их количеством.
   - Получение общей информации о корзине, включая количество товаров и общую стоимость.

## Установка и запуск приложения локально

### Предварительные требования

- Python версии 3.8 или выше
- Django версии 3.x
- Django REST Framework версии 3.x
- djoser для аутентификации
- drf-yasg для генерации документации Swagger

### Шаги по установке

1. **Клонируйте репозиторий:**
   ```bash
   git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
   cd <ВАША_ПАПКА_С_ПРОЕКТОМ>

2. **Создайте и активируйте виртуальное окружение:**

#### Для Windows:
bash

Copy
python -m venv venv
.\venv\Scripts\activate

#### Для MacOS/Linux:
bash

Copy
python3 -m venv venv
source venv/bin/activate

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt

4. **Создайте базу данных:**
   ```bash
   python manage.py migrate

5. **Запустите сервер:**
   ```bash
   python manage.py runserver

6. **Откройте в браузере:** http://127.0.0.1:8000/swagger/

## Документация

Документация доступна по адресу http://127.0.0.1:8000/swagger/.

## Тестирование

Для запуска тестов используйте команду перейдите в репозиторий 
**test_alfa/alfa_shop** и выполните следующую команду:

```bash
pytest
```

## Примеры запросов:

### Получение списка категорий

```bash
GET http://127.0.0.1:8000/api/mcateg
```

### Создание категории

```bash
POST http://127.0.0.1:8000/api/mcateg/
Content-Type: application/json

{
  "name": "Игрушки2",
  "slug": "tiys",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
}
```
### Создание подкатегории

```bash
POST http://127.0.0.1:8000/api/mcateg/2/lcateg/
Content-Type: application/json

{
  "name": "Машинки2",
  "slug": "cars",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
}
```

### Создание товара

```bash
POST http://127.0.0.1:8000/api/mcateg/1/lcateg/1/prodacts/
Content-Type: application/json

{
  "name": "Машинка",
  "slug": "car",
  "price": 15,
  "images": [
    {
      "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
    },
    {
      "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
    },
    {
      "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
    }
  ]
}
```
### Добавления товара в корзину

```bash
POST http://127.0.0.1:8000/api/mcateg/1/lcateg/1/prodacts/1/shop_basket/
Content-Type: application/json

```

