import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import joblib

import nltk
# Загрузка стоп-слов для русского языка
nltk.download('stopwords')
from nltk.corpus import stopwords

russian_stopwords = stopwords.words('russian')


# 1. Загрузка данных
data = pd.read_csv('parsed_data.csv')

# 2. Определение целевой переменной и признаков
X = data.drop('Название', axis=1)  # Признаки
y = data['Описание']  # Целевая переменная

# 3. Кодирование целевой переменной
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# 4. Обработка текстовых колонок с проверкой на пустые значения
text_columns = X.select_dtypes(include=['object']).columns  # Текстовые колонки

vectorizer = TfidfVectorizer(max_features=100, stop_words=russian_stopwords)  # TF-IDF векторизация
for col in text_columns:
    # Заполнение пропусков и фильтрация пустых строк
    X[col] = X[col].fillna('').str.strip()  # Убираем пробелы и NaN

    # Исключаем колонки, где все строки пустые
    if X[col].str.len().sum() == 0:
        print(f"Пропуск колонки '{col}' из-за отсутствия данных.")
        X = X.drop(col, axis=1)
    else:
        try:
            X_tfidf = vectorizer.fit_transform(X[col]).toarray()
            X = X.drop(col, axis=1)
            X = pd.concat([X, pd.DataFrame(X_tfidf)], axis=1)
        except ValueError as e:
            print(f"Ошибка при обработке колонки '{col}': {e}")
            X = X.drop(col, axis=1)  # Удаляем проблемную колонку

# 5. Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Оценка модели
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# 8. Сохранение модели
joblib.dump(model, 'trained_model.pkl')
print("Модель сохранена в 'trained_model.pkl'")
