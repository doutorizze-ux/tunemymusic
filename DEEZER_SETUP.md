# Configuração da API do Deezer para StaySoft

Este guia explica como configurar a integração com a API do Deezer no StaySoft.

## 📋 Pré-requisitos

- Conta Deezer (gratuita ou premium)
- Acesso ao [Deezer Developers](https://developers.deezer.com/)

## 🚀 Passo a Passo

### 1. Criar Aplicação no Deezer

1. Acesse [Deezer Developers](https://developers.deezer.com/myapps)
2. Faça login com sua conta Deezer
3. Clique em **"Create a new Application"** ou **"My Apps" → "Create new app"**
4. Preencha as informações:
   - **Application Name**: StaySoft (ou nome de sua preferência)
   - **Application Description**: Music playlist transfer application
   - **Application Domain**: `localhost` (para desenvolvimento local)
   - **Redirect URL after authentication**: `http://localhost:8889/deezer/callback`

### 2. Obter Credenciais

Após criar a aplicação, você receberá:
- **Application ID** (App ID)
- **Secret Key**

### 3. Configurar Variáveis de Ambiente

Adicione as seguintes variáveis ao arquivo `backend/.env`:

```env
# Deezer API
DEEZER_APP_ID=seu-app-id-aqui
DEEZER_SECRET_KEY=sua-secret-key-aqui
DEEZER_REDIRECT_URI=http://localhost:8889/deezer/callback
```

### 4. Permissões Necessárias

O StaySoft solicita as seguintes permissões:
- `basic_access`: Acesso básico ao perfil do usuário
- `email`: Acesso ao email do usuário
- `manage_library`: Gerenciar biblioteca de música (criar/editar playlists)
- `delete_library`: Remover itens da biblioteca (opcional)

## 🔧 Testando a Integração

1. Inicie o backend:
   ```bash
   cd backend
   python app.py
   ```

2. Inicie o frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Acesse `http://localhost:5173`
4. Clique no botão **"Entrar com Deezer"**
5. Autorize a aplicação
6. Você será redirecionado de volta ao StaySoft

## 📊 Endpoints Disponíveis

### Autenticação
- `GET /deezer/login` - Inicia o fluxo OAuth
- `GET /deezer/callback` - Callback OAuth
- `GET /auth/check` - Verifica status de login (inclui Deezer)
- `POST /auth/logout` - Faz logout de todas as plataformas

### Playlists
- `GET /deezer/playlists` - Lista playlists do usuário
- `POST /deezer/transfer` - Transfere playlist (em desenvolvimento)

## 🌐 Produção

Para produção, você precisará:

1. Atualizar o **Redirect URL** no Deezer Developers:
   ```
   https://seu-dominio.com/deezer/callback
   ```

2. Atualizar as variáveis de ambiente:
   ```env
   DEEZER_REDIRECT_URI=https://seu-dominio.com/deezer/callback
   FRONTEND_URL=https://seu-dominio.com
   ```

3. Adicionar seu domínio ao **Application Domain** no painel do Deezer

## 🔐 Segurança

- ✅ Nunca compartilhe sua **Secret Key**
- ✅ Não commite o arquivo `.env` no Git
- ✅ Use HTTPS em produção
- ✅ Tokens Deezer não expiram por padrão (mas podem ser revogados pelo usuário)

## 📚 Recursos Adicionais

- [Deezer API Documentation](https://developers.deezer.com/api)
- [OAuth Authentication Guide](https://developers.deezer.com/api/oauth)
- [API Explorer](https://developers.deezer.com/api/explorer)

## ❓ Troubleshooting

### Erro: "Invalid redirect_uri"
- Verifique se o redirect URI no código corresponde exatamente ao configurado no Deezer Developers
- Certifique-se de incluir `http://` ou `https://`

### Erro: "Invalid app_id"
- Confirme que o DEEZER_APP_ID está correto no arquivo `.env`
- Verifique se não há espaços extras nas variáveis

### Erro: "Permission denied"
- Certifique-se de que todas as permissões necessárias estão sendo solicitadas
- Revogue o acesso e tente autorizar novamente

## 🎉 Próximos Passos

Após configurar o Deezer, você poderá:
- ✅ Listar playlists do Deezer
- ✅ Transferir playlists do Spotify → Deezer
- ✅ Transferir playlists do YouTube → Deezer
- ✅ Transferir playlists do Deezer → Spotify
- ✅ Transferir playlists do Deezer → YouTube

**Nota**: As funcionalidades de transferência estão sendo implementadas gradualmente.
