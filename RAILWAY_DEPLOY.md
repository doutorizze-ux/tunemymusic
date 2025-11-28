# 🚂 Guia Completo de Deploy no Railway

Este guia mostra como fazer o deploy completo da aplicação TuneMyMusic no Railway.

---

## 📋 Pré-requisitos

1. ✅ Conta no [Railway.app](https://railway.app/)
2. ✅ Conta no [GitHub](https://github.com/)
3. ✅ Código do projeto no GitHub
4. ✅ Credenciais das APIs (Spotify, YouTube, Deezer, Amazon Music)

---

## 🎯 Arquitetura do Deploy

O deploy será dividido em **3 serviços** no Railway:

1. **Redis** - Banco de dados em memória para filas
2. **API (Backend)** - Flask + Gunicorn
3. **Celery Worker** - Processamento de tarefas em background

---

## 📦 Passo 1: Preparar o Repositório no GitHub

### 1.1 Se ainda não tiver o código no GitHub:

```bash
# No terminal, na pasta do projeto
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/tunemymusic.git
git push -u origin main
```

### 1.2 Verificar arquivos importantes:

Certifique-se de que estes arquivos existem:
- ✅ `Dockerfile.api`
- ✅ `Dockerfile.celery`
- ✅ `backend/requirements.txt`
- ✅ `.dockerignore`

---

## 🚀 Passo 2: Criar Projeto no Railway

### 2.1 Criar novo projeto

1. Acesse [railway.app](https://railway.app/)
2. Faça login com sua conta GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório `tunemymusic`
6. O Railway criará automaticamente um serviço

---

## 🔴 Passo 3: Adicionar Redis

### 3.1 Adicionar serviço Redis

1. No projeto Railway, clique em **"+ New"**
2. Selecione **"Database"** → **"Add Redis"**
3. O Railway criará automaticamente a variável `REDIS_URL`
4. ✅ Anote que o Redis está configurado

---

## ⚙️ Passo 4: Configurar Serviço da API

### 4.1 Renomear o serviço

1. Clique no serviço que foi criado automaticamente
2. Clique em **"Settings"** (ícone de engrenagem)
3. Em **"Service Name"**, renomeie para: `backend-api`

### 4.2 Configurar Dockerfile

1. Ainda em **"Settings"**
2. Role até **"Build"**
3. Em **"Dockerfile Path"**, altere para: `Dockerfile.api`
4. Clique em **"Save"**

### 4.3 Adicionar variáveis de ambiente

1. Clique na aba **"Variables"**
2. Clique em **"+ New Variable"** e adicione cada uma das seguintes:

```env
SECRET_KEY=d03b84527c89a4d6aa7364f098f718797a9f14bf862b42e983520cb1e99d9922

# Spotify
SPOTIFY_CLIENT_ID=seu-spotify-client-id
SPOTIFY_CLIENT_SECRET=seu-spotify-client-secret
SPOTIFY_REDIRECT_URI=https://SEU-DOMINIO.railway.app/spotify/callback

# Google/YouTube
GOOGLE_CLIENT_ID=seu-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret
GOOGLE_REDIRECT_URI=https://SEU-DOMINIO.railway.app/youtube/callback
YOUTUBE_API_KEY=sua-youtube-api-key

# Deezer (opcional)
DEEZER_APP_ID=seu-deezer-app-id
DEEZER_SECRET_KEY=seu-deezer-secret-key
DEEZER_REDIRECT_URI=https://SEU-DOMINIO.railway.app/deezer/callback

# Amazon Music (opcional)
AMAZON_CLIENT_ID=seu-amazon-client-id
AMAZON_CLIENT_SECRET=seu-amazon-client-secret
AMAZON_REDIRECT_URI=https://SEU-DOMINIO.railway.app/amazon/callback

# Frontend URL (atualize depois)
FRONTEND_URL=http://localhost:5173
```

**⚠️ IMPORTANTE:** 
- A variável `REDIS_URL` será adicionada automaticamente pelo Railway
- Substitua `SEU-DOMINIO` pela URL real após o primeiro deploy
- Substitua os valores `seu-*` pelas suas credenciais reais

### 4.4 Configurar domínio público

1. Vá em **"Settings"** → **"Networking"**
2. Clique em **"Generate Domain"**
3. O Railway gerará uma URL como: `backend-api-production-xxxx.up.railway.app`
4. ✅ **Copie esta URL** - você precisará dela!

### 4.5 Atualizar variáveis com a URL real

1. Volte em **"Variables"**
2. Atualize as seguintes variáveis com a URL que você copiou:
   - `SPOTIFY_REDIRECT_URI=https://backend-api-production-xxxx.up.railway.app/spotify/callback`
   - `GOOGLE_REDIRECT_URI=https://backend-api-production-xxxx.up.railway.app/youtube/callback`
   - `DEEZER_REDIRECT_URI=https://backend-api-production-xxxx.up.railway.app/deezer/callback`
   - `AMAZON_REDIRECT_URI=https://backend-api-production-xxxx.up.railway.app/amazon/callback`

---

## 🔄 Passo 5: Configurar Celery Worker

### 5.1 Adicionar novo serviço

1. No projeto Railway, clique em **"+ New"**
2. Selecione **"GitHub Repo"**
3. Escolha o **mesmo repositório** (`tunemymusic`)

### 5.2 Configurar o serviço

1. Renomeie o serviço para: `celery-worker`
2. Vá em **"Settings"** → **"Build"**
3. Em **"Dockerfile Path"**, altere para: `Dockerfile.celery`

### 5.3 Adicionar variáveis de ambiente

1. Clique em **"Variables"**
2. Adicione as **mesmas variáveis** que você adicionou na API
3. **Dica:** Você pode copiar e colar todas de uma vez

**Variáveis necessárias:**
- `REDIS_URL` (será adicionada automaticamente)
- `SECRET_KEY`
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- `YOUTUBE_API_KEY`
- `DEEZER_APP_ID` (opcional)
- `DEEZER_SECRET_KEY` (opcional)
- `DEEZER_REDIRECT_URI` (opcional)
- `AMAZON_CLIENT_ID` (opcional)
- `AMAZON_CLIENT_SECRET` (opcional)
- `AMAZON_REDIRECT_URI` (opcional)
- `FRONTEND_URL`

### 5.4 Desabilitar domínio público (opcional)

O Celery Worker não precisa de domínio público:
1. Vá em **"Settings"** → **"Networking"**
2. Se houver um domínio gerado, você pode removê-lo

---

## 🔐 Passo 6: Atualizar Callbacks nas APIs

Agora você precisa atualizar as URLs de callback nos dashboards das APIs:

### 6.1 Spotify Dashboard

1. Acesse: [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Selecione seu aplicativo
3. Clique em **"Edit Settings"**
4. Em **"Redirect URIs"**, adicione:
   ```
   https://backend-api-production-xxxx.up.railway.app/spotify/callback
   ```
5. Clique em **"Save"**

### 6.2 Google Cloud Console (YouTube)

1. Acesse: [https://console.cloud.google.com](https://console.cloud.google.com)
2. Vá em **"APIs & Services"** → **"Credentials"**
3. Clique no seu OAuth 2.0 Client ID
4. Em **"Authorized redirect URIs"**, adicione:
   ```
   https://backend-api-production-xxxx.up.railway.app/youtube/callback
   ```
5. Clique em **"Save"**

### 6.3 Deezer (se estiver usando)

1. Acesse: [https://developers.deezer.com/myapps](https://developers.deezer.com/myapps)
2. Selecione seu aplicativo
3. Atualize a **"Redirect URI"** para:
   ```
   https://backend-api-production-xxxx.up.railway.app/deezer/callback
   ```

### 6.4 Amazon Music (se estiver usando)

1. Acesse o Amazon Developer Console
2. Atualize a **"Redirect URI"** para:
   ```
   https://backend-api-production-xxxx.up.railway.app/amazon/callback
   ```

---

## 🌐 Passo 7: Deploy do Frontend

### 7.1 Opção A: Deploy no Vercel (Recomendado)

1. Acesse: [https://vercel.com](https://vercel.com)
2. Faça login com GitHub
3. Clique em **"New Project"**
4. Selecione o repositório `tunemymusic`
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Adicione variável de ambiente:
   - `VITE_API_URL=https://backend-api-production-xxxx.up.railway.app`
7. Clique em **"Deploy"**

### 7.2 Opção B: Build local e upload para hospedagem compartilhada

1. Crie o arquivo `frontend/.env.production`:
   ```env
   VITE_API_URL=https://backend-api-production-xxxx.up.railway.app
   ```

2. Execute o build:
   ```bash
   cd frontend
   npm run build
   ```

3. Faça upload do conteúdo da pasta `frontend/dist` para sua hospedagem:
   - Acesse o cPanel
   - Vá em **"Gerenciador de Arquivos"**
   - Entre na pasta `public_html`
   - Faça upload de **todos os arquivos** de `frontend/dist`

### 7.3 Atualizar FRONTEND_URL no Railway

1. Volte ao Railway
2. No serviço **backend-api**, vá em **"Variables"**
3. Atualize `FRONTEND_URL` com a URL do seu frontend:
   - Se Vercel: `https://tunemymusic.vercel.app`
   - Se hospedagem própria: `https://seudominio.com`

---

## ✅ Passo 8: Verificar se está funcionando

### 8.1 Testar Backend

Acesse no navegador:
```
https://backend-api-production-xxxx.up.railway.app/healthz
```

**Resposta esperada:**
```json
{"status": "ok"}
```

### 8.2 Testar Frontend

1. Acesse a URL do seu frontend
2. A página deve carregar normalmente
3. Tente fazer login com Spotify ou YouTube

### 8.3 Verificar logs

**Logs da API:**
1. No Railway, clique no serviço **backend-api**
2. Vá na aba **"Deployments"**
3. Clique no deployment mais recente
4. Clique em **"View Logs"**

**Logs do Celery:**
1. Clique no serviço **celery-worker**
2. Vá na aba **"Deployments"**
3. Clique no deployment mais recente
4. Clique em **"View Logs"**

---

## 🔧 Troubleshooting

### ❌ Erro 500 no backend

**Solução:**
1. Verifique os logs no Railway
2. Certifique-se de que todas as variáveis de ambiente estão corretas
3. Verifique se o Redis está rodando

### ❌ Erro de CORS

**Solução:**
1. Verifique se `FRONTEND_URL` está correto no Railway
2. Certifique-se de que não há `/` no final da URL

### ❌ Login não funciona

**Solução:**
1. Verifique se as URLs de callback estão corretas nos dashboards das APIs
2. Verifique se as variáveis `*_REDIRECT_URI` estão corretas no Railway
3. Certifique-se de que as credenciais das APIs estão corretas

### ❌ Tarefas não processam (Celery)

**Solução:**
1. Verifique os logs do **celery-worker**
2. Certifique-se de que `REDIS_URL` está configurado
3. Verifique se o serviço Redis está rodando

### ❌ Build falha

**Solução:**
1. Verifique se `Dockerfile.api` e `Dockerfile.celery` estão corretos
2. Verifique se `backend/requirements.txt` está completo
3. Veja os logs de build no Railway

---

## 📊 Monitoramento

### Ver uso de recursos

1. No Railway, clique no projeto
2. Vá em **"Usage"**
3. Você verá:
   - CPU usage
   - Memory usage
   - Network usage

### Reiniciar serviços

Se precisar reiniciar algum serviço:
1. Clique no serviço
2. Vá em **"Settings"**
3. Role até o final
4. Clique em **"Restart"**

---

## 💰 Custos

O Railway oferece:
- **$5 de crédito grátis por mês** (sem cartão de crédito)
- **$500 de crédito grátis** no primeiro mês (com cartão de crédito)

**Estimativa de custo mensal:**
- Redis: ~$5/mês
- Backend API: ~$5-10/mês
- Celery Worker: ~$5-10/mês
- **Total: ~$15-25/mês**

---

## 🎉 Pronto!

Sua aplicação TuneMyMusic agora está rodando no Railway! 🚀

**URLs importantes:**
- Backend API: `https://backend-api-production-xxxx.up.railway.app`
- Frontend: `https://seudominio.com` ou `https://tunemymusic.vercel.app`
- Health Check: `https://backend-api-production-xxxx.up.railway.app/healthz`

---

## 📚 Próximos passos

1. Configure um domínio customizado no Railway (opcional)
2. Configure SSL/HTTPS (Railway faz automaticamente)
3. Configure monitoramento de erros (Sentry, etc)
4. Configure backups do Redis (se necessário)

---

## 🆘 Precisa de ajuda?

- [Documentação do Railway](https://docs.railway.app/)
- [Discord do Railway](https://discord.gg/railway)
- [GitHub Issues](https://github.com/seu-usuario/tunemymusic/issues)
