from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Aushu Local Web UI")

static_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Aushu Local Web UI</title>
  <style>
    :root {
      color-scheme: light dark;
      --bg: #effaf6;
      --surface: #ffffff;
      --surface-strong: #d4f2e7;
      --border: #b7eed3;
      --text: #05201a;
      --muted: #3b5a52;
      --accent: #3ba58b;
      --accent-strong: #1f7f6a;
      --danger: #b91c1c;
      --shadow: 0 18px 40px rgba(30, 105, 89, 0.12);
    }
    [data-theme='dark'] {
      --bg: #0c1715;
      --surface: #122522;
      --surface-strong: #16312e;
      --border: #1f4f43;
      --text: #e7f7f2;
      --muted: #8fb7ad;
      --accent: #7fe3b2;
      --accent-strong: #4bc58c;
      --danger: #ff6b6b;
      --shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
    }
    * {
      box-sizing: border-box;
    }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, system-ui, sans-serif;
      background: radial-gradient(circle at top, rgba(59, 165, 139, 0.16), transparent 35%), var(--bg);
      color: var(--text);
    }
    .page {
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px;
    }
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .brand-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--accent), var(--accent-strong));
      box-shadow: 0 0 20px rgba(59, 165, 139, 0.45);
    }
    .brand-title {
      font-size: 1.4rem;
      font-weight: 700;
    }
    .topbar-actions {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
    }
    .button, .secondary {
      border: none;
      border-radius: 999px;
      padding: 0.85rem 1.25rem;
      font-size: 0.95rem;
      cursor: pointer;
      transition: transform 150ms ease, background-color 150ms ease;
    }
    .button {
      background: var(--accent);
      color: #fff;
      box-shadow: var(--shadow);
    }
    .secondary {
      background: rgba(255,255,255,0.15);
      color: var(--text);
    }
    .button:hover, .secondary:hover {
      transform: translateY(-1px);
    }
    .content {
      display: grid;
      gap: 1.5rem;
      grid-template-columns: 1fr 1.2fr;
      align-items: start;
    }
    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 1.5rem;
    }
    .panel h2 {
      margin: 0 0 1rem;
      font-size: 1.1rem;
      letter-spacing: 0.01em;
    }
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-size: 0.95rem;
      color: var(--muted);
    }
    select, textarea, input[type='text'] {
      width: 100%;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.92);
      color: var(--text);
      padding: 0.95rem 1rem;
      font-size: 1rem;
      outline: none;
    }
    textarea {
      min-height: 150px;
      resize: vertical;
    }
    .field-row {
      display: grid;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .field-inline {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
    .meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      margin-top: 1rem;
      flex-wrap: wrap;
    }
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.7rem 1rem;
      border-radius: 999px;
      background: rgba(59, 165, 139, 0.12);
      color: var(--accent-strong);
      font-weight: 600;
    }
    .chat-window {
      display: grid;
      gap: 1rem;
      min-height: 620px;
      padding: 1rem;
      border: 1px solid var(--border);
      border-radius: 24px;
      background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
      overflow: hidden;
    }
    .messages {
      display: grid;
      gap: 1rem;
      overflow-y: auto;
      padding-right: 0.5rem;
      max-height: 530px;
    }
    .message {
      max-width: 85%;
      padding: 1rem 1.25rem;
      border-radius: 22px;
      line-height: 1.6;
      font-size: 0.97rem;
      box-shadow: 0 10px 28px rgba(0,0,0,0.05);
    }
    .message.user {
      margin-left: auto;
      background: rgba(59, 165, 139, 0.18);
      color: var(--text);
    }
    .message.assistant {
      margin-right: auto;
      background: rgba(14, 45, 37, 0.08);
      color: var(--text);
    }
    .message.assistant strong {
      display: block;
      margin-bottom: 0.5rem;
      color: var(--accent-strong);
    }
    .about-panel {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: min(760px, calc(100vw - 2rem));
      max-height: 90vh;
      overflow-y: auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 28px;
      padding: 2rem;
      box-shadow: 0 26px 80px rgba(0, 0, 0, 0.18);
      display: none;
      z-index: 20;
    }
    .about-panel.active {
      display: block;
    }
    .about-panel h3 {
      margin-top: 0;
    }
    .about-close {
      position: absolute;
      top: 1rem;
      right: 1rem;
      border: none;
      background: transparent;
      color: var(--muted);
      font-size: 1.2rem;
      cursor: pointer;
    }
    .page::before {
      content: '';
      position: fixed;
      inset: 0;
      background: rgba(5, 32, 26, 0.12);
      pointer-events: none;
      opacity: 0.6;
    }
  </style>
</head>
<body data-theme="light">
  <div class="page">
    <header class="topbar">
      <div class="brand">
        <span class="brand-dot"></span>
        <div>
          <div class="brand-title">Aushu Local Web UI</div>
          <div style="font-size:0.93rem; color: var(--muted);">Browser-based control and local LLM completion</div>
        </div>
      </div>
      <div class="topbar-actions">
        <button class="button" id="about-button">About</button>
        <button class="secondary" id="theme-toggle">Dark mode</button>
      </div>
    </header>

    <div class="content">
      <section class="panel">
        <h2>Prompt & provider</h2>
        <div class="field-row">
          <label for="prompt">Prompt or command</label>
          <textarea id="prompt" placeholder="Write a command or ask the model anything..."></textarea>
        </div>
        <div class="field-inline">
          <div>
            <label for="provider">Provider</label>
            <select id="provider"></select>
          </div>
          <div>
            <label for="model">Model</label>
            <select id="model"></select>
          </div>
        </div>
        <div class="meta">
          <label><input id="use-llm" type="checkbox" checked /> Use LLM completion</label>
          <span class="status-pill" id="status">Loading providers...</span>
        </div>
        <div style="display:flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
          <button class="button" id="submit">Send message</button>
          <button class="secondary" id="check-provider">Check provider</button>
          <button class="secondary" id="clear-chat">Clear chat</button>
        </div>
      </section>

      <section class="panel chat-window">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:1rem;">
          <div>
            <h2 style="margin:0;">Chat</h2>
            <p style="margin:0.45rem 0 0; color: var(--muted);">Conversation history with the selected LLM provider.</p>
          </div>
          <small style="color: var(--muted);">Responses appear here after sending a prompt.</small>
        </div>
        <div class="messages" id="chat"></div>
      </section>
    </div>
  </div>

  <aside class="about-panel" id="about-panel" role="dialog" aria-modal="true" aria-labelledby="about-title">
    <button class="about-close" id="about-close">×</button>
    <h3 id="about-title">About Aushu</h3>
    <p>Aushu is a lightweight local agent interface for working with prompt-driven workflows and LLM completions. It supports both remote providers and local backends such as Ollama.</p>
    <ul>
      <li>Run prompt-based chat and command workflows.</li>
      <li>Use local Ollama models and cloud providers in one UI.</li>
      <li>Discover available models for each provider automatically.</li>
      <li>Test provider health and see live reachability status.</li>
      <li>Inspect conversation history in a clean chat interface.</li>
    </ul>
    <p>Use the buttons at the top to toggle dark mode and open this About panel. The chat area keeps your latest interactions visible while you refine prompts.</p>
  </aside>

  <script>
    const providerEl = document.getElementById('provider');
    const modelEl = document.getElementById('model');
    const promptEl = document.getElementById('prompt');
    const useLlmEl = document.getElementById('use-llm');
    const statusEl = document.getElementById('status');
    const submitEl = document.getElementById('submit');
    const checkProviderEl = document.getElementById('check-provider');
    const clearChatEl = document.getElementById('clear-chat');
    const chatEl = document.getElementById('chat');
    const themeToggle = document.getElementById('theme-toggle');
    const aboutButton = document.getElementById('about-button');
    const aboutPanel = document.getElementById('about-panel');
    const aboutClose = document.getElementById('about-close');

    let theme = 'light';

    function addMessage(role, text) {
      const item = document.createElement('div');
      item.className = `message ${role}`;
      if (role === 'assistant') {
        item.innerHTML = `<strong>Assistant</strong>${text}`;
      } else {
        item.textContent = text;
      }
      chatEl.appendChild(item);
      chatEl.scrollTop = chatEl.scrollHeight;
    }

    function setStatus(text, ok = true) {
      statusEl.textContent = text;
      statusEl.style.color = ok ? 'var(--accent-strong)' : 'var(--danger)';
    }

    function updateTheme() {
      document.body.setAttribute('data-theme', theme);
      themeToggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    }

    function showAbout() {
      aboutPanel.classList.add('active');
    }

    function hideAbout() {
      aboutPanel.classList.remove('active');
    }

    async function loadProviders() {
      setStatus('Loading providers...', true);
      try {
        const res = await fetch('/api/providers');
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        providerEl.innerHTML = '';
        data.providers.forEach(p => {
          const opt = document.createElement('option');
          opt.value = p;
          opt.textContent = p;
          providerEl.appendChild(opt);
        });
        const selected = data.providers[0] || '';
        if (selected) {
          await loadModels(selected);
          await checkProvider(selected);
        } else {
          setStatus('No providers available', false);
        }
      } catch (err) {
        setStatus('Load failed', false);
        addMessage('assistant', `Provider list failed: ${err}`);
      }
    }

    async function loadModels(provider) {
      modelEl.innerHTML = '';
      const defaultOpt = document.createElement('option');
      defaultOpt.value = '';
      defaultOpt.textContent = 'Use default model';
      modelEl.appendChild(defaultOpt);
      if (!provider) return;

      try {
        const res = await fetch(`/api/models/${encodeURIComponent(provider)}`);
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        data.models.forEach(m => {
          const opt = document.createElement('option');
          opt.value = m;
          opt.textContent = m;
          modelEl.appendChild(opt);
        });
      } catch (err) {
        const errorOpt = document.createElement('option');
        errorOpt.value = '';
        errorOpt.textContent = 'Failed to load models';
        modelEl.appendChild(errorOpt);
        addMessage('assistant', `Model list failed: ${err}`);
      }
    }

    async function checkProvider(provider) {
      if (!provider) return;
      try {
        const res = await fetch(`/api/health?provider=${encodeURIComponent(provider)}`);
        const data = await res.json();
        if (data.ok) {
          setStatus(`${provider} reachable (${data.models?.length ?? 0} models)`);
        } else {
          setStatus(`${provider} unreachable`, false);
          addMessage('assistant', `Health check failed: ${data.message}`);
        }
      } catch (err) {
        setStatus('Health check error', false);
        addMessage('assistant', `Health check error: ${err}`);
      }
    }

    async function submitPrompt() {
      const prompt = promptEl.value.trim();
      if (!prompt) {
        addMessage('assistant', 'Please enter a prompt or command first.');
        return;
      }
      addMessage('user', prompt);
      promptEl.value = '';
      setStatus('Sending prompt...', true);
      try {
        const payload = {
          prompt,
          provider: providerEl.value || null,
          model: modelEl.value || null,
          llm: useLlmEl.checked,
        };
        const res = await fetch('/api/complete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          addMessage('assistant', data.detail || JSON.stringify(data));
          setStatus('Completion failed', false);
        } else {
          addMessage('assistant', data.output || JSON.stringify(data));
          setStatus('Completion received', true);
        }
      } catch (err) {
        addMessage('assistant', `Request error: ${err}`);
        setStatus('Request failed', false);
      }
    }

    providerEl.addEventListener('change', async event => {
      const provider = event.target.value;
      await loadModels(provider);
      await checkProvider(provider);
    });

    checkProviderEl.addEventListener('click', async () => {
      await checkProvider(providerEl.value);
    });

    clearChatEl.addEventListener('click', () => {
      chatEl.innerHTML = '';
      setStatus('Chat cleared', true);
    });

    submitEl.addEventListener('click', submitPrompt);
    themeToggle.addEventListener('click', () => {
      theme = theme === 'light' ? 'dark' : 'light';
      updateTheme();
    });
    aboutButton.addEventListener('click', showAbout);
    aboutClose.addEventListener('click', hideAbout);
    window.addEventListener('click', event => {
      if (event.target === aboutPanel) hideAbout();
    });

    updateTheme();
    loadProviders();
  </script>
</body>
</html>
"""


class CompleteRequest(BaseModel):
    prompt: str
    provider: str | None = None
    model: str | None = None
    llm: bool = True


def load_agent():
    try:
        from aushu_core.agent import Agent
    except ImportError:
        repo_root = Path(__file__).resolve().parents[2]
        sys.path.insert(0, str(repo_root / "packages" / "core"))
        sys.path.insert(0, str(repo_root / "packages" / "ai"))
        sys.path.insert(0, str(repo_root / "packages" / "permissions"))
        from aushu_core.agent import Agent
    return Agent()


agent = load_agent()


@app.get("/", response_class=HTMLResponse)
def homepage() -> str:
    return static_html


@app.get("/api/providers")
def providers() -> JSONResponse:
    try:
        from aushu_ai import list_providers
    except ImportError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    try:
        return JSONResponse({"providers": list_providers()})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/models/{provider}")
def list_models(provider: str) -> JSONResponse:
    try:
        from aushu_ai import list_models
    except ImportError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    try:
        return JSONResponse({"provider": provider, "models": list_models(provider)})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/health")
def provider_health(provider: str | None = None) -> JSONResponse:
    """Basic health check for a provider. If `provider` is provided, attempt to
    list models for that provider to verify reachability. Returns JSON with
    `ok` and `message` and optional `models` list.
    """
    if provider is None:
        return JSONResponse({"ok": True, "message": "web-ui running"})
    try:
        from aushu_ai import list_models
    except Exception as exc:
        return JSONResponse({"ok": False, "message": f"aushu_ai unavailable: {exc}"}, status_code=503)
    try:
        models = list_models(provider)
        return JSONResponse({"ok": True, "message": "provider reachable", "models": list(models)})
    except Exception as exc:
        return JSONResponse({"ok": False, "message": str(exc) or "unknown error"}, status_code=503)


@app.post("/api/complete")
def complete(request: CompleteRequest) -> JSONResponse:
    if request.llm:
        try:
            result = agent.complete(request.prompt, provider=request.provider, model=request.model)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        return JSONResponse(result)

    result = agent.run(request.prompt)
    return JSONResponse(result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
