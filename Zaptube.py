#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import yt_dlp
import argparse

class VideoExtractor:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_video(self, url, quality='best', audio_only=False):
        """
        Extrai vídeo de uma URL
        
        Args:
            url (str): URL do vídeo
            quality (str): Qualidade desejada ('best', 'worst', '720p', etc.)
            audio_only (bool): Se True, baixa apenas o áudio
        """
        
        # Configurações do yt-dlp
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'format': self._get_format_selector(quality, audio_only),
            'writeinfojson': True, 
            'writethumbnail': True,
        }
        
        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Obter informações do vídeo
                info = ydl.extract_info(url, download=False)
                print(f"Título: {info.get('title', 'N/A')}")
                print(f"Duração: {info.get('duration', 'N/A')} segundos")
                print(f"Uploader: {info.get('uploader', 'N/A')}")
                print(f"Descrição: {info.get('description', 'N/A')[:100]}...")
                
                # Baixar o vídeo
                print(f"\nIniciando download...")
                ydl.download([url])
                print("Download concluído!")
                
        except Exception as e:
            print(f"Erro ao extrair vídeo: {str(e)}")
            return False
        
        return True
    
    def extract_playlist(self, url, max_videos=None):
        """
        Extrai playlist completa ou limitada
        
        Args:
            url (str): URL da playlist
            max_videos (int): Número máximo de vídeos para baixar
        """
        
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'),
            'format': 'best[height<=720]',
        }
        
        if max_videos:
            ydl_opts['playlistend'] = max_videos
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print("Playlist baixada com sucesso!")
        except Exception as e:
            print(f"Erro ao extrair playlist: {str(e)}")
            return False
            
        return True
    
    def get_video_info(self, url):
        """
        Obtém informações do vídeo sem baixar
        
        Args:
            url (str): URL do vídeo
            
        Returns:
            dict: Informações do vídeo
        """
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description'),
                    'formats': [f"{f['format_id']} - {f.get('height', 'N/A')}p" 
                              for f in info.get('formats', [])],
                }
        except Exception as e:
            print(f"Erro ao obter informações: {str(e)}")
            return None
    
    def _get_format_selector(self, quality, audio_only):
        """Define o seletor de formato baseado na qualidade desejada"""
        if audio_only:
            return 'bestaudio/best'
        
        quality_map = {
            'best': 'best',
            'worst': 'worst',
            '4k': 'best[height<=2160]',
            '1080p': 'best[height<=1080]',
            '720p': 'best[height<=720]',
            '480p': 'best[height<=480]',
            '360p': 'best[height<=360]',
        }
        
        return quality_map.get(quality, 'best')

def main():
    parser = argparse.ArgumentParser(description='Extrator de vídeos de sites')
    parser.add_argument('url', help='URL do vídeo ou playlist')
    parser.add_argument('-o', '--output', default='downloads', 
                       help='Diretório de saída (padrão: downloads)')
    parser.add_argument('-q', '--quality', default='best',
                       choices=['best', 'worst', '4k', '1080p', '720p', '480p', '360p'],
                       help='Qualidade do vídeo')
    parser.add_argument('-a', '--audio-only', action='store_true',
                       help='Baixar apenas áudio')
    parser.add_argument('-p', '--playlist', action='store_true',
                       help='Tratar como playlist')
    parser.add_argument('-i', '--info-only', action='store_true',
                       help='Mostrar apenas informações sem baixar')
    parser.add_argument('-m', '--max-videos', type=int,
                       help='Número máximo de vídeos da playlist')
    
    args = parser.parse_args()
    
    extractor = VideoExtractor(args.output)
    
    if args.info_only:
        info = extractor.get_video_info(args.url)
        if info:
            print("=== INFORMAÇÕES DO VÍDEO ===")
            for key, value in info.items():
                if key == 'formats':
                    print(f"{key.upper()}:")
                    for fmt in value[:10]:  
                        print(f"  - {fmt}")
                else:
                    print(f"{key.upper()}: {value}")
    
    elif args.playlist:
        extractor.extract_playlist(args.url, args.max_videos)
    
    else:
        extractor.extract_video(args.url, args.quality, args.audio_only)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=== EXEMPLO DE USO ===")
        extractor = VideoExtractor()
        
        url = input("Digite a URL do vídeo: ").strip()
        
        if url:
            print("\n=== INFORMAÇÕES DO VÍDEO ===")
            info = extractor.get_video_info(url)
            if info:
                print(f"Título: {info['title']}")
                print(f"Duração: {info['duration']} segundos")
                print(f"Uploader: {info['uploader']}")
                
                choice = input("\nDeseja baixar o vídeo? (s/N): ").lower()
                if choice in ['s', 'sim', 'y', 'yes']:
                    extractor.extract_video(url)
    else:
        main()
