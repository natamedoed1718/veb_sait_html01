# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer

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


if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")
    print("Любой GET-запрос возвращает страницу «Контакты»")
    print("Нажмите Ctrl+C для остановки")

    try:
        # Старт веб-сервера в бесконечном цикле
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Остановка через Ctrl+C
        pass

    # Корректная остановка веб-сервера
    webServer.server_close()
    print("Server stopped.")
