# Configuração do Redis

Você está usando Redis Labs (cloud). A URL do Redis precisa incluir usuário e senha no formato:

```
redis://username:password@host:port/db
```

## Como obter as credenciais completas:

1. Acesse seu painel do Redis Labs
2. Vá em "Databases" e selecione seu database
3. Procure por "Connection" ou "Endpoint"
4. Você verá algo como:
   - **Host:** redis-10523.c228.us-central1-1.gce.cloud.redislabs.com
   - **Port:** 10523
   - **Password:** sua-senha-aqui
   - **Username:** default (geralmente)

## Formato correto no .env:

```env
REDIS_URL=redis://default:SUA_SENHA_AQUI@redis-10523.c228.us-central1-1.gce.cloud.redislabs.com:10523/0
```

**Importante:** Substitua `SUA_SENHA_AQUI` pela senha real do seu Redis.

## Alternativa: Redis Local

Se preferir usar Redis local (mais simples para desenvolvimento):

### Windows:
```bash
# Opção 1: Docker (recomendado)
docker run -d -p 6379:6379 redis

# Opção 2: Instalar Redis
# Baixe de: https://github.com/microsoftarchive/redis/releases
```

Depois use no .env:
```env
REDIS_URL=redis://localhost:6379/0
```
