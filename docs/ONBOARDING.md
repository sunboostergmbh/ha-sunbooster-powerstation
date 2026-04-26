# Sunbooster Powerstation – Beta-Onboarding

Willkommen im Beta-Programm der Sunbooster-Home-Assistant-Integration!

Mit dieser Integration verbindet sich Ihre Sunbooster-Powerstation direkt mit Home Assistant. Sie bekommen 17 Sensoren, Schalter und Regler – und können damit z.B. Nulleinspeisung am Hausanschluss umsetzen.

## Was Sie bekommen

- **Sunbooster-Key** (Format `SB-xxxxxxxx-xxxxxxxx`) per E-Mail
- Zugang zur Beta-Integration auf GitHub
- Direkten Support unter service@sunbooster.com
- Updates automatisch über HACS

## Voraussetzungen

- Home Assistant (Version 2024.6 oder neuer)
- HACS installiert (https://hacs.xyz)
- Internetverbindung (für Cloud-Proxy)
- Ihre Sunbooster-Powerstation muss in Betrieb und in der Sunbooster-App registriert sein

## Installation in 5 Schritten

### 1. HACS Custom Repository hinzufuegen

1. In Home Assistant: **HACS** -> **Integrations** -> Drei-Punkte-Menue oben rechts -> **Custom repositories**
2. Repo-URL einfuegen: `https://github.com/sunboostergmbh/ha-sunbooster-powerstation`
3. Category: **Integration**
4. **Add** klicken

### 2. Integration installieren

1. In HACS nach **"Sunbooster Powerstation"** suchen
2. **Download** klicken -> Version waehlen (neueste) -> **Download**
3. Home Assistant **neu starten** (Einstellungen -> System -> Neustart)

### 3. Integration einrichten

1. **Einstellungen** -> **Geraete & Dienste** -> **Integration hinzufuegen**
2. Nach **"Sunbooster Powerstation"** suchen
3. Ihren **Sunbooster-Key** eingeben (aus der Willkommens-Mail)
4. Fertig – 17 Entitaeten werden automatisch angelegt

### 4. Erste Entitaeten ansehen

Unter **Einstellungen -> Geraete & Dienste -> Sunbooster Powerstation** finden Sie:

- `sensor.<geraete-id>_akku_stand` (Ladezustand in %)
- `sensor.<geraete-id>_eingangsleistung_gesamt` (Solar/Netz Eingang)
- `sensor.<geraete-id>_ausgangsleistung_gesamt` (Hausnetz Ausgang)
- `switch.<geraete-id>_netz_einspeisung` (Hausnetz-Einspeisung an/aus)
- `number.<geraete-id>_netz_ladeleistung_mig` (0..800 W Setpoint)
- `number.<geraete-id>_max_ladeleistung` (0..1600 W Ladegrenze)
- `select.<geraete-id>_lademodus` (off/normal/fast/silent)
- ...und weitere

### 5. Beispiel-Automation: Nulleinspeisung

Sie brauchen einen Strom-Sensor am Hausanschluss (z.B. Shelly Pro 3EM). Dann:

```yaml
- alias: Sunbooster Nulleinspeisung
  trigger:
    - platform: state
      entity_id: sensor.shellypro3em_<id>_leistung
  action:
    - choose:
        # Netzbezug -> Powerstation einspeisen
        - conditions:
            - condition: numeric_state
              entity_id: sensor.shellypro3em_<id>_leistung
              above: 50
          sequence:
            - service: number.set_value
              target:
                entity_id: number.<geraete-id>_netz_ladeleistung_mig
              data:
                value: "{{ [800, [50, ((states('sensor.shellypro3em_<id>_leistung') | float(0)) | round(0))] | max] | min }}"
            - service: switch.turn_on
              target:
                entity_id: switch.<geraete-id>_netz_einspeisung
        # Ueberschuss -> einspeisen aus, laden
        - conditions:
            - condition: numeric_state
              entity_id: sensor.shellypro3em_<id>_leistung
              below: -50
          sequence:
            - service: switch.turn_off
              target:
                entity_id: switch.<geraete-id>_netz_einspeisung
            - service: select.select_option
              target:
                entity_id: select.<geraete-id>_lademodus
              data:
                option: normal
```

## Was Sie testen sollen

1. **Installation klappt** – komplett bis HA-Restart
2. **Geraete-Verbindung** – sehen Sie aktuelle Akku-, Eingangs- und Ausgangswerte?
3. **Schalter funktionieren** – `ac_ausgang` an/aus, `netz_einspeisung` an/aus
4. **Setpoints werden uebernommen** – `netz_ladeleistung_mig` von 0 auf 400 setzen, beobachten ob die Powerstation tatsaechlich einspeist
5. **Stabilitaet ueber 1 Woche** – laufen die Sensoren stabil? Gibt es API-Aussetzer?
6. **Nulleinspeisung-Automation** – funktioniert sie ueber den Tag?

## Feedback / Probleme

- **Bugs**: GitHub Issue erstellen unter https://github.com/sunboostergmbh/ha-sunbooster-powerstation/issues
- **Fragen**: E-Mail an service@sunbooster.com
- **Schnelle Hilfe**: Beim E-Mail-Support bitte folgende Infos beilegen:
  - Geraete-ID (siehe Sunbooster-App)
  - HA-Version (Einstellungen -> Info)
  - Integration-Version (HACS -> Sunbooster Powerstation)
  - Beschreibung des Problems + ggf. Logfile (Einstellungen -> System -> Logs -> "sunbooster")

## Beta-Hinweis

Diese Integration ist im **Beta-Stadium**:

- Es kann zu unerwarteten Fehlern oder Datenausfaellen kommen
- Updates koennen Breaking Changes enthalten (wir kommunizieren diese im Changelog)
- Es gibt **keine Garantie** auf Verfuegbarkeit oder Funktionsumfang
- Nutzung **auf eigene Verantwortung** – speziell bei automatisierter Steuerung von Stromfluessen
- Keine SLA, kein 24/7-Support – aber ehrliches und schnelles Feedback per E-Mail

Vielen Dank fuer Ihre Mithilfe! Ihr Feedback macht das Produkt besser.

– Ihr Sunbooster-Team  
service@sunbooster.com
