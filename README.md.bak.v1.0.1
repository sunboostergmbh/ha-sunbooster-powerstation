# Sunbooster Powerstation – Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/sunbooster/ha-sunbooster-powerstation/releases)

Offizielle Home-Assistant-Integration für **Sunbooster**-Powerstations. Verbindet Ihre Powerstation sicher mit Home Assistant – **ohne dass Sie sich bei der Hersteller-Plattform einloggen müssen**.

## ✨ Features

- **17 Entities** (Sensoren, Schalter, Regler) für vollständige Kontrolle
- **Nulleinspeisung**: Überschuss laden, bei Netzbezug einspeisen
- **Sicher**: Kommunikation über verschlüsselten Sunbooster-Cloud-Proxy
- **Einfach**: Ein Sunbooster-Key von Ihrem Händler – keine Acceleronix-Login nötig
- **Offline-tauglich**: Integration läuft lokal, nur API-Calls gehen nach außen

## 🚀 Installation

### Option A: HACS (empfohlen)

1. HACS öffnen → **Integrations** → ⋮ → **Custom repositories**
2. Repo-URL: `https://github.com/sunbooster/ha-sunbooster-powerstation`
3. Category: **Integration**
4. Nach **"Sunbooster Powerstation"** suchen und installieren
5. Home Assistant neu starten

### Option B: Manuell

1. [Neueste Release-ZIP herunterladen](https://github.com/sunbooster/ha-sunbooster-powerstation/releases/latest)
2. In `<config>/custom_components/sunbooster_powerstation/` entpacken
3. Home Assistant neu starten

## ⚙️ Einrichtung

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. **"Sunbooster Powerstation"** auswählen
3. Sunbooster-Key eingeben (Format: `SB-xxxxxxxx-xxxxxxxx`)
4. Fertig – 17 Entities werden automatisch angelegt

## 🔑 Sunbooster-Key erhalten

Wenden Sie sich an Ihren Sunbooster-Händler oder an [support@sunbooster.com](mailto:support@sunbooster.com).

## 📋 Entities

| Typ | Beispiel | Funktion |
|---|---|---|
| sensor | `akku_stand` | SOC in % |
| sensor | `eingangsleistung_gesamt` | Lade-Leistung in W |
| sensor | `ausgangsleistung_gesamt` | Entlade-Leistung in W |
| sensor | `verbleibende_zeit_laden` / `_entladen` | Minuten |
| sensor | `geratestatus`, `lademodus` | Status-Strings |
| number | `max_ladeleistung` | 0–1600 W |
| number | `netz_ladeleistung_mig` | 0–800 W |
| select | `lademodus` | PV / Netz / Standby |
| switch | `ac_ausgang`, `dc_ausgang`, `usb_ausgang` | Ausgänge |

## 🏗 Architektur

```
Home Assistant  ──HTTPS──►  api.sunbooster.com  ──API──►  Acceleronix Cloud  ──►  Powerstation
     (Ihr Netz)               (Sunbooster-Proxy)          (Hersteller-Cloud)      (Ihr Gerät)
```

Der Sunbooster-Proxy prüft Ihren Key, leitet Requests an die Hersteller-API weiter und liefert nur Ihre Gerätedaten zurück.

## 🔒 Datenschutz

- Der Proxy speichert **keine** Gerätedaten, nur den Customer-Key + Device-Binding
- Kommunikation: TLS 1.3 (Let's Encrypt)
- Keine Acceleronix-Zugangsdaten beim Kunden

## 🐛 Support

- [Issues auf GitHub](https://github.com/sunbooster/ha-sunbooster-powerstation/issues)
- [support@sunbooster.com](mailto:support@sunbooster.com)

## 📄 Lizenz

MIT License – siehe [LICENSE](LICENSE)
