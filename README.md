# JARVIS for iPhone

A personal JARVIS-style assistant with text chat, spoken replies, and microphone dictation where the browser supports it.

## Start in GitHub Codespaces

1. Set **OPENAI_API_KEY** and **JARVIS_ACCESS_PIN** as Codespaces secrets in GitHub settings. Never put them in files committed to GitHub or in the web page. Restart Codespaces after adding them.
2. In the Codespaces terminal run `pip install -r requirements.txt`.
3. Run `python app.py`.
4. Open the forwarded **port 8000** link on your iPhone. Keep port visibility **Private**. Codespaces must stay running.
5. Enter the server access PIN in the web page and send a message.

The API key is only used by Python on the server. This is a basic personal prototype, not a production-ready public service. Keep the forwarded port private and use HTTPS. The access PIN is not stored by the web page. Requests are limited to 60 per hour per server process.

The iPhone's built-in text-to-speech is free, but not as natural as paid AI speech generation. Microphone dictation depends on browser support.

**GitHub Pages alone cannot run the Python backend.** Open the Codespaces forwarded port instead. API usage consumes your OpenAI credit, and Codespaces/hosting can have separate charges.
