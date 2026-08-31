# Sessions vs JWT state management

This Python example demonstrates server-side session management. It simulates user login, logout, and profile retrieval using cookies to store a session ID on the client, while the actual user state is maintained in a server-side dictionary. This highlights the 'stateful' nature of sessions.

## Language

`python`

## How to Run

1. Save the code as `main.py`.
2. Run from your terminal: `python main.py`.
3. Use `curl` or a tool like Postman to interact with the server (e.g., POST to /login, GET /profile).

## Original Article

This example accompanies the Turkish article: [Sessions vs JWTs: Durum (State) İçin Ne Zaman Ödeme Yapıyorsunuz?](https://fatihsoysal.com/blog/sessions-vs-jwts-durum-state-icin-ne-zaman-odeme-yapiyorsunuz/).

## License

MIT — see [LICENSE](LICENSE).
