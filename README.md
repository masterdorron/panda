## 🔧 Назначение

**Panda** — это минимальное Flask-приложение, подготовленное для контейнеризации и интеграции в CI/CD-процесс. Репозиторий служит заготовкой для тестирования пайплайна Jenkins и развёртывания через Docker Compose.

> ❗ Проект написан в рамках тестового задания. Основная цель — продемонстрировать навыки работы с Docker, Jenkins и основами DevOps-практик.

---

## ⚙️ Системные требования

- Docker ≥ 20.10  
- Docker Compose ≥ 1.29  
- Jenkins с доступом к Docker (если CI/CD будет запускаться локально)

---

## 📁 Обзор структуры репозитория

```
.
├── app.py                 # Простой Flask-сервер
├── requirements.txt       # Зависимости Flask
├── Dockerfile             # Сборка Python-образа
├── docker-compose.yml     # Комбинирует сервисы (в данном случае один — web)
├── Jenkinsfile            # Описание Jenkins-пайплайна
└── README.md              # Внешнее описание (может быть доработано под публичное представление)
```

---

## 🐳 Контейнеризация

### Dockerfile

Контейнер основан на `python:3.11-slim`, копирует исходники и устанавливает зависимости через `pip`.

Приложение поднимается командой:

```bash
docker-compose up --build
```

Проверка:

```bash
curl http://localhost:5000
```

---

## 🌐 Flask-приложение

`app.py` запускает HTTP-сервер, отвечающий на GET-запрос корневого маршрута:

```python
@app.route("/")
def home():
    return "Hello from Panda!"
```

---

## 🔄 CI/CD: Jenkins

### Jenkinsfile

Jenkins использует пайплайн с declarative-синтаксисом. Этапы:

1. **Clone** — скачивание исходников  
2. **Build Docker image** — сборка образа  
3. **Test** — HTTP-запрос к `http://localhost:5001` и проверка ответа  
4. **Run container** — запуск контейнера (в фоне)  
5. **Clean up** — остановка и удаление тестового контейнера  

Для корректной работы Jenkins должен иметь доступ к Docker-сокету  
(или использовать Docker-in-Docker на агенте).

## 🚀 Развёртывание CI/CD пайплайна

Установка Jenkins (локально через Docker)
```bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  --network="host" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```
Затем открыть http://localhost:8080, ввести initial admin password (см. в логах), установить рекомендованные плагины и создать job.

Настройка job в Jenkins
Создайте Pipeline job с произвольным именем (например, panda-ci).

В настройках job выберите:

**Pipeline from SCM**

Тип: Git

URL: https://github.com/masterdorron/panda.git

## Мониторинг
### Prometheus

Настройка
Конфиг: prometheus.yml

Запуск
```bash
docker run -d \
  -p 9090:9090 \
  --network="host" \
  -v /path/to/repo/prometheus.yml:/etc/prometheus/prometheus.yml \
  --name prometheus \
  prom/prometheus
```
Цели (targets)

Docker: localhost:9323
Включить в /etc/docker/daemon.json:
```json
{
  "metrics-addr": "127.0.0.1:9323",
  "experimental": true
}
```
cAdvisor: localhost:8082

### cAdvisor
Запуск
```bash
docker run -d \
  -p 8082:8080 \
  --network="host" \
  --name cadvisor \
  google/cadvisor:latest
```
### Grafana
Запуск
```bash
docker run -d \
  -p 3000:3000 \
  --network="host" \
  --name grafana \
  grafana/grafana
```
Доступ
http://localhost:3000
Логин: admin
Пароль: admin

Источник данных
http://localhost:9090

Дашборд

CPU:
```bash
sum(rate(container_cpu_usage_seconds_total{name="app-container"}[1m]))
```
Память:
```bash
container_memory_usage_bytes{name="app-container"}
```
Оповещения

CPU > 80% в течение 1 минуты:
Память > 500MB в течение 1 минуты:

