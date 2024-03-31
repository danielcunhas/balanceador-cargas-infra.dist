# Relatório de Implementação: Infraestrutura Distribuída com Balanceamento de Carga

Daniel da Cunha Santos - RA: 10085553 - TIA: 32127928

## Descrição da Implementação
A implementação consistiu na criação de uma infraestrutura distribuída na AWS para hospedar um serviço web de conversão de moeda, com balanceamento de carga realizado pelo Nginx. A infraestrutura inclui um servidor frontend como balanceador de carga e dois servidores backend executando o serviço de conversão de moeda. O Nginx foi configurado para distribuir o tráfego entre os servidores backend, garantindo alta disponibilidade e escalabilidade.

## Dificuldades Encontradas:
Durante a implementação, enfrentei dificuldades com a integração de APIs externas para obter as taxas de câmbio em tempo real. A maioria das APIs exigia uma chave de acesso (API key), o que complicava a integração. Optei por uma solução alternativa de definir taxas de câmbio fixas no código do serviço de conversão de moeda para contornar essa dificuldade já que o foco desta atividade era o funcionamento dos servidores usando o balanceamento de carga.

## Execução do Serviço:
1. Consulta do valor do dólar a partir de uma máquina do cliente e a resposta vindo do backend1.
 
2. Consulta de outro valor do dólar a partir da mesma máquina do cliente e a resposta vindo do backend2.
    

3. Serviços em execução:
 

### Arquivo WebService convertemoeda.py:
```
from flask import Flask, jsonify
app = Flask(__name__)
# Função para converter o valor de BRL para USD e EUR usando as taxas fixas
def converteMoeda(valor_brl):
    valor_usd = valor_brl / taxas_fixas['USD']
    valor_eur = valor_brl / taxas_fixas['EUR']
    # Limitando os resultados a duas casas decimais
    valor_usd = round(valor_usd, 2)
    valor_eur = round(valor_eur, 2)
    return {'real': valor_brl, 'dolar': valor_usd, 'euro': valor_eur}

@app.route('/convertemoeda/<valor>')
def convertemoeda(valor):
    try:
        valor_brl = float(valor)
        valores_convertidos = converteMoeda(valor_brl)
        resposta = {
            'conversao': {
                'real': f"R$ {valores_convertidos['real']:.2f}",
                'dolar': f"US$ {valores_convertidos['dolar']:.2f}",
                'euro': f"€ {valores_convertidos['euro']:.2f}",
                'maquina': 'back-end2'
            }
        }
        return jsonify(resposta), 200
    except ValueError:
        return jsonify({'error': 'O valor deve ser um número inteiro ou um número decimal.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Arquivo de Configuração do Nginx (load-balancer.conf):
```
upstream backend {
    server 54.164.72.85:5000;
    server 44.212.60.214:5000;
}

server {
    listen 80;
    server_name 52.55.238.140;
    location / {
        proxy_pass http://backend;
    }
}
```
## Conclusão:
A implementação da infraestrutura distribuída com balanceamento de carga foi concluída com sucesso. Embora tenhamos enfrentado desafios com a integração de APIs externas, conseguimos contornar essas dificuldades com soluções alternativas. O serviço web de conversão de moeda está funcionando corretamente, e o balanceamento de carga está distribuindo o tráfego de forma eficiente entre os servidores backend.

## Informações finais: 
Link github: https://github.com/danielcunhas/balanceador-cargas-infra.dist

No github é possível encontrar:
- convertemoeda.py
- Load-balancer.conf
- Video mostrando serviços em funcionamento.
	


