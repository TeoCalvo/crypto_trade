# Crypto Tarde

Códigos destinados a coleta e m,doelagem preditiva de bitcoin a partir da API do [https://coinmarketcap.com](https://coinmarketcap.com/). Use com cuidado.

## Setup e execução

### Configuração do ambiente

```bash
conda create --name crypto --file requirements.txt
conda activate crypto
```

### Coleta de dados históricos

```bash
python scrap.py --mode all
```

### Coleta de dados novos

```bash
python scrap.py --mode update
```
