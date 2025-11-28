# Configuração da API do Amazon Music para StaySoft

Este guia explica como configurar a integração com a API do Amazon Music (Login With Amazon) no StaySoft.

## ⚠️ Nota Importante

A API de reprodução e gerenciamento de playlists do Amazon Music está em **Beta Fechado**. O acesso público é restrito. Este guia cobre a configuração do **Login With Amazon (LWA)**, que é o primeiro passo para autenticação.

## 📋 Pré-requisitos

- Conta Amazon Developer
- Acesso ao [Amazon Developer Console](https://developer.amazon.com/)

## 🚀 Passo a Passo

### 1. Criar Security Profile

1. Acesse o [Amazon Developer Console](https://developer.amazon.com/loginwithamazon/console/site/lwa/overview.html).
2. Clique em **"Create a New Security Profile"**.
3. Preencha as informações:
   - **Security Profile Name**: StaySoft
   - **Security Profile Description**: Music playlist transfer application
   - **Consent Privacy Notice URL**: `http://localhost:5173/privacy`
4. Salve o perfil.

### 2. Configurar Web Settings

1. No seu novo Security Profile, vá para a aba **"Web Settings"**.
2. Clique em **"Edit"**.
3. Adicione as seguintes URLs:
   - **Allowed Origins**: `http://localhost:5173` e `http://localhost:8889`
   - **Allowed Return URLs**: `http://localhost:8889/amazon/callback`

### 3. Obter Credenciais

Copie as credenciais geradas:
- **Client ID**
- **Client Secret**

### 4. Configurar Variáveis de Ambiente

Adicione as seguintes variáveis ao arquivo `backend/.env`:

```env
# Amazon Music API
AMAZON_CLIENT_ID=seu-client-id-aqui
AMAZON_CLIENT_SECRET=seu-client-secret-aqui
AMAZON_REDIRECT_URI=http://localhost:8889/amazon/callback
```

## 🔧 Testando a Integração

1. Inicie o backend e frontend.
2. Acesse `http://localhost:5173`.
3. Clique em **"Entrar com Amazon Music"**.
4. Você será redirecionado para a página de login da Amazon.
5. Após autorizar, você retornará ao StaySoft.

## 📊 Limitações Atuais

Devido à natureza beta da API de Música:
- A listagem de playlists pode retornar vazia se sua conta não estiver na allowlist da Amazon.
- A transferência de músicas ainda não está totalmente funcional sem acesso aos endpoints protegidos.

## 📚 Recursos Adicionais

- [Login With Amazon Documentation](https://developer.amazon.com/docs/login-with-amazon/web-docs.html)
- [Amazon Music API Overview](https://developer.amazon.com/amazon-music)
