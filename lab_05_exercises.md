{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "cell-000",
   "metadata": {},
   "source": [
    "# Лабораторная работа 05. Scikit-learn: первая модель оценки цены\n",
    "\n",
    "**Курс:** «Анализ данных и искусственный интеллект», 1 курс бакалавриата.\n",
    "\n",
    "Мы уже подготовили и изучили данные об автомобилях. Теперь хотим по характеристикам автомобиля получить оценку цены. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-001",
   "metadata": {},
   "source": [
    "## 1. Что именно мы просим модель сделать\n",
    "\n",
    "Один объект — автомобиль в одной строке. Его признаки — год выпуска, пробег, объём двигателя и условный среднегодовой пробег. Правильный ответ для обучения — указанная цена\n",
    "\n",
    "| Термин | В нашей задаче |\n",
    "|---|---|\n",
    "| Объект | Одна строка с автомобилем |\n",
    "| Признаки | Известные характеристики автомобиля |\n",
    "| Целевая переменная | Цена `Price` |\n",
    "| Обучение | Настройка модели по признакам и известным ценам |\n",
    "| Предсказание | Получение оценки цены по признакам |\n",
    "| Регрессия | Предсказание численного значения |\n",
    "\n",
    "Обученная модель не узнаёт состояние машины и фактическую цену сделки. Она ищет закономерности в доступных признаках и ценах предложений.\n",
    "\n",
    "**Упражнение 1.1:** какая колонка здесь является ответом? Можно ли передать её модели как входной признак при оценке неизвестной цены?\n",
    "*Ваш ответ:* "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-002",
   "metadata": {},
   "source": [
    "### Подключаем библиотеки\n",
    "\n",
    "`import` подключает библиотеку. Через `from ... import ...` берём конкретный инструмент. Пока подключаем только работу с таблицами, графиками и разделение данных.\n",
    "\n",
    "Установка при необходимости: `pip install pandas numpy matplotlib scikit-learn joblib`. После установки перезапустите ядро. Установочный пакет называется `scikit-learn`, а импорт — `sklearn`.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Версия scikit-learn: 1.7.2\n"
     ]
    }
   ],
   "source": [
    "from pathlib import Path\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from IPython.display import display\n",
    "from sklearn.model_selection import train_test_split\n",
    "import sklearn\n",
    "\n",
    "print('Версия scikit-learn:', sklearn.__version__)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-004",
   "metadata": {},
   "source": [
    "Появился номер версии. Модель пока не создана и не обучена.\n",
    "\n",
    "**Упражнение 1.2:** чем подключение библиотеки отличается от обучения модели?\n",
    "*Ваш ответ:* "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-005",
   "metadata": {},
   "source": [
    "### Загружаем результат лабораторной 02\n",
    "\n",
    "Используем `cars_processed.csv`, а не таблицу со средними ценами групп. Положите файл рядом с ноутбуком; без локального файла используется пример из репозитория курса. Код проверяет наличие пропусков и недопустимых для примера значений, но не выполняет новую скрытую очистку.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "data_path = Path('cars_processed.csv')\n",
    "if data_path.exists():\n",
    "    df = pd.read_csv(data_path)\n",
    "else:\n",
    "    df = pd.read_csv(\n",
    "        'https://raw.githubusercontent.com/MVRonkin/BasicDataAnalysisCourse/'\n",
    "        'refs/heads/main/Workshops/cars_processed.csv'\n",
    "    )\n",
    "df = df.rename(columns={'Price(euro)': 'Price', 'Engine_capacity(cm3)': 'Engine'})\n",
    "df = df.drop(columns=[c for c in df.columns if c.startswith('Unnamed:')])\n",
    "df = df.reset_index(drop=True)\n",
    "NUMERIC_FEATURES = ['Year', 'Distance', 'Engine', 'km_year']\n",
    "if df[NUMERIC_FEATURES + ['Price']].isna().any().any():\n",
    "    raise ValueError('В выбранных колонках есть пропуски: вернитесь к подготовке данных.')\n",
    "if not np.isfinite(df[NUMERIC_FEATURES + ['Price']].to_numpy()).all():\n",
    "    raise ValueError('В выбранных колонках есть бесконечные значения.')\n",
    "if not (df['Price'] > 0).all():\n",
    "    raise ValueError('Для этого учебного примера нужны положительные цены.')\n",
    "df.head(3)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-008",
   "metadata": {},
   "source": [
    "## 2. X — вопросы модели, y — известные ответы\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-009",
   "metadata": {},
   "source": [
    "### Выбираем входы и ответ\n",
    "\n",
    "`X` — таблица с несколькими колонками. `y` — Series с одной ценой для каждой строки. Их индексы должны совпадать.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = df[NUMERIC_FEATURES].copy()\n",
    "y = df['Price'].copy()\n",
    "\n",
    "display(X.head(3))\n",
    "display(y.head(3))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-011",
   "metadata": {},
   "source": [
    "В `X` нет колонки `Price`. В `y` нет признаков. Строка с тем же индексом относится к тому же автомобилю.\n",
    "\n",
    "**Упражнение 2.1:** где находится цена автомобиля с индексом 0?\n",
    "*Ваш ответ:* "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-012",
   "metadata": {},
   "source": [
    "### Проверяем размеры\n",
    "\n",
    "Для `X` форма `(n, p)` означает n объектов и p признаков. Для `y` форма `(n,)` означает n ответов.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "print('X:', X.shape)\n",
    "print('y:', y.shape)\n",
    "print('Индексы совпадают:', X.index.equals(y.index))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-016",
   "metadata": {},
   "source": [
    "## 3. Учим на одной части, проверяем на другой\n",
    "\n",
    "Если модель увидела цену во время обучения, удачное предсказание этой же цены ещё не показывает качество на новой записи. Поэтому выделим три непересекающиеся части:\n",
    "\n",
    "| Часть | Примерная доля | Для чего используется |\n",
    "|---|---:|---|\n",
    "| `train/validation` | 60% | Обучение моделей |\n",
    "| `test` | 40% | Итоговая проверка |\n",
    "\n",
    "В этой работе **тестовые метрики не считаем**. Учимся читать результаты на валидации. Повторный подбор по валидации возможен, но чем больше вариантов проверено, тем больше риск подстроиться под неё.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-017",
   "metadata": {},
   "source": [
    "### Первое разделение\n",
    "\n",
    "`train_test_split` принимает `X` и `y` вместе и сохраняет соответствие строк. `test_size=0.4` означает 40% во временную отложенную часть. Остальные 60% идут в обучение.\n",
    "\n",
    "Имена четырёх результатов задаём слева: признаки обучения, признаки отложенной части, ответы обучения, ответы отложенной части. `random_state=42` фиксирует случайный выбор; число 42 не улучшает качество.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, y_train, y_test = train_test_split(\n",
    "    X, y, test_size=0.4, random_state=42\n",
    ")\n",
    "print('Обучение:', X_train.shape, y_train.shape)\n",
    "print('Отложенная часть:', X_test.shape, y_test.shape)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-020",
   "metadata": {},
   "source": [
    "### Второе разделение (Практикум)\n",
    "\n",
    "**Упражнение 3.1:** Раскомментируйте и выполните код ниже, чтобы разбить обучающую выборку ещё пополам на обучающую и валидационную части. Посчитайте общую сумму объектов и сравните с исходной размерностью `X`.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Напишите код второго разделения здесь:\n",
    "# X_valid, X_train, y_valid, y_train = train_test_split(\n",
    "#     X_train, y_train, test_size=0.5, random_state=43\n",
    "# )\n",
    "# split_sizes = pd.Series({'train': len(X_train), 'valid': len(X_valid), 'test': len(X_test)})\n",
    "# display(split_sizes.to_frame('Число объектов'))\n",
    "# print('Частей в сумме:', split_sizes.sum(), 'Исходных строк:', len(X))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-023",
   "metadata": {},
   "source": [
    "### Проверяем отсутствие пересечения\n",
    "\n",
    "Посмотрим на индексы строк. `intersection` возвращает общие метки. Для непересекающихся частей число общих меток равно нулю.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "print('train ∩ test:', len(X_train.index.intersection(X_test.index)))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-026",
   "metadata": {},
   "source": [
    "## 4. До сложной модели: один ответ для всех автомобилей\n",
    "\n",
    "Начнём с ориентира: всем автомобилям предсказываем медиану цены **обучающей части**. Такой прогноз не учитывает признаки. Он нужен, чтобы понять, даёт ли модель пользу по сравнению с очень простым решением.\n",
    "\n",
    "`DummyRegressor` — модель-ориентир в scikit-learn. `strategy='median'` выбирает медиану. \n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cell-027",
   "metadata": {},
   "source": [
    "### Создаём модель-ориентир\n",
    "\n",
    "Первая строка импортирует класс. Вторая создаёт объект с выбранным параметром. Создание объекта ещё не использует данные.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.dummy import DummyRegressor\n",
    "\n",
    "dummy_model = DummyRegressor(strategy='median')\n",
    "dummy_model\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}