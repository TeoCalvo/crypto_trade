# Crypto Tarde

Códigos destinados a coleta e m,doelagem preditiva de bitcoin a partir da API do [https://coinmarketcap.com](https://coinmarketcap.com/). Use com cuidado.

## Setup e execução

### Configuração do ambiente

```bash
conda create --name crypto python=3.9
conda activate crypto
pip install -r requirements.txt
```

### Coleta de dados históricos

```bash
python scrap.py --mode all
```

### Coleta de dados novos

```bash
python scrap.py --mode update
```

Todos os dados ficam salvos no banco sqlite `data/crypto.db`.