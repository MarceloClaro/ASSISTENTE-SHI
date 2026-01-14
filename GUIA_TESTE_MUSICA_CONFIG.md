# Guia de Teste - Configuração de Música Local

## 🎯 Objetivo
Validar que a configuração de caminho de música local funciona corretamente na interface GUI.

## ✅ Testes Automatizados (JÁ COMPLETOS)

Todos os testes de integração foram executados com sucesso:

```
✓ GUI Display Model - Config I/O (Teste 1)
✓ Music Player - Custom Path (Teste 2)  
✓ Music Scan - Custom Path Integration (Teste 3)
✓ Full Workflow Integration (Teste 4)

Total: 4/4 testes passaram ✅
```

Para re-executar:
```bash
python test_music_config_integration.py
```

---

## 🧪 Testes Manuais na GUI

### Pré-requisitos
1. ✅ Python 3.13.3 venv ativo
2. ✅ Pasta com arquivos MP3 local (e.g., `C:\Users\seu_user\Música`)
3. ✅ Aplicação pode ser iniciada

### Teste 1: Abrir Dialog de Configurações
**Passos:**
1. Execute: `python main.py --mode gui --protocol websocket`
2. Aguarde GUI carregar (≈5 segundos)
3. Clique no botão "⚙️" (Configurações) no canto superior direito
4. Dialog modal deve aparecer sobreposto

**Esperado:**
- ✅ Dialog com fundo semi-transparente (opacidade)
- ✅ Título "Configurações de Sistema"
- ✅ Seção "🎵 Caminho de Música Local"
- ✅ TextField com caminho padrão pré-preenchido
- ✅ Botão "Procurar" (desabilitado por enquanto)
- ✅ Botões "Cancelar" e "Salvar"

### Teste 2: Editar Caminho de Música
**Passos:**
1. Com dialog aberto, localize o TextField de música
2. Selecione todo o texto (Ctrl+A)
3. Digite um novo caminho válido, exemplo:
   ```
   C:\Users\seu_user\Música
   ```
4. Verifique que o texto foi atualizado

**Esperado:**
- ✅ Campo aceita entrada de texto
- ✅ Novo caminho é exibido no TextField
- ✅ Sem mensagens de erro

### Teste 3: Salvar Configuração
**Passos:**
1. Com novo caminho no TextField, clique "Salvar"
2. Dialog deve fechar automaticamente
3. Verifique que arquivo foi criado:
   ```bash
   # PowerShell
   Get-Content config\music_config.json
   ```

**Esperado:**
- ✅ Dialog fecha
- ✅ Arquivo `config/music_config.json` existe
- ✅ Contém JSON com novo caminho:
   ```json
   {
     "music_path": "C:\\Users\\seu_user\\Música",
     "version": "1.0"
   }
   ```

### Teste 4: Persistência Entre Sessões
**Passos:**
1. Feche a aplicação (Ctrl+C no terminal)
2. Re-abra: `python main.py --mode gui --protocol websocket`
3. Clique em "⚙️" para abrir Settings novamente
4. Verifique o caminho no TextField

**Esperado:**
- ✅ Caminho anterior está pré-preenchido
- ✅ Confirmação de persistência funcionando

### Teste 5: Testar Reprodução com Novo Caminho
**Passos:**
1. Certifique-se que tem arquivos MP3 no diretório configurado
2. Na interface principal, use o comando de música:
   ```
   Reproduzir [nome da música]
   ```
3. Observar logs do console

**Esperado:**
- ✅ MusicPlayer busca no novo diretório
- ✅ Se música existe localmente, reproduz
- ✅ Logs mostram: "usando modo offline" ou caminho customizado

### Teste 6: Cancelar sem Salvar
**Passos:**
1. Abra Settings (⚙️)
2. Altere o caminho para algo diferente
3. Clique "Cancelar" (não "Salvar")
4. Abra Settings novamente

**Esperado:**
- ✅ Dialog fecha sem salvar
- ✅ Próximo acesso mostra caminho anterior
- ✅ Arquivo JSON não foi modificado

### Teste 7: Validação de Caminho Inválido (Futuro)
**Nota:** Atualmente não há validação visual em tempo real no TextField.
O MusicPlayer validará quando usar o caminho.

**Esperado (quando implementado):**
- Campo avermelhado se caminho não existe
- Mensagem de erro abaixo do campo
- Botão "Salvar" desabilitado

---

## 🔍 Checklist de Validação

### Interface GUI
- [ ] Dialog modal aparece ao clicar ⚙️
- [ ] TextField mostra caminho padrão ou salvo anteriormente
- [ ] Texto pode ser editado livremente
- [ ] Botões funcionam (Salvar/Cancelar)
- [ ] Dialog fecha após ação

### Persistência
- [ ] Arquivo `config/music_config.json` criado
- [ ] JSON é válido e formatado
- [ ] Caminho é recarregado entre sessões
- [ ] Múltiplas alterações/saves funcionam

### Integração com MusicPlayer
- [ ] MusicPlayer usa novo caminho para busca
- [ ] Músicas locais são encontradas no novo diretório
- [ ] Logs mostram operações customizadas
- [ ] Fallback ainda funciona se local falha

### Tratamento de Erros
- [ ] Diretório inválido é rejeitado (retorna False)
- [ ] App não crasheia com entrada inválida
- [ ] Caminho anterior é mantido se falho

---

## 📊 Comparação: Antes vs Depois

### Antes
```
❌ Caminho hardcoded em music_player.py
❌ Sem opção GUI para usuário mudar
❌ Usuário precisa editar código-fonte
❌ Sem persistência entre sessões
```

### Depois
```
✅ Dialog GUI para entrada de caminho
✅ Persistência em JSON (config/music_config.json)
✅ Carregamento automático ao iniciar
✅ Integração total com MusicPlayer
✅ Validação de existência de diretório
✅ Tratamento de erros robusto
```

---

## 🚀 Problema Encontrado & Resolvido

Durante a implementação encontrou-se:
1. **Issue:** MusicPlayer escaneava sempre `self.cache_dir`
2. **Solução:** Adicionado `get_music_search_path()` que prioriza caminho customizado
3. **Teste:** Validado que _scan_local_music() usa novo caminho

---

## 📝 Logs Esperados

### Ao salvar configuração
```
Caminho de música aplicado ao player: C:\Users\...\Música
```

### Ao usar reprodutor com novo caminho
```
Caminho de música customizado: C:\Users\...\Música
```

### Se caminho inválido
```
Caminho customizado não existe: /caminho/inexistente
```

---

## 🔧 Troubleshooting

### Dialog não aparece
- [ ] Verificar se botão ⚙️ existe no QML
- [ ] Confirmar que displayModel é setado no QML
- [ ] Verificar console para erros Python

### Configuração não é salva
- [ ] Confirmar que diretório `config/` tem permissão de escrita
- [ ] Verificar se JSON é válido com: `Get-Content config\music_config.json`
- [ ] Ver erros em console do Python

### MusicPlayer não usa novo caminho
- [ ] Confirmar que `set_custom_music_path()` retorna True
- [ ] Verificar logs do reprodutor
- [ ] Confirmar diretório existe e tem arquivos MP3

### Erro: "name 'Path' is not defined"
- [ ] Restaurar import: `from pathlib import Path` em gui_display_model.py
- [ ] Re-executar testes: `python test_music_config_integration.py`

---

## ✨ Resumo

A funcionalidade de configuração de música foi implementada com sucesso:

| Aspecto | Status |
|---------|--------|
| GUI Dialog | ✅ Completo |
| Data Binding | ✅ Completo |
| Persistência JSON | ✅ Completo |
| Validação | ✅ Completo |
| Integração | ✅ Completo |
| Testes | ✅ 4/4 Passando |
| Documentação | ✅ Completa |

**Próximo Passo:** Abrir `python main.py --mode gui --protocol websocket` e testar!
