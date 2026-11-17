"""Regenera index.xml (ReaPack) con la versión y el commit actual de cada repo Nube (carpetas hermanas en ~/Music)."""
import subprocess, pathlib, re, datetime, os
# carpeta con los repos Nube; NUBE_ROOT=~/Music cuando se corre desde un worktree
M = pathlib.Path(os.environ["NUBE_ROOT"]).expanduser() if os.environ.get("NUBE_ROOT") else pathlib.Path(__file__).resolve().parent.parent
P = [("NubeEQ", "nube-eq", "Parametric EQ, 16 bands, M/S, dynamic"), ("NubeComp", "nube-comp", "Compressor, 5 styles, sidechain, lookahead"),
     ("NubeVerb", "nube-verb", "Algorithmic reverb, 16-line FDN, shimmer, freeze"), ("NubeDeEss", "nube-deess", "De-esser, relative detection, split-band"),
     ("NubeLimit", "nube-limit", "Brickwall limiter, true peak, LUFS meter"), ("NubeDelay", "nube-delay", "Delay, tape / analog / lo-fi, ping-pong, ducking"),
     ("NubeSynth", "nube-synth", "Polyphonic synthesizer, unison, FM, glide, modulation matrix"),
     ("NubeGate", "nube-gate", "Gate / expander / ducker, transient detection, MIDI trigger"),
     ("NubeSampler", "nube-sampler", "Sampler, multi-sample zones, MPC-style chops, one-shot, time-stretch, tempo sync"),
     ("NubeTune", "nube-tune", "Pitch correction (auto-tune), scales, formants, MIDI")]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
# las entradas que no cambiaron de fuente conservan su fecha (el diff muestra solo lo nuevo)
_old = (pathlib.Path(__file__).parent / "index.xml")
_old = _old.read_text() if _old.exists() else ""
OLDT = dict((src, t) for t, src in re.findall(r'time="([^"]+)">\s*<source>([^<]+)</source>', _old))
cats = []
for d, repo, desc in P:
    sha = subprocess.check_output(["git", "-C", str(M / d), "rev-parse", "HEAD"], text=True).strip()
    f = next((M / d).glob("*.jsfx")); ver = re.search(r"^//version: (\S+)", f.read_text(), re.M).group(1)
    src = f"https://github.com/KevinMeneses/{repo}/raw/{sha}/{f.name}"
    name = "Nube " + d[4:].replace("DeEss", "De-Ess")
    cats.append(f'''  <category name="{name}">
    <reapack name="{f.name}" type="effect" desc="{name} - {desc}">
      <metadata><link rel="website">https://github.com/KevinMeneses/{repo}</link></metadata>
      <version name="{ver}" author="Kev Meneses" time="{OLDT.get(src, now)}">
        <source>{src}</source>
      </version>
    </reapack>
  </category>''')
(pathlib.Path(__file__).parent / "index.xml").write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<index version="1" name="Nube plugins">
{chr(10).join(cats)}
  <metadata>
    <link rel="website">https://github.com/KevinMeneses/nube-plugins</link>
  </metadata>
</index>
''')
print("ok")
