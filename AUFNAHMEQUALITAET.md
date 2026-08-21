# Aufnahmequalität: was der Browser mit dem Signal macht

Diese Notiz hält fest, welche Eigenschaften der aufgenommenen Dateien **nicht**
vom Mikrofon stammen, sondern von der Aufnahmekette im Browser. Wer die
Aufnahmen später signaltechnisch auswertet oder Mikrofone vergleichen will,
muss das kennen — sonst misst er den Browser und hält es für das Mikrofon.

## Die Kette

```
Mikrofon → Betriebssystem → WebRTC-Audioverarbeitung → Resampling → Encoder → Datei
```

Von diesen fünf Stufen liegt genau eine im Mikrofon. Alles danach wird vom
Browser bestimmt und unterscheidet sich zwischen Geräten, Browsern und
Betriebssystemen.

## Zwei getrennte Probleme

### 1. Der Encoder (behoben)

`mic_recorder()` verwendet ohne Angabe `format="webm"`. Der Browser wählt dann
selbst einen verlustbehafteten Codec:

| Browser | Container / Codec |
|---|---|
| Safari (macOS, iOS) | MP4 / AAC-LC |
| Chrome, Edge, Firefox | WebM / Opus |

Folgen für die Auswertung:

- **Es gibt keine Bittiefe.** Verlustbehaftete Codecs speichern quantisierte
  Frequenzkoeffizienten, keine PCM-Abtastwerte. Eine Wortbreite ist dort nicht
  unbekannt, sondern gegenstandslos.
- **Die obere Bandgrenze setzt der Encoder**, nicht das Mikrofon. In einer
  Messreihe dieses Projekts lagen die Kanten je nach Aufnahmegerät zwischen
  13,7 kHz und 18,4 kHz — ein Unterschied von über vier Oktavbruchteilen, der
  ausschließlich aus der Kodierung stammte.
- **Die Samplerate ist die des Browsers** (meist 48 kHz, teils 44,1 kHz), nicht
  die des Mikrofons.

Behoben durch `format="wav"` in `record_audio.py`: der Browser liefert dann
unkomprimiertes PCM. Damit sind Bittiefe, Bandbreite und Samplerate wieder
eigenschaften der Aufnahme und nicht der Kodierung. Die Dateien werden größer,
was für Sprachaufnahmen dieser Länge unerheblich ist.

### 2. Die WebRTC-Verarbeitung (nicht aus diesem Repo behebbar)

`streamlit-mic-recorder` startet die Aufnahme mit:

```js
navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1 } })
```

Gesetzt wird nur die Kanalzahl. Für alles andere gelten die Browser-Vorgaben —
und die aktivieren **`echoCancellation`, `noiseSuppression` und
`autoGainControl`**. Jede Aufnahme läuft also durch eine Rauschunterdrückung,
eine Echokompensation und eine automatische Pegelregelung, bevor sie im Encoder
ankommt.

Was das bedeutet:

- **Rauschunterdrückung** entfernt leise, rauschähnliche Signalanteile. Genau
  dazu gehören Frikative (/s/, /f/, /sch/) und Silbenansätze. Bei Kindersprache
  ist das besonders folgenreich, weil diese Anteile dort ohnehin kürzer und
  leiser ausfallen als bei Erwachsenen.
- **Pegelregelung** ebnet Lautstärkeunterschiede ein und macht damit sowohl den
  gemessenen Dynamikumfang als auch jeden Pegelvergleich zwischen Geräten
  wertlos.
- Der Vorgang ist **nicht umkehrbar**. Was die Rauschunterdrückung entfernt hat,
  steht nicht mehr in der Datei und lässt sich durch keine Nachbearbeitung
  zurückholen.

Aus Python ist das nicht abschaltbar: die Zeile steht im Frontend der
Komponente, das in einem eigenen iframe läuft. Wer sie ändern will, muss
[B4PT0R/streamlit-mic-recorder](https://github.com/B4PT0R/streamlit-mic-recorder)
forken, in `frontend/src/MicRecorder.tsx` die Constraints ergänzen,

```js
navigator.mediaDevices.getUserMedia({ audio: {
  channelCount: 1,
  echoCancellation: false,
  noiseSuppression: false,
  autoGainControl: false,
} })
```

das Frontend neu bauen und das Paket aus dem Fork installieren.

## Wenn es wirklich auf die Signalqualität ankommt

Für Messreihen, in denen Mikrofone verglichen werden sollen, ist der Browser der
falsche Ort. `sounddevice` steht bereits in `requirements.txt` und nimmt lokal
auf — ohne WebRTC-Verarbeitung, ohne Encoder, in der nativen Samplerate und
Bittiefe des Geräts. Eine Browser-Aufnahme taugt für Transkription; für einen
Geräte­vergleich taugt sie nur, wenn alle Geräte durch **dieselbe** Kette
laufen, also am selben Rechner im selben Browser aufgenommen werden.

## Kurzfassung

| Kennwert | Aussagekräftig? |
|---|---|
| Bittiefe | nur mit `format="wav"` |
| Samplerate | Browser, nicht Mikrofon |
| Obere Bandgrenze | mit `format="wav"` wieder aussagekräftig |
| Absolutpegel, Dynamik | nein, solange `autoGainControl` aktiv ist |
| Rauschabstand | eingeschränkt, `noiseSuppression` wirkt mit |
| Sprachinhalt, Transkriptionsqualität | ja |
