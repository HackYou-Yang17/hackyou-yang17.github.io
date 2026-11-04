# Personal website — setup and pipeline

Six plain HTML pages, one stylesheet, one small script. No build tools. What you see in the files is what goes live.

## What is in the folder

```
index.html        home
research.html     research + research CV
industry.html     industry + industry CV
programming.html  game, simulations, art
dance.html        dance and videography
cooking.html      menu, gallery, recipe book
css/style.css     every colour, font and layout rule (colours are at the very top)
js/main.js        phone menu, image zoom, footer year, recipe links
assets/img/...    one folder per page, placeholder images with the final file names
assets/cv/...     research-cv.pdf and industry-cv.pdf (placeholders)
.nojekyll         tells GitHub to serve the files as they are
```

## 1. Set up your computer (once, about 20 minutes)

1. **Git** — you already have it. Check with `git --version`.
2. **VS Code** — install it, then install the extension **Live Server** (by Ritwick Dey). It opens the site in your browser and reloads every time you save. No Live Server? In the site folder run `python -m http.server 8000` and open `http://localhost:8000` — the same trick as Flask, minus the app.
3. **GitHub account** — you have one. Note your exact username.

## 2. Put the site online (once, about 15 minutes)

1. On GitHub, create a new **public** repository named exactly `YOURUSERNAME.github.io`.
2. On your computer:
   ```
   git clone https://github.com/YOURUSERNAME/YOURUSERNAME.github.io.git
   ```
   Copy everything from this folder into the cloned folder (including `.nojekyll`).
3. Push it:
   ```
   git add .
   git commit -m "First version of the site"
   git push
   ```
4. On GitHub: repository → **Settings → Pages** → Source: **Deploy from a branch**, Branch: **main**, folder **/ (root)** → Save.
5. Wait one or two minutes, then open `https://YOURUSERNAME.github.io`.

## 3. The everyday loop

Think of it as cook → taste → serve.

1. **Cook:** open the folder in VS Code, edit a page.
2. **Taste:** right-click the page → *Open with Live Server*. Check it on desktop, then shrink the window to phone width.
3. **Serve:** `git add . && git commit -m "what changed" && git push`. Live in about a minute.

## 4. Filling in the placeholders

- **Text:** search the whole folder for `TODO` (VS Code: Ctrl+Shift+F). Every gap says what goes there.
- **Yellow dashed boxes** mark unfilled text. When you fill one, delete `class="ph"` from that tag (or just the `<span class="ph">…</span>` wrapper) and the box disappears.
- **Images:** every placeholder image already has its final name and size written on it. Replace the file with your photo **using the same name**, and the page picks it up with no code change.
- **CVs:** export each CV to PDF and save over `assets/cv/research-cv.pdf` and `assets/cv/industry-cv.pdf`.
- **Links:** search for `href="TODO` for every social or project link still missing.

## 5. Images and video — keep the site fast

- Resize photos to the size written on the placeholder (roughly 1600 px wide at most), then compress at **squoosh.app**. Aim for under 300 KB per photo.
- Pixel art: export at a whole-number scale (e.g. 32×32 sprite → 512×512) so it stays crisp. The site already displays it with sharp pixels.
- The XY and Ising GIFs: keep each under about 5 MB. If they are bigger, export an MP4 instead and use `<video src="..." autoplay muted loop playsinline>` in place of the `<img>`. MP4 is usually 5–10 times smaller.
- **Never put long videos in the repo.** Dance videos live on Instagram or YouTube and are linked or embedded. The repo should stay well under 1 GB.

## 6. Instagram and TikTok

- **Simple (set up now):** each reel tile is a link plus a cover image. Paste the reel URL into `href` and save a screenshot as `reel-1.jpg` etc.
- **Real player (optional):** on Instagram, open the reel → ••• → *Embed* → copy the code. Paste it inside a `<div class="reel">` and keep one `<script async src="https://www.instagram.com/embed.js"></script>` at the bottom of `dance.html`. Embeds load slower and Instagram controls how they look, which is why the simple version is the default.
- TikTok works the same way (Share → Embed) once you have posts.

## 7. Custom domain (when you buy one)

1. Buy the domain (Cloudflare or Porkbun are cheapest to renew). Turn on auto-renew.
2. GitHub: Settings → Pages → **Custom domain** → type it in → Save. This adds a `CNAME` file to the repo — pull it with `git pull`.
3. At your domain seller, add the DNS records GitHub lists in its docs page *"Managing a custom domain for your GitHub Pages site"*. Use the values on that page rather than any copied from elsewhere, in case they change.
4. Once it works, tick **Enforce HTTPS**.

## 8. Before you share the link

- Every page checked at phone width.
- No `TODO` left on the home, research and industry pages (the launch set).
- Unpublished research figures cleared with your supervisors.
- Both CV PDFs are the real ones.
