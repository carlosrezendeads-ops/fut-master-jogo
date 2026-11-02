# Gera dados/cidades.js (CIDADES, carregado só na criação do clube) e dados/regioes.js (REGIAO_CLUBE): cidades dos 6 países do jogo + estado/região de cada clube (clássico = mesmo estado).
# Fontes: IBGE (todos os municípios do Brasil) e GeoNames cities5000 (cidades com 5 mil+ habitantes).
# Uso: python dados/cidades/cidades.py <pasta com cities5000.txt, admin1.txt, admin2.txt, ibge.json>
import sys, json, os
G = sys.argv[1]
AQUI = os.path.dirname(os.path.abspath(__file__))

A1 = {}
for l in open(os.path.join(G, 'admin1.txt'), encoding='utf-8'):
    c = l.rstrip('\n').split('\t'); A1[c[0]] = c[1]
A2 = {}
for l in open(os.path.join(G, 'admin2.txt'), encoding='utf-8'):
    c = l.rstrip('\n').split('\t'); A2[c[0]] = c[1]

TR = {  # nomes das regiões no idioma local
 'AR': {'Buenos Aires F.D.': 'Buenos Aires', 'Entre Rios': 'Entre Ríos', 'Tucuman': 'Tucumán', 'Cordoba': 'Córdoba', 'Rio Negro': 'Río Negro', 'Neuquen': 'Neuquén'},
 'ES': {'Andalusia': 'Andalucía', 'Catalonia': 'Cataluña', 'Basque Country': 'País Vasco', 'Balearic Islands': 'Islas Baleares', 'Canary Islands': 'Canarias', 'Castille-La Mancha': 'Castilla-La Mancha', 'Castille and León': 'Castilla y León', 'Navarre': 'Navarra', 'Aragon': 'Aragón', 'Valencia': 'Comunidad Valenciana', 'Murcia': 'Región de Murcia'},
 'DE': {'Bavaria': 'Bayern', 'North Rhine-Westphalia': 'Nordrhein-Westfalen', 'Saxony': 'Sachsen', 'Baden-Wurttemberg': 'Baden-Württemberg', 'Hesse': 'Hessen', 'Lower Saxony': 'Niedersachsen', 'Saxony-Anhalt': 'Sachsen-Anhalt', 'Thuringia': 'Thüringen', 'State of Berlin': 'Berlin'},
 'FR': {'Brittany': 'Bretagne', 'Normandy': 'Normandie', 'Corsica': 'Corse', 'New Aquitaine': 'Nouvelle-Aquitaine'},
}
# Inglaterra/Gales: distritos -> condado cerimonial (ou Sul/Norte de Gales)
CONDADO = {}
for cond, L in {
 'Greater London': ['Greater London'],
 'Greater Manchester': ['Manchester', 'City and Borough of Salford', 'Borough of Bolton', 'Borough of Bury', 'Borough of Oldham', 'Borough of Rochdale', 'Borough of Stockport', 'Borough of Tameside', 'Borough of Wigan', 'Trafford'],
 'Merseyside': ['Liverpool', 'Knowsley', 'Sefton', 'St. Helens', 'Metropolitan Borough of Wirral'],
 'West Midlands': ['City and Borough of Birmingham', 'Coventry', 'Dudley', 'Sandwell', 'Solihull', 'Walsall', 'Wolverhampton'],
 'West Yorkshire': ['City and Borough of Leeds', 'Bradford', 'Calderdale', 'Kirklees', 'City and Borough of Wakefield'],
 'South Yorkshire': ['Sheffield', 'Barnsley', 'Doncaster', 'Rotherham'],
 'Tyne and Wear': ['Newcastle upon Tyne', 'Gateshead', 'North Tyneside', 'South Tyneside', 'Sunderland'],
 'North Yorkshire': ['North Yorkshire', 'City of York', 'Middlesbrough', 'Redcar and Cleveland'],
 'County Durham': ['County Durham', 'Hartlepool', 'Darlington', 'Stockton-on-Tees'],
 'East Riding of Yorkshire': ['East Riding of Yorkshire', 'City of Kingston upon Hull'],
 'Lincolnshire': ['Lincolnshire', 'North Lincolnshire', 'North East Lincolnshire'],
 'Lancashire': ['Lancashire', 'Blackburn with Darwen', 'Blackpool'],
 'Cheshire': ['Cheshire East', 'Cheshire West and Chester', 'Borough of Halton', 'Warrington'],
 'Nottinghamshire': ['Nottingham', 'Nottinghamshire'],
 'Derbyshire': ['Derby', 'Derbyshire'],
 'Leicestershire': ['City of Leicester', 'Leicestershire', 'District of Rutland'],
 'Staffordshire': ['Stoke-on-Trent', 'Staffordshire'],
 'Shropshire': ['Shropshire', 'Telford and Wrekin'],
 'Bedfordshire': ['Bedford', 'Central Bedfordshire', 'Luton'],
 'Buckinghamshire': ['Buckinghamshire', 'Milton Keynes'],
 'Berkshire': ['Reading', 'Bracknell Forest', 'Royal Borough of Windsor and Maidenhead', 'Slough', 'West Berkshire', 'Wokingham'],
 'Hampshire': ['Hampshire', 'Southampton', 'Portsmouth', 'Isle of Wight'],
 'Dorset': ['Dorset', 'Bournemouth, Christchurch and Poole Council'],
 'Devon': ['Devon', 'Plymouth', 'Borough of Torbay'],
 'Somerset': ['Somerset', 'Bath and North East Somerset', 'North Somerset'],
 'Bristol': ['City of Bristol', 'South Gloucestershire'],
 'Wiltshire': ['Wiltshire', 'Borough of Swindon'],
 'Essex': ['Essex', 'Southend-on-Sea', 'Borough of Thurrock'],
 'Kent': ['Kent', 'Medway'],
 'Cambridgeshire': ['Cambridgeshire', 'Peterborough'],
 'Northamptonshire': ['North Northamptonshire', 'West Northamptonshire'],
 'East Sussex': ['East Sussex', 'Brighton and Hove'],
 'Sul de Gales': ['Cardiff', 'City and County of Swansea', 'Newport', 'Vale of Glamorgan', 'Bridgend county borough', 'Neath Port Talbot', 'Rhondda Cynon Taf', 'Merthyr Tydfil County Borough', 'Caerphilly County Borough', 'Blaenau Gwent', 'Torfaen County Borough', 'Monmouthshire', 'Carmarthenshire', 'Pembrokeshire'],
 'Norte de Gales': ['Wrexham', 'County of Flintshire', 'Denbighshire', 'Conwy', 'Gwynedd', 'Anglesey'],
 'Centro de Gales': ['Sir Powys', 'County of Ceredigion'],
}.items():
    for d in L: CONDADO[d] = cond

PAIS = {'AR': 'ARG', 'GB': 'ENG', 'ES': 'ESP', 'DE': 'GER', 'FR': 'FRA', 'AD': 'ESP', 'MC': 'FRA'}
cid = {k: set() for k in ['BRA', 'ARG', 'ENG', 'ESP', 'GER', 'FRA']}
POP = {}  # população (GeoNames) para mostrar as maiores cidades primeiro
for l in open(os.path.join(G, 'cities5000.txt'), encoding='utf-8'):
    c = l.rstrip('\n').split('\t'); cc = c[8]
    if cc == 'BR': POP[('BR', c[1])] = max(POP.get(('BR', c[1]), 0), int(c[14] or 0))
    if cc not in PAIS: continue
    nome = {'Munich': 'München', 'Nuremberg': 'Nürnberg', 'Dunkirk': 'Dunkerque', 'Cadiz': 'Cádiz'}.get(c[1], c[1])  # nomes locais
    POP[(cc if cc != 'AD' else 'AD', nome)] = max(POP.get((cc, nome), 0), int(c[14] or 0))
    if cc == 'GB':
        if c[10] not in ('ENG', 'WLS'): continue
        reg = CONDADO.get(A2.get(f'GB.{c[10]}.{c[11]}', ''), A2.get(f'GB.{c[10]}.{c[11]}', ''))
        if not reg: continue
    elif cc == 'AD': reg = 'Andorra'
    elif cc == 'MC': reg = "Provence-Alpes-Côte d'Azur"
    else:
        reg = A1.get(f'{cc}.{c[10]}', '')
        reg = TR.get(cc, {}).get(reg, reg)
        if not reg: continue
    cid[PAIS[cc]].add((nome, reg))
UF = {}
for m in json.load(open(os.path.join(G, 'ibge.json'), encoding='utf-8')):
    try: uf = m['microrregiao']['mesorregiao']['UF']
    except Exception: uf = (m.get('regiao-imediata') or {}).get('regiao-intermediaria', {}).get('UF')
    if not uf: continue
    UF[uf['sigla']] = uf['nome']; cid['BRA'].add((m['nome'], uf['sigla']))

# estado/região de cada clube do jogo (Brasil: sigla do estado)
CLUBES = json.load(open(os.path.join(AQUI, 'clubes.json'), encoding='utf-8'))

saida = {}
for k, S in cid.items():
    regs = sorted({r for _, r in S} | set(CLUBES[k].values()))
    idx = {r: i for i, r in enumerate(regs)}
    cc = {'BRA': 'BR', 'ARG': 'AR', 'ENG': 'GB', 'ESP': 'ES', 'GER': 'DE', 'FRA': 'FR'}[k]
    L = sorted(S, key=lambda x: (-POP.get((cc, x[0]), 0), x[0].lower(), x[1]))  # maiores primeiro
    saida[k] = {'r': regs, 'c': [[n, idx[r]] for n, r in L]}
saida['BRA']['nomes'] = UF
js = 'const CIDADES=' + json.dumps(saida, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(os.path.join(AQUI, '..', 'cidades.js'), 'w', encoding='utf-8').write(js)
open(os.path.join(AQUI, '..', 'regioes.js'), 'w', encoding='utf-8').write('const REGIAO_CLUBE=' + json.dumps(CLUBES, ensure_ascii=False, separators=(',', ':')) + ';\n')
print({k: len(v['c']) for k, v in saida.items()}, len(js) // 1024, 'KB')
faltam = {k: [r for r in set(v.values()) if r not in {x for _, x in cid[k]}] for k, v in CLUBES.items()}
print('regiões de clube sem cidade no banco:', faltam)
