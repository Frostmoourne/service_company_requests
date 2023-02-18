import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

from .models import ServiceRequest


class RequestService:
    @staticmethod
    def prepare_data():
        # Подготавливаем данные на основе всех заявок
        requests = ServiceRequest.objects.all()
        request_data = []
        for request in requests:
            request_data.append([request.request_type, request.status, request.urgency, request.request_date,
                                 request.request_origin, request.customer_type, request.due_date])
        request_data = pd.DataFrame(request_data, columns=['request_type', 'status', 'urgency', 'request_date',
                                                           'request_origin', 'customer_type', 'due_date'])
        X = request_data.drop('urgency', axis=1)
        y = request_data['urgency']

        # Разделим данные на обучающий и тестовый наборы
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Обучаем модель
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Оценка модели
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy: ", accuracy)

        # Сохраняем полученную модель в файл для дальнейшей оценки поступающих заявок
        with open('request_prioritization_model.pkl', 'wb') as f:
            pickle.dump(model, f)

        request_data.to_csv('training_data.csv')

        return X

    @staticmethod
    def get_urgency(service_request):
        priority_to_urgent = {
            '3': 'high',
            '2': 'medium',
            '1': 'low'
        }

        df = pd.read_csv('training_data.csv')
        # Отбрасываем ненужные поля заявки
        df = df.drop(columns=['request_details', 'id', 'number', 'customer'])

        # Очищаем и заполняем пустые поля
        df = df.dropna()
        df = df.fillna(df.mean())
        # Преобразование категориальных переменных в числовые переменные
        df = pd.get_dummies(df, columns=['request_type', 'status', 'request_date',
                                         'request_origin', 'customer_type', 'due_date'])

        X = df.drop('urgency', axis=1)

        # Загружаем обученую модель из файла
        with open("request_prioritization_model.pkl", "rb") as file:
            model = pickle.load(file)

        # Делаем датафрейм на основе запроса на создание заявки
        request_df = pd.DataFrame(service_request, index=[0])

        # Чтобы избежать ошибки несовпадения колонок в созданом дата фрейме и заявке выбираем только валидные значения
        missing_cols = set(X.columns) - set(request_df.columns)
        for col in missing_cols:
            request_df[col] = 0
        request_df = request_df[X.columns]

        # Прогнозирование приоритета с помощью обученной модели
        priority = model.predict(request_df)

        # Возвращаем полученый приоритет заявки
        return priority_to_urgent[str(priority)]
