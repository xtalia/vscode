import http.server
import socketserver
import urllib.parse as urlparse
from hatikoenchanced import final_dict, print_item_info  # Импортируйте ваш модуль

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path.path == '/search':
            query = urlparse.parse_qs(parsed_path.query)
            search_query = urlparse.parse_qs(parsed_path.query).get('search_query', [''])[0]
            search_type = query.get('search_type', ['item_name'])[0]

            count = 0
            results = []
            try:
                for item_id, item_info in final_dict.items():
                    if search_type == "vendor_code":
                        if search_query == item_info["vendor_code"]:
                            count += 1
                            result = print_item_info(item_id, item_info)
                            results.append(result)
                    elif search_type == "item_name":
                        if search_query.lower() in item_info["item_name"].lower():
                            count += 1
                            result = print_item_info(item_id, item_info)
                            results.append(result)

                    if count == 15:
                        break

                if count < 15:
                    results.append("Готово")
                else:
                    results.append("Уменьши размер поиска или используй артикул")
            except Exception as e:
                results.append("Error: " + str(e))

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("\n".join(results).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    PORT = 25536  # Измените порт на другой при необходимости
    with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
