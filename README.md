# SAIL-BSP Information Assistant — Vercel deployment

This is a Telegram bot served through a FastAPI webhook on Vercel Functions.
It does **not** run a permanent polling process. Telegram sends updates to the
`/webhook` HTTPS endpoint.

## 1. Prepare the Telegram bot token

1. Open Telegram and chat with `@BotFather`.
2. If the old token has ever been exposed, revoke it and generate a new one.
3. Keep the token private. Do not commit it to GitHub or put it in source code.

## 2. Push the project to GitHub

Extract this folder and push its contents (`api/`, `requirements.txt`,
`vercel.json`, `.python-version`, etc.) to a GitHub repository.

If you keep the `sail-bsp-bot` folder inside a larger repository, set that
folder as the Vercel **Root Directory**. If its contents are at the repository
root, leave Root Directory as `./`.

## 3. Import into Vercel

1. Sign in at https://vercel.com/
2. Select **Add New → Project** and import the GitHub repository.
3. Confirm the Root Directory as described above.
4. Deploy. Vercel detects the FastAPI app in `api/index.py` and installs
   dependencies from `requirements.txt`.

## 4. Add environment variables

In Vercel, open **Project → Settings → Environment Variables** and add:

- `BOT_TOKEN` — the token from BotFather.
- `WEBHOOK_SECRET` — a long random secret used to verify Telegram webhook calls.

Add both for Production (and Preview too if you intend to test Preview
deployments), save, and redeploy so the deployment receives the variables.

Do not put either value in GitHub. The `.env.example` file contains placeholders
only.

## 5. Register the Telegram webhook

After deployment, copy the production domain, for example
`https://your-project.vercel.app`.

Run this command in a terminal, replacing all three placeholders. Use the
**same** `WEBHOOK_SECRET` value that you saved in Vercel:

```bash
curl -X POST "https://api.telegram.org/bot< BOT_TOKEN >/setWebhook" \
  --data-urlencode "url=https://your-project.vercel.app/webhook" \
  --data-urlencode "secret_token=< WEBHOOK_SECRET >"
```

Remove the spaces inside `< BOT_TOKEN >` and `< WEBHOOK_SECRET >` when
replacing the placeholders. Telegram should return `{"ok":true,...}`.

You can also register it by opening this URL in a browser after replacing the
token and domain (do not share the URL; it contains your bot token):

`https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://YOUR_PROJECT.vercel.app/webhook&secret_token=YOUR_WEBHOOK_SECRET`

## 6. Test it

1. Visit `https://your-project.vercel.app/`. You should see `{"status":"ok"}`.
2. Open your Telegram bot and send `/start`.
3. Test several menu buttons and the back-to-menu buttons.

To inspect webhook status, call Telegram's `getWebhookInfo` endpoint using
your bot token. Check Vercel **Deployments → Functions → Logs** if updates
are not being handled.

## Important hosting note

Vercel Functions are request-driven and can scale down between requests. This
is appropriate for a webhook bot: Telegram calls `/webhook` when updates arrive.
It is **not** appropriate for a bot that relies on a continuously running
`run_polling()` loop. Keep the webhook design; do not switch this project to
long polling on Vercel.

The FastAPI lifespan handler initializes and starts the Telegram application
once for a warm function instance, and shuts it down with that instance. The
webhook handler processes each incoming update without trying to initialize
the Telegram application again on every request.

## Useful links

- Vercel Python / FastAPI: https://vercel.com/docs/functions/runtimes/python
- Telegram Bot API — setWebhook: https://core.telegram.org/bots/api#setwebhook
