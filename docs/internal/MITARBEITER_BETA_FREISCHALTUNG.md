cat >> $F << 'EOF1'
# Beta-User hinzufügen – Anleitung für Sunbooster-Mitarbeiter

> **Interne Anleitung** – nicht für Kunden bestimmt.
> Stand: April 2026 · Kontakt bei Fragen: service@sunbooster.com

Diese Anleitung beschreibt Schritt für Schritt, wie ein neuer Beta-Tester für die Sunbooster Home Assistant Integration freigeschaltet wird. Du brauchst dafür **kein** Programmier-Wissen, nur einen SSH-Zugang zum Sunbooster-API-Server.

---

## Voraussetzungen (einmalig einrichten)

1. **SSH-Zugang zum API-Server** (Hetzner)
   - Server: 49.12.193.229
   - SSH-Alias: hetzner (in ~/.ssh/config eingetragen)
   - Wenn du noch keinen Zugang hast: bei der IT melden.

2. **Admin-Token** (zum Erzeugen von Customer-Keys)
   - Liegt verschlüsselt im Passwort-Manager unter Sunbooster -> API -> ADMIN_TOKEN
   - **Niemals per Mail oder Chat weitergeben.**

3. **Device-ID des Kunden**
   - Steht auf dem Typenschild der Powerstation (12-stelliger Code, z. B. 502065bd3c63)
   - Alternativ in unserer Geräte-Datenbank suchen.

EOF1
wc -l $F && head -5 $F
---

## Ablauf: Neuen Beta-User freischalten

### Schritt 1 – Kunden-Daten sammeln

Du brauchst vom Kunden:

| Feld | Beispiel |
|------|----------|
| Vorname | Max |
| E-Mail | max.mustermann@example.com |
| Device-ID | 502065bd3c63 |

Trage diese Daten in unsere interne Beta-Liste ein (Google Sheet "Sunbooster Beta-Tester").

---

### Schritt 2 – Customer-Key generieren

Per SSH auf den API-Server verbinden:

```bash
ssh hetzner
```

Dann das mitgelieferte Skript ausführen:

```bash
cd /opt/sunbooster-api
./scripts/generate_key.sh <DEVICE_ID>
```

**Beispiel:**

```bash
./scripts/generate_key.sh 502065bd3c63
```

Das Skript fragt nach dem Admin-Token (aus dem Passwort-Manager kopieren – die Eingabe ist unsichtbar) und gibt anschließend einen Customer-Key aus, etwa:

```
Key generated:
   Device:  502065bd3c63
   Key:     SB-DRBV5uvKVhfr-ggc57Ir_9apdI5F5Cwu
   Expires: 2027-04-26
```

**Diesen Key kopieren** – er taucht nur einmal auf.

---

### Schritt 3 – Onboarding-Mail an den Kunden

Die fertige Mail-Vorlage liegt im Repo unter `docs/EMAIL_TEMPLATE.md`. Öffne sie und ersetze die Platzhalter:

| Platzhalter | Eintragen |
|-------------|-----------|
| `{{VORNAME}}` | Vorname des Kunden |
| `{{EMAIL}}` | E-Mail des Kunden |
| `{{DEVICE_ID}}` | Device-ID |
| `{{CUSTOMER_KEY}}` | Generierter Key aus Schritt 2 |

Die fertige Mail aus deinem Outlook/Gmail an den Kunden senden.

> Tipp: Lege dir eine Outlook-Vorlage an, dann musst du nur die vier Felder ersetzen.

---

### Schritt 4 – Eintrag in der Beta-Liste

Im Google Sheet "Sunbooster Beta-Tester" folgende Spalten ausfüllen:

- Datum Freischaltung
- Vorname / E-Mail / Device-ID
- Customer-Key (Tipp: nur die letzten 6 Zeichen für Identifikation, kompletten Key sicher speichern)
- Status: aktiv

---

## Häufige Probleme

### "Permission denied" beim SSH-Login
SSH-Key fehlt. Bei der IT melden.

### Skript meldet `401 Unauthorized`
Falscher Admin-Token. Token im Passwort-Manager prüfen, Eingabe wiederholen.

### Skript meldet `Device not found`
Device-ID falsch geschrieben. **Nur Kleinbuchstaben und Ziffern**, keine Bindestriche.

### Kunde meldet "Integration findet Powerstation nicht"
1. Customer-Key korrekt eingetragen? (Groß-/Kleinschreibung beachten!)
2. Powerstation online im WLAN? (LED-Status am Gerät prüfen)
3. Home Assistant neu gestartet? (Einstellungen -> System -> Neustart)

Bei weiteren Problemen: Issue auf https://github.com/sunboostergmbh/ha-sunbooster-powerstation/issues anlegen.

---

## Was darf NICHT passieren

- Admin-Token per Mail/Chat versenden
- Customer-Keys mehrfach für dieselbe Device-ID erzeugen (alter Key wird ungültig!)
- Kunden interne Cloud-Zugänge weitergeben
- Beta-Tester-Daten außerhalb des Google Sheets speichern (DSGVO)

---

## Eskalation

| Problem | Ansprechpartner |
|---------|-----------------|
| Technisches Problem mit der Integration | service@sunbooster.com |
| API-Server-Ausfall | IT-Bereitschaft |
| DSGVO-Frage zu Kundendaten | Datenschutzbeauftragter |
| Kunde will Beta verlassen | Eintrag im Sheet auf "deaktiviert" setzen, Key in der Datenbank sperren (siehe Admin-API-Doku) |

---

*Letzte Aktualisierung: April 2026 · Sunbooster GmbH*
