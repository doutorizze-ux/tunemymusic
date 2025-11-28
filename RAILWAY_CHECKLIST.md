# ✅ Checklist de Deploy no Railway

Use este checklist para garantir que todos os passos foram completados.

---

## 📋 Antes de começar

- [ ] Código está no GitHub
- [ ] Tenho credenciais do Spotify (Client ID + Secret)
- [ ] Tenho credenciais do Google/YouTube (Client ID + Secret + API Key)
- [ ] Tenho credenciais do Deezer (opcional)
- [ ] Tenho credenciais do Amazon Music (opcional)
- [ ] Tenho conta no Railway

---

## 🚀 Deploy no Railway

### Criar Projeto
- [ ] Criei novo projeto no Railway
- [ ] Conectei com repositório GitHub

### Redis
- [ ] Adicionei serviço Redis
- [ ] Verifiquei que `REDIS_URL` foi criada automaticamente

### Backend API
- [ ] Renomeei serviço para `backend-api`
- [ ] Configurei `Dockerfile Path` para `Dockerfile.api`
- [ ] Adicionei todas as variáveis de ambiente:
  - [ ] `SECRET_KEY`
  - [ ] `SPOTIFY_CLIENT_ID`
  - [ ] `SPOTIFY_CLIENT_SECRET`
  - [ ] `SPOTIFY_REDIRECT_URI`
  - [ ] `GOOGLE_CLIENT_ID`
  - [ ] `GOOGLE_CLIENT_SECRET`
  - [ ] `GOOGLE_REDIRECT_URI`
  - [ ] `YOUTUBE_API_KEY`
  - [ ] `DEEZER_APP_ID` (se usar)
  - [ ] `DEEZER_SECRET_KEY` (se usar)
  - [ ] `DEEZER_REDIRECT_URI` (se usar)
  - [ ] `AMAZON_CLIENT_ID` (se usar)
  - [ ] `AMAZON_CLIENT_SECRET` (se usar)
  - [ ] `AMAZON_REDIRECT_URI` (se usar)
  - [ ] `FRONTEND_URL`
- [ ] Gerei domínio público
- [ ] Copiei a URL gerada: `_________________________________`
- [ ] Atualizei as variáveis `*_REDIRECT_URI` com a URL real

### Celery Worker
- [ ] Adicionei novo serviço do mesmo repositório
- [ ] Renomeei para `celery-worker`
- [ ] Configurei `Dockerfile Path` para `Dockerfile.celery`
- [ ] Copiei todas as variáveis de ambiente da API

---

## 🔐 Atualizar Callbacks nas APIs

### Spotify
- [ ] Acessei [Spotify Dashboard](https://developer.spotify.com/dashboard)
- [ ] Adicionei callback: `https://_____.railway.app/spotify/callback`
- [ ] Salvei as alterações

### Google/YouTube
- [ ] Acessei [Google Console](https://console.cloud.google.com)
- [ ] Adicionei callback: `https://_____.railway.app/youtube/callback`
- [ ] Salvei as alterações

### Deezer (se usar)
- [ ] Acessei [Deezer Developers](https://developers.deezer.com/myapps)
- [ ] Adicionei callback: `https://_____.railway.app/deezer/callback`
- [ ] Salvei as alterações

### Amazon Music (se usar)
- [ ] Acessei Amazon Developer Console
- [ ] Adicionei callback: `https://_____.railway.app/amazon/callback`
- [ ] Salvei as alterações

---

## 🌐 Deploy do Frontend

### Opção A: Vercel
- [ ] Criei novo projeto no Vercel
- [ ] Conectei com repositório GitHub
- [ ] Configurei Root Directory: `frontend`
- [ ] Adicionei variável: `VITE_API_URL=https://_____.railway.app`
- [ ] Deploy concluído
- [ ] Copiei URL do Vercel: `_________________________________`

### Opção B: Hospedagem Compartilhada
- [ ] Criei arquivo `frontend/.env.production`
- [ ] Executei `npm run build`
- [ ] Fiz upload da pasta `dist` para `public_html`
- [ ] Verifiquei que `.htaccess` foi enviado

### Finalizar
- [ ] Atualizei `FRONTEND_URL` no Railway com a URL do frontend
- [ ] Reiniciei o serviço `backend-api`

---

## ✅ Testes

### Backend
- [ ] Acessei `https://_____.railway.app/healthz`
- [ ] Recebi resposta: `{"status": "ok"}`

### Frontend
- [ ] Acessei a URL do frontend
- [ ] Página carregou corretamente
- [ ] Tentei fazer login com Spotify - ✅ Funcionou
- [ ] Tentei fazer login com YouTube - ✅ Funcionou
- [ ] Tentei transferir uma playlist - ✅ Funcionou

### Logs
- [ ] Verifiquei logs da API - sem erros
- [ ] Verifiquei logs do Celery - sem erros
- [ ] Verifiquei logs do Redis - sem erros

---

## 🎉 Deploy Completo!

**URLs finais:**
- Backend: `https://_________________________________`
- Frontend: `https://_________________________________`

**Data do deploy:** ___/___/______

---

## 📝 Notas

Anote aqui qualquer problema encontrado ou observação importante:

```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

## 🔄 Próximas atualizações

Para atualizar o código no futuro:

1. [ ] Faço commit e push no GitHub
2. [ ] Railway faz deploy automático
3. [ ] Verifico os logs
4. [ ] Testo as funcionalidades

**Nota:** O Railway faz deploy automático sempre que você faz push para a branch `main`!
