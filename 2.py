import os
import pandas as pd

DIRECTORY= 'anonymized'

df = pd.read_csv(os.path.join(DIRECTORY, 'А.Макрелева.csv'), sep=';')

print('\nРазмер таблицы:', df.shape)

print('\nТипы данных:')
print(df.dtypes)

print('\nПервые 3 строки:')
print(df.head(3))

missing = df.isna().sum().sort_values(ascending=False)
print('\nПропуски по колонкам:')
print(missing[missing > 0])

print('\nУникальных областей лица:', df['Image context'].nunique())
print(df['Image context'].unique())

print('\nУникальных дат:', df['Отметка времени'].nunique())



na_before = df.isna().sum().sum()

text_cols = ['Image context', 'Изображение', 'Отметка времени',
             'Поры - Pore Type', 'Выбор.3', 'Выбор.4', 'Выбор.5',
             'Канал.3', 'Канал.4', 'Канал.5']

for col in df.columns:
    if col not in text_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'),
                                errors='coerce')

na_after = df.isna().sum().sum()
print(f'\nПропусков было: {na_before}, стало: {na_after} '
      f'(новых NaN: {na_after - na_before} — это мусор вида "--")')

df = df[df['Поры - Pore Type'] == 'All Pores']
print('Строк после фильтра All Pores:', len(df))

months_ru = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
             'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
             'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}


def parse_ru_date(s):
    parts = str(s).split()
    day = int(parts[0])
    month = months_ru[parts[1]]
    year = int(parts[2])
    time = parts[4]
    return pd.Timestamp(f'{year}-{month:02d}-{day:02d} {time}')


df['date'] = df['Отметка времени'].apply(parse_ru_date)

print('\nУникальных календарных дат:', df['date'].dt.date.nunique())
print(df['date'].dt.date.unique())



df['region'] = df['Image context'].str.split(' - ', n=1).str[1]

print('\nУникальных region:', df['region'].nunique())
print(df['region'].value_counts())


def simplify_region(r):
    """Левая/правая щека -> Щека, лоб любой стороны -> Лоб и т.д."""
    r = r.lower()
    if 'гусин' in r:
        return 'Гусиные лапки'
    elif 'щека' in r:
        return 'Щека'
    elif 'скула' in r:
        return 'Скула'
    elif 'носогуб' in r:
        return 'Носогубная складка'
    elif 'лоб' in r or 'лба' in r:
        return 'Лоб'
    return r


df['region_big'] = df['region'].apply(simplify_region)
print('\nСтрок в каждой укрупнённой области:')
print(df['region_big'].value_counts())



min_date = df['date'].min().normalize()

df['stage'] = (df['date'].dt.normalize() != min_date).astype(int)

print('\nСтрок с stage=0 (До) и stage=1 (После):')
print(df['stage'].value_counts())



def load_patient(filepath):
    d = pd.read_csv(filepath, sep=';')

    for col in d.columns:
        if col not in text_cols:
            d[col] = pd.to_numeric(d[col].astype(str).str.replace(',', '.'),
                                   errors='coerce')

    d = d[d['Поры - Pore Type'] == 'All Pores']

    d['date'] = d['Отметка времени'].apply(parse_ru_date)

    d['region'] = d['Image context'].str.split(' - ', n=1).str[1]
    d['region_big'] = d['region'].apply(simplify_region)

    d['stage'] = (d['date'].dt.normalize() != d['date'].min().normalize()).astype(int)

    d['patient'] = os.path.basename(filepath)[:-4]
    return d


all_dfs = []
for filename in sorted(os.listdir(DIRECTORY)):
    if not filename.endswith('.csv'):   # пропускаем не-csv файлы
        continue
    all_dfs.append(load_patient(os.path.join(DIRECTORY, filename)))

big = pd.concat(all_dfs, ignore_index=True)
print('\nПациентов:', big['patient'].nunique())
print('Всего строк:', len(big))

print('\nКоличество укрупнённых областей у каждого пациента:')
print(big.groupby('patient')['region_big'].nunique())
print('\nСколько пациентов имеет данные по каждой области:')
print(big.groupby('region_big')['patient'].nunique())



means = big.groupby(['patient', 'region_big', 'stage'])['Поры - Количество'] \
           .mean().reset_index()

piv = means.pivot_table(index=['patient', 'region_big'],
                        columns='stage', values='Поры - Количество')
for c in (0, 1):
    if c not in piv.columns:
        piv[c] = float('nan')
piv = piv[[0, 1]]
piv.columns = ['before', 'after']

stats = piv.groupby('region_big').agg(
    mean_before=('before', 'mean'),
    median_before=('before', 'median'),
    std_before=('before', 'std'),
    mean_after=('after', 'mean'),
    median_after=('after', 'median'),
    std_after=('after', 'std'),
)

stats['diff'] = stats['mean_after'] - stats['mean_before']
print('\n', stats.sort_values('diff'))



indicators = ['Поры - Количество',
              'Тонкие морщины - Итоговое число',
              'Тонкие морщины - Средняя глубина [mm]']

rows = []   # сюда собираем результат
for ind in indicators:
    # Среднее по замерам каждого пациента
    m = big.groupby(['patient', 'region_big', 'stage'])[ind].mean().reset_index()
    # "До" и "После" рядом
    p = m.pivot_table(index=['patient', 'region_big'],
                      columns='stage', values=ind)
    for c in (0, 1):
        if c not in p.columns:
            p[c] = float('nan')
    p = p[[0, 1]]
    p.columns = ['before', 'after']
    # Одна строка на (показатель, область)
    for region, g in p.groupby('region_big'):
        rows.append({
            'indicator': ind,
            'region': region,
            'n_patients': g['before'].notna().sum(),  # у скольких есть данные
            'mean_before': g['before'].mean(),
            'mean_after': g['after'].mean(),
            'diff': g['after'].mean() - g['before'].mean(),
        })

summary = pd.DataFrame(rows)
print('\n', summary.sort_values(['indicator', 'diff']).to_string())




print('\n' + '=' * 70)
print('ЗАДАНИЕ 8. Динамика по пациентам: Поры - Количество')
print('=' * 70)

# ШАГ 1: разность После - До для каждого пациента и области
piv['diff'] = piv['after'] - piv['before']

# ШАГ 2-3: считаем положительные (показатель вырос),
# отрицательные (снизился — желаемый эффект) и нулевые разности
result = piv.groupby('region_big')['diff'].agg(
    n_positive=lambda x: (x > 0).sum(),
    n_negative=lambda x: (x < 0).sum(),
    n_zero=lambda x: (x == 0).sum(),
).reset_index()
print('\n', result.to_string())



print('\n' + '=' * 70)
print('ЗАДАНИЕ 9. Визуализация')
print('=' * 70)

# 1. Boxplot «До vs После» по областям
big.boxplot(column='Поры - Количество', by=['region_big', 'stage'],
            figsize=(12, 6), rot=45)

# 2. Bar chart средних «До» и «После» по областям
stats[['mean_before', 'mean_after']].plot.bar(figsize=(10, 5),
                                              title='Поры - Количество: До vs После')

# 3. Гистограмма разностей для Щеки (одно число на пациента)
cheek_diff = piv.xs('Щека', level='region_big')['diff']
cheek_diff.plot.hist(bins=10, title='Разность После-До: Щека')

# ============================================================================
# ЗАДАНИЕ 10. Сравнение левой и правой стороны
# ============================================================================
print('\n' + '=' * 70)
print('ЗАДАНИЕ 10. Симметрия левой/правой стороны')
print('=' * 70)

# ШАГ 1: среднее по замерам для левой и правой щеки
cheeks = big[big['region'].isin(['Левая щека', 'Правая щека'])]
cm = cheeks.groupby(['patient', 'region'])['Поры - Количество'].mean().unstack()

# ШАГ 2: пациенты с разницей между сторонами > 20%
cm['diff_pct'] = ((cm['Правая щека'] - cm['Левая щека']).abs()
                  / cm['Левая щека'] * 100)
print('\nПациенты с разницей > 20% (щёки):')
print(cm[cm['diff_pct'] > 20])

# ШАГ 3: scatter "слева vs справа" — точки у диагонали = стороны симметричны
cm.plot(kind='scatter', x='Левая щека', y='Правая щека',
        title='Симметрия: левая vs правая щека')

# То же для скулы и носогубной складки
for left, right in [('Левая скула', 'Правая скула'),
                    ('Левая носогубная складка', 'Правая носогубная складка')]:
    side = big[big['region'].isin([left, right])]
    sm = side.groupby(['patient', 'region'])['Поры - Количество'].mean().unstack()
    sm['diff_pct'] = ((sm[right] - sm[left]).abs() / sm[left] * 100)
    print(f'\nПациенты с разницей > 20% ({left}):')
    print(sm[sm['diff_pct'] > 20])
    sm.plot(kind='scatter', x=left, y=right,
            title=f'Симметрия: {left} vs {right}')

# ============================================================================
# ЗАДАНИЕ 11. Поиск аномалий (метод IQR)
# ============================================================================
print('\n' + '=' * 70)
print('ЗАДАНИЕ 11. Поиск аномалий: Тонкие морщины - Итоговое число')
print('=' * 70)

col = 'Тонкие морщины - Итоговое число'

# ШАГ 1: границы нормы по всем данным (метод 1.5*IQR)
q1 = big[col].quantile(0.25)   # первый квартиль (25%)
q3 = big[col].quantile(0.75)   # третий квартиль (75%)
iqr = q3 - q1                  # межквартильный размах
lower = q1 - 1.5 * iqr         # нижняя граница
upper = q3 + 1.5 * iqr         # верхняя граница
print(f'\nГраницы нормы: [{lower:.2f}; {upper:.2f}]')

# ШАГ 2: отбираем выбросы
outliers = big[(big[col] < lower) | (big[col] > upper)]
print('Количество выбросов:', len(outliers))
print(outliers[['patient', 'region_big', 'stage', col]].to_string())

# ============================================================================
# ЗАДАНИЕ 12. Финальный отчёт
# ============================================================================
print('\n' + '=' * 70)
print('ЗАДАНИЕ 12. Структура финального отчёта')
print('=' * 70)
print("""
1. Введение         — прибор анализа кожи, 22 пациента, замеры До/После
2. Загрузка/очистка — функция load_patient() (задания 1-5)
3. Описат. статистика — таблицы из заданий 6-7
4. Визуализация     — графики из задания 9
5. Выводы           — задания 8, 10, 11: где эффект сильнее,
                      симметричны ли области, есть ли выбросы
""")

# Сохраняем главные таблицы в Excel для отчёта
with pd.ExcelWriter('report_tables.xlsx') as w:
    stats.to_excel(w, sheet_name='stats_pores')
    summary.to_excel(w, sheet_name='summary_3x4', index=False)
    result.to_excel(w, sheet_name='dynamics', index=False)
    outliers[['patient', 'region_big', 'stage', col]].to_excel(
        w, sheet_name='outliers', index=False)
print('Таблицы сохранены в report_tables.xlsx')