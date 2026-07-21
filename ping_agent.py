"""
╔══════════════════════════════════════════════════════════╗
║         Lab TI — Agente de Ping                         ║
║  Roda no seu PC e monitora todos os outros              ║
║  Envia resultado para o Firebase a cada X minutos       ║
╚══════════════════════════════════════════════════════════╝

INSTALAÇÃO (só uma vez):
  1. Instale o Python: https://python.org/downloads
     (marque "Add Python to PATH" na instalação)
  2. Abra o CMD e execute:
       pip install requests

COMO USAR:
  - Abra o CMD na pasta deste arquivo
  - Execute: python ping_agent.py
  - Deixe rodando enquanto estiver no lab
  - O site vai mostrar online/offline em tempo real

PERSONALIZAR:
  - INTERVALO_MINUTOS: tempo entre cada verificação
"""

import subprocess
import platform
import time
import requests
import json
from datetime import datetime

# ── Configuração ──────────────────────────────────────────
INTERVALO_MINUTOS = 3          # verifica a cada 3 minutos
TIMEOUT_PING = 1000            # ms para considerar offline (1 segundo)

# Firebase — não altere
FIREBASE_PROJECT = "labdeinformatica-d5545"
FIREBASE_URL = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT}/databases/(default)/documents"
# ─────────────────────────────────────────────────────────


def ping(ip: str) -> bool:
    """Retorna True se o IP responder ao ping."""
    if not ip or ip == '—':
        return False
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    try:
        result = subprocess.run(
            ['ping', param, '1', timeout_param, '1000', ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def get_pcs() -> list:
    """Busca lista de PCs cadastrados no Firebase."""
    try:
        url = f"{FIREBASE_URL}/pcs"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"  ⚠ Erro ao buscar PCs: {resp.status_code}")
            return []
        data = resp.json()
        docs = data.get('documents', [])
        pcs = []
        for doc in docs:
            fields = doc.get('fields', {})
            pc_id = doc['name'].split('/')[-1]
            ip    = fields.get('ip', {}).get('stringValue', '')
            name  = fields.get('name', {}).get('stringValue', pc_id)
            pcs.append({'id': pc_id, 'name': name, 'ip': ip})
        return pcs
    except Exception as e:
        print(f"  ⚠ Erro ao conectar ao Firebase: {e}")
        return []


def save_ping_status(pc_id: str, online: bool):
    """Salva o resultado do ping no Firebase (coleção ping_status)."""
    try:
        url = f"{FIREBASE_URL}/ping_status/{pc_id}"
        body = {
            "fields": {
                "online": {"booleanValue": online},
                "ts":     {"integerValue": str(int(time.time() * 1000))}
            }
        }
        requests.patch(url, json=body, timeout=10)
    except Exception as e:
        print(f"  ⚠ Erro ao salvar status: {e}")


def run_check():
    """Executa uma rodada de ping em todos os PCs."""
    now = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{now}] Verificando PCs...")

    pcs = get_pcs()
    if not pcs:
        print("  Nenhum PC encontrado no Firebase.")
        return

    online_count = 0
    for pc in pcs:
        ip = pc['ip']
        if not ip:
            print(f"  {pc['name']:20} — sem IP cadastrado")
            save_ping_status(pc['id'], False)
            continue

        result = ping(ip)
        status = "🟢 ONLINE " if result else "🔴 OFFLINE"
        print(f"  {pc['name']:20} {ip:16} {status}")
        save_ping_status(pc['id'], result)
        if result:
            online_count += 1

    print(f"\n  ✅ {online_count}/{len(pcs)} PCs online")
    print(f"  Próxima verificação em {INTERVALO_MINUTOS} minuto(s)... (Ctrl+C para parar)")


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║       Lab TI — Agente de Monitoramento      ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"  Intervalo: {INTERVALO_MINUTOS} minuto(s)")
    print("  Pressione Ctrl+C para parar\n")

    while True:
        try:
            run_check()
            time.sleep(INTERVALO_MINUTOS * 60)
        except KeyboardInterrupt:
            print("\n\n  Agente encerrado. Até mais!")
            break
        except Exception as e:
            print(f"\n  ⚠ Erro inesperado: {e}")
            print(f"  Tentando novamente em {INTERVALO_MINUTOS} minuto(s)...")
            time.sleep(INTERVALO_MINUTOS * 60)


if __name__ == '__main__':
    main()
