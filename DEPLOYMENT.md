# Production deployment (Coolify / Docker)

## Target URL

```
https://google-ads-mcp.oweb.one/mcp
```

OWeb (`agent-workspace`) expects:

```
GOOGLE_ADS_MCP_URL=https://google-ads-mcp.oweb.one/mcp
```

## Coolify

- **Project:** google-ads-mcp
- **Application UUID:** `trxusagkge807e6csumseio8`
- **Server:** mcp-servers (`5.161.179.117`)
- **Repository:** `SalesflowOne/google_ads_mcp` branch `main`
- **Build pack:** Dockerfile
- **Port:** 8000

### Required runtime env vars

| Variable | Value |
|---|---|
| `USE_GOOGLE_OAUTH_ACCESS_TOKEN` | `true` |
| `GOOGLE_ADS_CREDENTIALS` | `/app/google-ads.yaml` |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Google Ads API developer token |
| `FASTMCP_SERVER_BASE_URL` | `https://google-ads-mcp.oweb.one` |
| `PORT` | `8000` |
| `ADS_MCP_ENABLE_MUTATIONS` | `false` (optional) |

Health check: `GET /health`

## DNS (oweb.one)

Add an **A record** in your DNS provider:

```
google-ads-mcp.oweb.one  →  5.161.179.117

DNS is managed in **Cloudflare** (authoritative NS for `oweb.one`: `brynne.ns.cloudflare.com`, `carter.ns.cloudflare.com`). Create an **A** record with name `google-ads-mcp`, content `5.161.179.117`, proxy **off** (DNS only) so Coolify/Traefik can issue Let's Encrypt certs.
```

`oweb.one` nameservers are Cloudflare (`brynne.ns.cloudflare.com`, `carter.ns.cloudflare.com`).
If you manage DNS through Cloudways DNS Made Easy, ensure the record is published to the active zone.

Traefik on Coolify will issue Let's Encrypt once DNS resolves.

## OWeb Vercel (`agent-workspace`)

```
GOOGLE_ADS_MCP_URL=https://google-ads-mcp.oweb.one/mcp
GOOGLE_ADS_CLIENT_ID=<Google OAuth client id>
GOOGLE_ADS_CLIENT_SECRET=<Google OAuth client secret>
GOOGLE_ADS_MCP_ENABLE_MUTATIONS=false
```

OAuth redirect (already in OWeb):

```
https://oweb.one/api/public/oauth/google-ads/callback
```
