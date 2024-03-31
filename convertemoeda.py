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
