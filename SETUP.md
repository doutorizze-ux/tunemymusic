# Guia de Configuração - TuneMyMusic

## ✅ O que foi feito

Atualizei o código para usar variáveis de ambiente para as URLs da API, permitindo que você configure facilmente para desenvolvimento local ou produção.

## 📋 Checklist de Configuração

### 1. Frontend (.env)

Crie o arquivo `frontend/.env` com:

```env
VITE_API_URL=http://localhost:8889
```

**Nota:** Se você deixar vazio ou não criar o arquivo, ele usará `https://api.playlifts.com` por padrão.

### 2. Backend (.env)

Você já tem o arquivo `backend/.env`. Verifique se ele contém **TODAS** estas variáveis:

```env
# Flask
SECRET_KEY=sua-chave-secreta-aqui

# Spotify API
SPOTIFY_CLIENT_ID=seu-client-id-do-spotify
SPOTIFY_CLIENT_SECRET=seu-client-secret-do-spotify
SPOTIFY_REDIRECT_URI=http://localhost:8889/spotify/callback

# Google/YouTube API
GOOGLE_CLIENT_ID=seu-client-id-do-google
GOOGLE_CLIENT_SECRET=seu-client-secret-do-google
GOOGLE_REDIRECT_URI=http://localhost:8889/youtube/callback
YOUTUBE_API_KEY=sua-api-key-do-youtube

# Redis
REDIS_URL=redis://localhost:6379/0

# Frontend URL (para onde redirecionar após login)
FRONTEND_URL=http://localhost:5173
```

### 3. Verificar APIs Configuradas

Você precisa ter credenciais válidas de:

#### Spotify API
1. Acesse: https://developer.spotify.com/dashboard
2. Crie um app
3. Copie o Client ID e Client Secret
4. Adicione `http://localhost:8889/spotify/callback` nos Redirect URIs

#### Google/YouTube API
1. Acesse: https://console.cloud.google.com/
2. Crie um projeto
3. Ative a YouTube Data API v3
4. Crie credenciais OAuth 2.0
5. Adicione `http://localhost:8889/youtube/callback` nos Redirect URIs autorizados
6. Copie o Client ID e Client Secret
7. Crie uma API Key para YouTube

### 4. Redis

Você precisa ter o Redis rodando:

**Windows:**
- Baixe e instale: https://github.com/microsoftarchive/redis/releases
- Ou use Docker: `docker run -d -p 6379:6379 redis`

### 5. Iniciar o Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

O backend deve iniciar em `http://localhost:8889`

### 6. Iniciar o Celery Worker

Em outro terminal:

```bash
cd backend
celery -A tasks worker --loglevel=info --pool=solo
```

### 7. Iniciar o Frontend

```bash
cd frontend
npm install
npm run dev
```

O frontend deve iniciar em `http://localhost:5173`

## 🔍 Como Testar

1. Abra `http://localhost:5173` no navegador
2. Clique em "Transferir YouTube → Spotify" ou "Transferir Spotify → YouTube"
3. Faça login com Spotify e/ou YouTube
4. Teste uma transferência de playlist

## ❌ Problemas Comuns

### "Not authenticated"
- Verifique se as credenciais do Spotify/YouTube estão corretas no `.env`
- Verifique se os Redirect URIs estão configurados corretamente nos dashboards

### "CORS error"
- Verifique se o backend está rodando em `http://localhost:8889`
- Verifique se o frontend está usando a URL correta (definida em `VITE_API_URL`)

### "Task failed"
- Verifique se o Redis está rodando
- Verifique se o Celery worker está ativo

### "Connection refused"
- Verifique se o backend está rodando
- Verifique se a URL no `.env` do frontend está correta

## 📝 Notas Importantes

- As variáveis `VITE_*` no frontend só são lidas durante o build/dev server
- Se você alterar o `.env` do frontend, precisa reiniciar o `npm run dev`
- O backend lê o `.env` automaticamente com `load_dotenv(override=True)`
