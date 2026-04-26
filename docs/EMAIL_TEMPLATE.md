# Beta-Tester E-Mail-Template

Verwendung: Platzhalter `{{...}}` ersetzen, dann per E-Mail (z.B. service@sunbooster.com) versenden.

---

**Betreff:** Ihre Beta-Einladung: Sunbooster Powerstation in Home Assistant

**An:** {{EMAIL}}

---

Hallo {{VORNAME}},

vielen Dank, dass Sie Beta-Tester der neuen Sunbooster-Home-Assistant-Integration werden moechten!

Mit dieser Integration verbinden Sie Ihre Sunbooster-Powerstation **{{DEVICE_ID}}** direkt mit Ihrem Home Assistant – fuer 17 Sensoren, Schalter und Regler, mit denen Sie z.B. Nulleinspeisung am Hausanschluss umsetzen koennen.

**Ihr persoenlicher Beta-Key:**

```
{{CUSTOMER_KEY}}
```

(Format: SB-xxxxxxxx-xxxxxxxx – diesen Key bei der Einrichtung der Integration eingeben.)

**Naechste Schritte:**

1. Folgen Sie der Schritt-fuer-Schritt-Anleitung:  
   https://github.com/sunboostergmbh/ha-sunbooster-powerstation/blob/main/docs/ONBOARDING.md
2. Installieren Sie die Integration ueber HACS:  
   `https://github.com/sunboostergmbh/ha-sunbooster-powerstation`
3. Bei Fragen oder Problemen melden Sie sich unter **service@sunbooster.com**

**Was wir uns wuenschen:**

- Beobachten Sie die Integration ueber 1-2 Wochen
- Probieren Sie die Beispiel-Automation fuer Nulleinspeisung aus (siehe Onboarding-Doku)
- Wenn etwas nicht funktioniert: kurze Mail an service@sunbooster.com oder GitHub-Issue

**Wichtig:** Die Integration ist im Beta-Stadium. Es kann zu Fehlern oder Aussetzern kommen. Bitte nutzen Sie sie nur in Bereichen, in denen ein temporaerer Ausfall fuer Sie kein Problem ist.

Vielen Dank fuer Ihre Mithilfe!

Herzliche Gruesse  
Stefan Ponsold  
Sunbooster GmbH  
service@sunbooster.com  
https://sunbooster.com
