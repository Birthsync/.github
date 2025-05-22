import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# Загрузка данных
df = pd.read_csv('survey_data.csv', encoding='utf-8')

# Предобработка данных
df.columns = [col.strip() for col in df.columns]
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Визуализации
plt.figure(figsize=(15, 20))

# 1. Распределение оценок уникальности проекта
plt.subplot(4, 2, 1)
sns.countplot(data=df, x='Как вы оцениваете уникальность проекта по сравнению с аналогичными сервисами?')
plt.title('Оценка уникальности проекта')
plt.xticks(rotation=45)
plt.show()

# 2. Популярность функций
functions = df['Какие функции проекта кажутся вам наиболее полезными?  (выберите до 3 вариантов)'].str.split(', ')
all_functions = [item for sublist in functions.dropna() for item in sublist]
function_counts = Counter(all_functions)

plt.subplot(4, 2, 2)
pd.Series(function_counts).plot(kind='bar')
plt.title('Топ полезных функций')
plt.xticks(rotation=45)
plt.show()

# 3. Готовность платить
plt.subplot(4, 2, 3)
sns.countplot(data=df, x='Какую максимальную сумму вы готовы платить ежемесячно за такой сервис?')
plt.title('Максимальная ежемесячная плата')
plt.xticks(rotation=45)
plt.show()

# 4. Отношение к рекламе
plt.subplot(4, 2, 4)
sns.countplot(data=df, x='Насколько вас раздражает реклама в бесплатной версии приложений?')
plt.title('Восприятие рекламы')
plt.xticks(rotation=45)
plt.show()

# 5. Риски
risks = df['Какие риски вы видите в использовании такого приложения?  (выберите до 2 вариантов)'].str.split(', ')
all_risks = [item for sublist in risks.dropna() for item in sublist]
risk_counts = Counter(all_risks)
plt.show()

plt.subplot(4, 2, 5)
pd.Series(risk_counts).plot(kind='bar')
plt.title('Основные риски')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('analysis_plots.png')
plt.close()

# Текстовый анализ открытых вопросов
def clean_text(text):
    return re.sub(r'[^\w\s]', '', str(text).lower())

improvements = ' '.join(df['Что бы вы добавили в приложение для повышения удобства? (открытый вопрос)'].apply(clean_text))
negative = ' '.join(df['Что вам не нравится в текущей концепции приложения? (открытый вопрос)'].apply(clean_text))

# Генерация отчета
report = f"""
Аналитический отчет по результатам опроса:

1. Уникальность проекта:
- {df['Как вы оцениваете уникальность проекта по сравнению с аналогичными сервисами?'].value_counts().to_string()}

2. Топ-3 востребованных функций:
{pd.Series(function_counts).nlargest(3).to_string()}

3. Монетизация:
- Предпочтительные модели оплаты: {df['Какая модель оплаты для вас предпочтительнее?'].value_counts().to_string()}
- Средняя готовность платить: {df['Какую максимальную сумму вы готовы платить ежемесячно за такой сервис?'].mode()[0]}

4. Основные риски:
{risk_counts}

5. Рекомендации:
- Упростить интерфейс (упоминалось {negative.count('интерфейс')} раз)
- Улучшить систему подбора подарков (упоминалось {improvements.count('подбор')} раз)
- Ввести гибкую систему подписок с пробным периодом
- Обеспечить прозрачность использования данных

Текстовые предложения:
- Частые запросы: {Counter(improvements.split()).most_common(5)}
- Основные жалобы: {Counter(negative.split()).most_common(5)}
"""

print(report)