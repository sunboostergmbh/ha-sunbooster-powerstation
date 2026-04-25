# Changelog

## v1.0.1 (2026-04-25) - Bugfix Nulleinspeisung

### Bugfix
- **Korrektes Schalt-Verhalten für Nulleinspeisung:** Die Powerstation speist jetzt
  tatsächlich ins Hausnetz ein. Vorher wurde nur der AC-Steckdosen-Schalter
  (`ac_switch_hm`) umgelegt — das ist aber nur für direkt eingesteckte Verbraucher
  am Gehäuse. Korrekt ist `smart_on_grid_switch` (MIG-Modul, Hausnetz-Einspeisung).

### Neue Entitäten
- `switch.netz_einspeisung` (steuert `smart_on_grid_switch`) — Master-Schalter
  für Hausnetz-Einspeisung. Nutze diesen für Nulleinspeisung-Automationen.
- `switch.auto_einspeisung_soc` (steuert `soc_mig_switch`) — Optional: automatische
  Einspeisung basierend auf SOC-Schwellen (ohne externes Strom-Mess-Gerät).

### Renamed
- `number.netz_ladeleistung_mig` heißt jetzt `Netz-Einspeisung max (MIG)`
  (entity_id bleibt für Kompatibilität gleich, nur friendly_name geändert).
  Schreibt nach wie vor auf `MIG_connection_data_hm` (Setpoint 0..800W).

### Migration
Wenn du eine eigene Nulleinspeisung-Automation hast: Ändere im Discharge-Branch
`switch.<device>_ac_ausgang` auf `switch.<device>_netz_einspeisung`. Setze
zusätzlich `number.<device>_netz_ladeleistung_mig` auf den gewünschten Watt-Wert
(0..800, in 50W-Schritten).

## v1.0.0 (2026-04-24) - Initial Beta-Release
- 20 Entitäten: Akku-Stand, Eingangs-/Ausgangs-Leistung, Lademodus, Max. Ladeleistung,
  AC/DC/USB-Switches, Geräte-Status, Solar-Eingang u.v.m.
- Cloud-Polling über Sunbooster-Proxy (api.sunbooster.com)
- Authentifizierung via Customer-Key (per E-Mail nach Beta-Anmeldung)
