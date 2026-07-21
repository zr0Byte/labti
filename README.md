🇧🇷 **Português** | 🇺🇸 [English](README_en.md)

# Lab Dashboard — Sistema de Monitoramento de Laboratório de Informática

> Dashboard em tempo real para monitorar o status das máquinas de um laboratório de informática escolar, construído com Firebase/Firestore e Python.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Firebase](https://img.shields.io/badge/firebase-firestore-orange)

---

## Sobre o projeto

Esse projeto nasceu de uma necessidade real do meu trabalho: eu administro um laboratório de informática com 13 computadores e precisava de uma forma rápida e visual de saber quais máquinas estavam online, offline ou com problemas — sem precisar checar manualmente uma por uma.

O sistema é composto por:
- Um **dashboard web** (`index.html`) que exibe o status de cada PC em tempo real, consumindo dados do Firebase/Firestore
- Um **script Python** (`ping_agent.py`) que roda periodicamente, testa a conectividade de cada máquina e atualiza o status no banco de dados

## Screenshots

### Visão geral do dashboard

<img width="1361" height="766" alt="dashboard" src="https://github.com/user-attachments/assets/d925482f-0510-43cc-8820-b5e627e8ab7e" />


O painel principal mostra o total de máquinas, quantas estão funcionando, em manutenção ou indisponíveis, além de filtros de busca e opções de exportação (Excel/PDF).

### Detalhe dos cards (online vs offline)

<img width="661" height="182" alt="cards" src="https://github.com/user-attachments/assets/0bf3c17a-7919-466e-9bc0-98d0e8f94930" />


Cada card exibe informações técnicas da máquina (CPU, RAM, armazenamento), IP atual, status e horário da última atualização.

## Meu papel no projeto (transparência)

Quero ser transparente sobre como esse projeto foi construído, porque acho isso mais valioso do que parecer algo que não é:

- **Eu identifiquei o problema** e defini os requisitos: monitorar 13 máquinas, saber status em tempo real, resolver via web
- **Eu tomei as decisões técnicas de arquitetura**: escolher Firebase/Firestore, decidir migrar de IP fixo para hostname (após diagnosticar que IPs por DHCP quebravam o ping)
- **Eu testei e validei tudo no ambiente real** do laboratório, incluindo troubleshooting de rede (firewall ICMPv4, resolução de hostname)
- **Eu decidi as escolhas de design** (paleta cyber teal/navy, tipografia, comportamento visual)
- Como meu nível de programação ainda é básico, **usei assistência de IA (Claude/Anthropic) para a implementação do código**, revisando, testando e ajustando cada parte no meu próprio ambiente

Estou ativamente estudando programação, Python, SQL e cibersegurança para evoluir minha capacidade de escrever esse tipo de solução de forma cada vez mais independente.

## Problema técnico resolvido

Um dos desafios mais interessantes do projeto: os PCs recebiam IPs dinâmicos via DHCP, o que quebrava constantemente o sistema de ping (o IP salvo no banco ficava desatualizado).

**Solução:** migrei a lógica para ping por **hostname** (`ping -4 LABXX`) em vez de IP fixo. O agente testa o hostname primeiro; se não responder, tenta o último IP conhecido como fallback, e atualiza o Firestore automaticamente quando detecta um IP novo — sem sobrescrever os outros campos do registro.

### O agente em ação

<img width="738" height="496" alt="ping_agent" src="https://github.com/user-attachments/assets/b3edf592-f28a-4a89-9e40-25f660656b9f" />


Repare no PC-07: o agente detectou que o IP mudou (`10.0.10.231 → 10.0.4.159`) e atualizou automaticamente no banco de dados. Já os PCs 03, 04, 11 e 12 não responderam pelo hostname, então o agente tentou o IP antigo salvo como fallback antes de marcar como offline.

## Tecnologias usadas

- **Frontend:** HTML, CSS (variáveis customizadas), JavaScript
- **Backend/Dados:** Firebase / Firestore
- **Automação:** Python (`ping_agent.py`)
- **Infraestrutura:** Resolução de hostname, regras de firewall Windows (ICMPv4)

## Como funciona

1. `ping_agent.py` roda periodicamente e testa a conectividade de cada PC (PC-01 a PC-13) via hostname
2. Se o hostname não responder, tenta o último IP conhecido como fallback
3. O resultado (online/offline + IP atual) é salvo no Firestore, sem sobrescrever outros campos
4. O `index.html` consome esses dados em tempo real e exibe status, com animações e badges visuais
5. Um campo opcional permite sobrescrever o hostname manualmente, para máquinas fora do padrão

## Contato

Fique à vontade para entrar em contato caso tenha dúvidas sobre esse projeto ou queira trocar uma ideia sobre TI/cibersegurança.

