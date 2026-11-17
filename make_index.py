"""Regenera index.xml (ReaPack) con la versión y el commit actual de cada repo Nube (carpetas hermanas en ~/Music)."""
import subprocess, pathlib, re, datetime
M = pathlib.Path(__file__).resolve().parent.parent
P = [("NubeEQ", "nube-eq", "Parametric EQ, 16 bands, M/S, dynamic"), ("NubeComp", "nube-comp", "Compressor, 5 styles, sidechain, lookahead"),
     ("NubeVerb", "nube-verb", "Algorithmic reverb, 16-line FDN, shimmer, freeze"), ("NubeDeEss", "nube-deess", "De-esser, relative detection, split-band"),
     ("NubeLimit", "nube-limit", "Brickwall limiter, true peak, LUFS meter"), ("NubeDelay", "nube-delay", "Delay, tape / analog / lo-fi, ping-pong, ducking"),
     ("NubeSynth", "nube-synth", "Polyphonic synthesizer, unison, FM, glide")]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
cats = []
for d, repo, desc in P:
    sha = subprocess.check_output(["git", "-C", str(M / d), "rev-parse", "HEAD"], text=True).strip()
    f = next((M / d).glob("*.jsfx")); ver = re.search(r"^//version: (\S+)", f.read_text(), re.M).group(1)
    name = "Nube " + d[4:].replace("DeEss", "De-Ess")
    cats.append(f'''  <category name="{name}">
    <reapack name="{f.name}" type="effect" desc="{name} - {desc}">
      <metadata><link rel="website">https://github.com/KevinMeneses/{repo}</link></metadata>
      <version name="{ver}" author="Kev Meneses" time="{now}">
        <source>https://github.com/KevinMeneses/{repo}/raw/{sha}/{f.name}</source>
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
