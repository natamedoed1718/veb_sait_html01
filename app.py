# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Настройки запуска
hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """

        # ЛЮБОЙ GET-запрос возвращает страницу «Контакты»
        try:
            # Читаем HTML файл через open()
            with open('kontakty.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Отправляем код ответа 200 (OK)
            self.send_response(200)

            # Отправляем тип данных - HTML
            self.send_header("Content-type", "text/html; charset=utf-8")

            # Завершаем формирование заголовков
            self.end_headers()

            # Отправляем HTML-содержимое
            self.wfile.write(bytes(html_content, "utf-8"))

        except FileNotFoundError:
            # Если файл не найден - ошибка 404
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes("<h1>404 - Файл kontakty.html не найден</h1>", "utf-8"))

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов (отправка формы) """

        # Получаем длину содержимого
        content_length = int(self.headers['Content-Length'])

        # Читаем данные из тела запроса
        post_data = self.rfile.read(content_length)

        # Декодируем данные из байтов в строку
        post_data_str = post_data.decode('utf-8')

        # Парсим данные формы (превращаем строку в словарь)
        form_data = urllib.parse.parse_qs(post_data_str)

        # Извлекаем значения полей
        name = form_data.get('name', [''])[0]
        email = form_data.get('email', [''])[0]
        message = form_data.get('message', [''])[0]

        # Выводим данные в консоль сервера
        print("\n" + "=" * 50)
        print("НОВОЕ СООБЩЕНИЕ ИЗ ФОРМЫ")
        print("=" * 50)
        print(f"Имя: {name}")
        print(f"Почта: {email}")
        print(f"Сообщение: {message}")
        print("=" * 50 + "\n")

        # Отправляем ответ клиенту (перенаправляем обратно на главную)
        self.send_response(303)  # 303 See Other
        self.send_header('Location', '/')
        self.end_headers()

        # Можно также отправить HTML-страницу с подтверждением
        # Но для простоты перенаправляем на главную


if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен: http://{hostName}:{serverPort}")
    print("Любой GET-запрос возвращает страницу «Контакты»")
    print("Данные из формы будут выведены в консоль")
    print("Нажмите Ctrl+C для остановки")
    print("\n" + "=" * 50)

    try:
        # Старт веб-сервера в бесконечном цикле
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Остановка через Ctrl+C
        print("\nОстановка сервера...")

    # Корректная остановка веб-сервера
    webServer.server_close()
    print("Сервер остановлен.")
