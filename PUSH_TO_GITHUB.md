# So lädst du das Repo zu GitHub hoch

## Schritt 1: GitHub-Repo erstellen
1. Geh auf https://github.com/new (als `sunbooster`-User, den du noch anlegen musst)
2. Repo-Name: `ha-sunbooster-powerstation`
3. Public, **ohne** README/LICENSE/gitignore (haben wir schon)
4. "Create repository" klicken

## Schritt 2: Von HA-SSH-Terminal pushen
```bash
cd /config/sunbooster_github_repo
git init
git add .
git commit -m "Initial release v1.0.0"
git branch -M main
git remote add origin https://github.com/sunbooster/ha-sunbooster-powerstation.git
git push -u origin main
```

(Beim Push fragt Git nach Username + Personal Access Token.)

## Schritt 3: Release v1.0.0 anlegen
1. Im GitHub-Repo: **Releases** → **Draft a new release**
2. Tag: `v1.0.0`, Title: `Sunbooster Powerstation 1.0.0`
3. ZIP von `/config/sunbooster_powerstation-1.0.0.zip` hochladen
4. **Publish release**

## Schritt 4: HACS-Store einreichen (optional)
https://hacs.xyz/docs/publish/start
