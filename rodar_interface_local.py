import http.server
import socketserver
import webbrowser

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

print(f"🌐 Servindo interface em http://localhost:{PORT}")
print("🔁 Pressione Ctrl+C para encerrar.")
webbrowser.open(f"http://localhost:{PORT}/relatorio_codex.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
