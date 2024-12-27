# Electronic-retail-chain

Онлайн-платформа для работы с компаниями

### Описание задачи:

Разработка API-приложения с возможностью создания компаний,
просмотром их контактов и поставщиков, а также отслеживанием задолженостей
Для реализации проекта применяется Django Rest Framework (DRF).

### Функционал API:

1. **Управление компаниями**:
    - Создание, редактирование и удаление компаний.
    - Получение списка всех компаний.
    - Поиск компаний по различным критериям (название, поставщик, тип и т.д.).
    - При создании компании через API запрещено обновлять поле задолженость
      (рассмотрено два варианта):
      * Создание 2х сериализаторов, на которые прописаны разные права доступа:
   ```python
   class CompanyAllFieldsSerializer(serializers.ModelSerializer):
    company_products = ProductSerializer(many=True, read_only=True)

    class Meta:
       model = Company
       exclude = ("debt", "debt_currency"),
   ```
   ```python
   class CompanySerializer(serializers.ModelSerializer):
    company_products = ProductSerializer(many=True, read_only=True)

    class Meta:
       model = Company
       fields = "__all__"
   ```
   * * Переопределение методов создания и обновления в файле `/retail_chain/views.py/`:

      ```python
          def create(self, request, *args, **kwargs):
           """Метод , запрещяющий добавлять через АПИ задолженость"""
           serializer = self.get_serializer(data=request.data)
           if (
               request.data.get("debt") is None
               and request.data.get("debt_currency") is None
           ):
               serializer.is_valid(raise_exception=True)
               self.perform_create(serializer)
               return Response(serializer.data, status=status.HTTP_201_CREATED)
           data = {"error": f"Ошибка с кодом 403. Вы не можете указывать задолженность"}
           return JsonResponse(
               data["error"],
               safe=False,
               status=status.HTTP_400_BAD_REQUEST,
               json_dumps_params={"ensure_ascii": False},
           )
      ```
      ```python
          def perform_update(self, serializer):
           """Метод , запрещяющий обновлять через АПИ задолженость"""
           if self.request.data.get("debt"):
               data = {"error": f"Ошибка с кодом 403. Вы не можете менять задолженность"}
               return JsonResponse(
                   data["error"],
                   safe=False,
                   status=status.HTTP_400_BAD_REQUEST,
                   json_dumps_params={"ensure_ascii": False},
               )
           serializer.save()
           Response(serializer.data)
      ```
2. **Управление контактной информацией**:
    - Создание, редактирование и удаление контакта.
    - Получение списка всех контактов компании.
3. **Управление пользователями**:
    - Регистрация и авторизация пользователей.
    - Получение информации о пользователях.
4. **Управление продуктами**:
   - Создание, редактирование и удаление продуктов, которые поставляют компании.
   - Получение списка всех продуктов.
5. **Работа с админ-панелью**:
    - Помимо основного представления, добавлена возможность просмотра контактной информации конкретной компании.
    - Реализовано действие, которое обнулит задолженость перед поставщиком у выбранной компании.

### Технические требования:

1. Запустить докер комнадой

* `docker run -p 8080:80 nginx:latest`

2. Задать настройки приложения в

* `docker-compose.yaml`

3. Заполнение файла .env согласно примеру (.env.template)
4. Создать образ и запустить контейнеры

* `docker-compose up -d --build`

5. Проверяем работоспособность в браузере

* `http://localhost:8000/redoc/`

### Работа с приложением:

1. Для начала работы необходимо зарегестрироваться на платформе по эндпоинту

* `/users/register/`
   ```json
	{
		"email": "your_email",
		"password": "your_password",
	}
	```

2. Войти в учетную запись для получения JWT-токена по эндпоинту

* `/users/login/`
  ```json
  {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzMwODUwMywiaWF0IjoxNzMzMjIyMTAzLCJqdGkiOiIzODI1YTExN2E5NDg0MWNhOTg4MDg0OGY5ODVjMWRjOCIsInVzZXJfaWQiOjF9.Ac6H0LjNQRbq3EUHwRdcJooLvQPz3zpUcC2xQ2Ge9pc",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMzA4NTAzLCJpYXQiOjE3MzMyMjIxMDMsImp0aSI6IjJhMTRhNDZiOTgzMTRmNDA4ZmQ2MDM3Y2M3N2Q0ZWMwIiwidXNlcl9pZCI6MX0.UC4phtaMVzjnI_pWg6rM9cOYqIo9RIbU0ciidjPU6sk"
  }
  ```

3. Данный токен вставляется для работы в эндпоинтах с моделями Company, Contacts и Product с помощью заголовка
   Authorization со
   значением Bearer <access token>



