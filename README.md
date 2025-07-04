# Zaptube

**Zaptube** é uma ferramenta simples de linha de comando para baixar vídeos, playlists ou apenas o áudio de diversos sites usando [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).  
Ela permite extrair mídias em diferentes qualidades ou formatos, obter metadados dos vídeos e muito mais — tudo direto do terminal.

## 🚀 Funcionalidades

- 🎞️ Baixe vídeos individuais ou playlists completas
- 🎧 Extraia somente o áudio em formato MP3
- 📊 Veja informações detalhadas do vídeo (título, duração, uploader, etc.)
- 🔽 Escolha a qualidade de download (4K, 1080p, 720p, etc.)
- 📁 Salve os arquivos em uma pasta personalizada

## 📦 Requisitos

- Python 3.7 ou superior
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [`ffmpeg`](https://ffmpeg.org/) (necessário para extração de áudio)

Instale as dependências:
```bash
pip install yt-dlp
```

> Certifique-se de que o `ffmpeg` está instalado e disponível no PATH do sistema.

## 📥 Uso

```bash
python zaptube.py [URL] [OPÇÕES]
```

### Exemplos básicos

- Baixar um vídeo simples:
  ```bash
  python zaptube.py https://exemplo.com/video
  ```

- Baixar apenas o áudio:
  ```bash
  python zaptube.py https://exemplo.com/video -a
  ```

- Baixar uma playlist (limitada a 5 vídeos):
  ```bash
  python zaptube.py https://exemplo.com/playlist -p -m 5
  ```

- Exibir apenas informações do vídeo:
  ```bash
  python zaptube.py https://exemplo.com/video -i
  ```

### Opções

| Opção                | Descrição                                        |
|----------------------|--------------------------------------------------|
| `-o`, `--output`     | Pasta de saída (padrão: `downloads`)             |
| `-q`, `--quality`    | Qualidade do vídeo: `best`, `720p`, `4k`, etc.   |
| `-a`, `--audio-only` | Baixar apenas o áudio (formato MP3)              |
| `-p`, `--playlist`   | Tratar a URL como playlist                       |
| `-i`, `--info-only`  | Exibir apenas as informações, sem baixar         |
| `-m`, `--max-videos` | Número máximo de vídeos a baixar da playlist     |

## 📄 Exemplo de Saída

```
Título: Vídeo Incrível
Duração: 435 segundos
Uploader: CanalLegal
Descrição: Este é um vídeo excelente sobre...
```

## 📁 Estrutura do Projeto

``` zaptube/
├── zaptube.py        # Script principal
├── downloads/        # Pasta padrão de saída
└── README.md         # Este arquivo
```

