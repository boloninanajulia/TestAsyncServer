# Быстрый запуск
```
docker-compose up -d
```

###Cтек технологий:
1. Модуль для асинхронного выполнения кода - asyncio;
2. Реализация вебсокетов - websockets;
3. База хранения данных - MongoDB;
4. Взаимодействие с БД - umongo, motor.


###Комментарии к заданию: 
Я выбрала MongoDB посольку это нереляционная БД (гибкая и производительная), 
распространенная. Также, из-за того, что я хотела получить опыт работы с нереляционными БД (обычно я работаю с реляционными БД PostgreSQL, SQLLite и т.д.).

Для таблицы 'Active' столбец 'id' был использован стандартный формат для MongoDB под названием 'ObjectId';
 
Дальнейшие шаги по оптимизации решения (программы) прописаны в коде как комментарии с пометкой 'TODO'