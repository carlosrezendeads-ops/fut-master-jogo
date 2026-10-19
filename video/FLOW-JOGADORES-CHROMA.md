# Jogadores em chroma key — Google Flow

Vídeos de jogador parado em fundo verde (8s, loop, 720p, sem som), gerados no Google Flow
(flow.google.com, conta carlosrezende.ads@gmail.com, projeto "Oct 17 - 21:32").

## Status (19/10/2026)

| Arquivo | Jogador | Status |
|---|---|---|
| `chroma-jogador-negro.mp4` | Negro, cabelo curto (prompt original) | Pronto — aprovado ("ficou muito bom") |
| `chroma-jogador-loiro.mp4` | Branco, loiro, barba rala, olhos azuis | Pronto |
| — | Asiático, cabelo preto liso undercut, sem barba | Pendente (cota diária do Flow) |
| — | Latino, cabelo ondulado castanho, barba cheia curta | Pendente (cota diária do Flow) |
| — | Árabe, cabelo preto cacheado curto, barba grossa | Pendente (cota diária do Flow) |

## Prompt base

Para cada jogador, só muda a frase "He is a ..." depois de "centered.":

```
Medium shot of a professional soccer player standing still, facing the camera, waist up, centered. He is a [DESCRIÇÃO DO JOGADOR]. He wears a completely plain pure white soccer jersey with no logos, no stripes, no numbers, plain white shorts. Solid flat chroma key green background (#00FF00), even studio lighting, no shadows on the background. Photorealistic, 4K. Animation: he stays in the same position, only subtle idle movements - natural breathing, blinking, eyes looking around slightly, small neck and head turns, a light confident expression change, slight smile. Calm, no walking, no arm gestures. Static camera, no zoom. 8 seconds, seamless loop, ends in the exact same pose as it starts.
```

Descrições dos pendentes:
- `East Asian man in his mid-20s with straight black hair in a short undercut style, clean-shaven, dark brown eyes, slim athletic build`
- `Latino man around 30 years old with medium-length wavy dark brown hair, a short well-trimmed full beard, tan skin, brown eyes, strong athletic build`
- `Middle Eastern man in his late 20s with short curly black hair, a thick dark beard, olive skin, dark eyes, muscular athletic build`

## Como gerar (aprendido)

- Modelo: Veo 3.1 Fast, 16:9, 1 vídeo por vez = 20 créditos.
- Download só até 720p (1080p/4K pedem upgrade de plano).
- Deixar ligado "Return silent videos" (configurações do projeto). Mesmo assim às vezes falha por áudio → botão Retry no card resolve (falha é reembolsada).
- Mandar 1 vídeo por mensagem pro agente do Flow; mensagem gigante com vários vídeos dá aviso de "unusual activity". Se aparecer, recarregar a página.
- Cota diária de vídeo acaba rápido (em 18/10 travou depois de 2 vídeos). Falha por cota não cobra.
