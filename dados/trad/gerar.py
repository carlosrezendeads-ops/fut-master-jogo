# junta dados/trad/t*.tsv (pt, es, en, fr, de) e gera dados/idiomas.js (IDIOMAS)
import glob, json, os, re
D = os.path.dirname(os.path.abspath(__file__))
pt, L = [], {"es": [], "en": [], "fr": [], "de": []}
vistos = set()
for f in sorted(glob.glob(os.path.join(D, "t*.tsv"))):
    for n, linha in enumerate(open(f, encoding="utf8").read().splitlines(), 1):
        if not linha.strip(): continue
        c = linha.split("\t")
        if len(c) != 5: print("colunas erradas:", os.path.basename(f), n, linha[:60]); continue
        if c[0] in vistos: continue
        ph = sorted(re.findall(r"\{\d+\}", c[0]))
        if any(sorted(re.findall(r"\{\d+\}", x)) != ph for x in c[1:]):
            print("placeholders diferentes:", os.path.basename(f), n, c[0][:60]); continue
        vistos.add(c[0]); pt.append(c[0])
        for k, x in zip(L, c[1:]): L[k].append(x)
with open(os.path.join(D, "..", "idiomas.js"), "w", encoding="utf8") as o:
    o.write("const IDIOMAS=" + json.dumps({"pt": pt, **L}, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(pt), "frases")
