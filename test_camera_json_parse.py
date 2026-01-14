import json

# Testar parse do JSON retornado pela câmera
test_json = '{"success": true, "text": "Homem sem camisa sentado no banheiro com luz natural e mobiliário de fundo."}'

result_dict = json.loads(test_json)
if result_dict.get('success') and 'text' in result_dict:
    description = result_dict['text']
    print('✅ Parse correto!')
    print(f'Descrição: {description}')
else:
    print('❌ Parse falhou')
