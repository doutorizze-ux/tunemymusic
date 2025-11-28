# 🚀 Guia Rápido de Deploy

## Passo 1: Enviar código para o GitHub

1. Acesse: https://github.com/new
2. Crie um repositório (privado ou público)
3. **NÃO** marque "Initialize with README"
4. Copie a URL do repositório
5. Execute o arquivo `push-to-github.bat` e cole a URL quando solicitado

## Passo 2: Deploy no Railway (Backend)

### 2.1 Criar Projeto
1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório `tunemymusic` que você acabou de criar

### 2.2 Adicionar Redis
1. No projeto Railway, clique em **"New"** > **"Database"** > **"Add Redis"**
2. O Railway criará automaticamente a variável `REDIS_URL`

### 2.3 Configurar Serviço da API
1. Clique no serviço que foi criado automaticamente
2. Vá em **"Settings"**
3. Em **"Build"** > **"Dockerfile Path"**, altere para: `Dockerfile.api`
4. Vá em **"Variables"** e adicione (clique em "New Variable" para cada uma):

```
SECRET_KEY=sua-secret-key-aqui
SPOTIFY_CLIENT_ID=seu-spotify-client-id
SPOTIFY_CLIENT_SECRET=seu-spotify-client-secret
SPOTIFY_REDIRECT_URI=https://SEU-DOMINIO-RAILWAY.up.railway.app/spotify/callback
GOOGLE_CLIENT_ID=seu-google-client-id
GOOGLE_CLIENT_SECRET=seu-google-client-secret
GOOGLE_REDIRECT_URI=https://SEU-DOMINIO-RAILWAY.up.railway.app/youtube/callback
YOUTUBE_API_KEY=sua-youtube-api-key
FRONTEND_URL=https://SEU-DOMINIO-FRONTEND.com
```

**IMPORTANTE:** A variável `REDIS_URL` será adicionada automaticamente pelo Railway quando você adicionar o Redis.

5. Após o primeiro deploy, copie a URL pública (ex: `tunemymusic-production.up.railway.app`)
6. Volte em "Variables" e atualize `SPOTIFY_REDIRECT_URI` e `GOOGLE_REDIRECT_URI` com a URL real

### 2.4 Configurar Serviço do Celery Worker
1. No projeto Railway, clique em **"New"** > **"GitHub Repo"**
2. Selecione o **mesmo repositório** novamente
3. Nas configurações deste novo serviço:
   - **Settings** > **Dockerfile Path**: `Dockerfile.celery`
   - **Variables**: Adicione as mesmas variáveis da API (copie e cole)

### 2.5 Atualizar Callbacks nos Dashboards
1. **Spotify Dashboard** (https://developer.spotify.com/dashboard):
   - Adicione: `https://SEU-DOMINIO-RAILWAY.up.railway.app/spotify/callback`

2. **Google Console** (https://console.cloud.google.com):
   - Adicione: `https://SEU-DOMINIO-RAILWAY.up.railway.app/youtube/callback`

## Passo 3: Deploy do Frontend (Hospedagem Compartilhada)

### 3.1 Configurar variável de ambiente
1. Crie o arquivo `frontend/.env.production` com:
```
VITE_API_URL=https://SEU-DOMINIO-RAILWAY.up.railway.app
```

### 3.2 Build
Execute no terminal (pasta frontend):
```bash
npm run build
```

### 3.3 Upload
1. Acesse o cPanel da sua hospedagem
2. Vá em "Gerenciador de Arquivos"
3. Entre na pasta `public_html` (ou `www`)
4. Faça upload de **TODO o conteúdo** da pasta `frontend/dist`
   - Isso inclui: index.html, pasta assets/, .htaccess, etc.

## ✅ Verificar se está funcionando

1. **Backend:** Acesse `https://SEU-DOMINIO-RAILWAY.up.railway.app/healthz`
   - Deve retornar: `{"status":"ok"}`

2. **Frontend:** Acesse seu domínio
   - A página deve carregar normalmente

## 🔧 Troubleshooting

- **Erro 500 no Railway:** Verifique os logs em "Deployments" > "View Logs"
- **Frontend não carrega:** Verifique se o `.htaccess` foi enviado
- **Erro de CORS:** Verifique se `FRONTEND_URL` está correto no Railway
