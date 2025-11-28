# Guia de Deploy: Híbrido (Railway + Host Compartilhada)

Este guia explica como fazer o deploy do Backend no **Railway** e do Frontend em uma **Hospedagem Compartilhada** (cPanel, Hostgator, Hostinger, etc).

---

## Parte 1: Backend (Railway)

O Backend será dividido em dois serviços no Railway: a API e o Worker (Celery).

### 1. Preparação
1. Crie uma conta no [Railway.app](https://railway.app/).
2. Instale a CLI do Railway (opcional) ou conecte seu GitHub.
3. Certifique-se de que este projeto está no seu GitHub.

### 2. Criar Novo Projeto
1. No Railway, clique em **"New Project"** > **"Deploy from GitHub repo"**.
2. Selecione o repositório deste projeto.
3. **IMPORTANTE:** O Railway tentará detectar automaticamente, mas precisamos configurar dois serviços separados.

### 3. Configurar Serviço da API
1. Nas configurações do serviço criado, vá em **"Settings"**.
2. Em **"Root Directory"**, mantenha `/`.
3. Em **"Build"** > **"Dockerfile Path"**, altere para `Dockerfile.api`.
4. Vá em **"Variables"** e adicione:
   - `SECRET_KEY`: (Gere uma chave aleatória forte)
   - `SPOTIFY_CLIENT_ID`: (Seu ID do Spotify)
   - `SPOTIFY_CLIENT_SECRET`: (Seu Secret do Spotify)
   - `SPOTIFY_REDIRECT_URI`: `https://<SEU-URL-RAILWAY>/spotify/callback` (Você pegará a URL após o primeiro deploy)
   - `GOOGLE_CLIENT_ID`: (Seu ID do Google)
   - `GOOGLE_CLIENT_SECRET`: (Seu Secret do Google)
   - `GOOGLE_REDIRECT_URI`: `https://<SEU-URL-RAILWAY>/youtube/callback`
   - `YOUTUBE_API_KEY`: (Sua chave de API do YouTube)
   - `FRONTEND_URL`: `https://<SEU-DOMINIO-FRONTEND>` (Ex: meussite.com)
5. Adicione um banco de dados **Redis** ao projeto (New > Database > Redis).
6. O Railway criará automaticamente a variável `REDIS_URL`.

### 4. Configurar Serviço do Celery Worker
1. Clique em **"New"** > **"GitHub Repo"** e selecione o **mesmo repositório** novamente.
2. Nas configurações deste novo serviço:
   - **Dockerfile Path**: `Dockerfile.celery`
   - **Variables**: Copie as mesmas variáveis da API, principalmente `REDIS_URL`, `SPOTIFY_...`, `GOOGLE_...`, `YOUTUBE_API_KEY`.

### 5. Finalizar
1. Após o deploy da API, copie a URL pública gerada (ex: `playlifts-production.up.railway.app`).
2. Atualize as variáveis `SPOTIFY_REDIRECT_URI` e `GOOGLE_REDIRECT_URI` no Railway com essa URL.
3. Atualize também no **Spotify Dashboard** e **Google Console** com as novas URLs de callback.

---

## Parte 2: Frontend (Hospedagem Compartilhada)

### 1. Configurar URL da API
1. No seu computador, crie/edite o arquivo `frontend/.env.production`:
   ```env
   VITE_API_URL=https://<SUA-URL-DA-API-NO-RAILWAY>
   ```

### 2. Build
1. Abra o terminal na pasta `frontend`.
2. Execute:
   ```bash
   npm run build
   ```
3. Isso criará uma pasta `dist` com os arquivos otimizados.

### 3. Upload
1. Acesse o gerenciador de arquivos da sua hospedagem (cPanel ou FTP).
2. Abra a pasta pública (geralmente `public_html` ou `www`).
3. Faça o upload de **todo o conteúdo** de dentro da pasta `dist` (index.html, assets, .htaccess, etc) para lá.
4. **Nota:** O arquivo `.htaccess` já foi criado automaticamente na pasta `public` para garantir que a navegação funcione.

---

## Resumo das URLs
- **Frontend:** `https://seusite.com`
- **Backend API:** `https://playlifts-production.up.railway.app` (exemplo)
- **Callbacks:** `https://playlifts-production.up.railway.app/spotify/callback`
