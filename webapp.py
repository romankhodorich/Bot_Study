from quart import Quart, request
import ast
from settings import *
import bot
app = Quart(__name__)


@app.route('/', methods=['POST', 'GET'])
async def handle_request():

    params = request.args.get('params', '')
    try:
        params_dict = ast.literal_eval(params)
        # Извлекаем параметры из POST-запроса
        link = params_dict.get('link', '')
        user_name = params_dict.get('user_name', '')
        ticket_name = params_dict.get('ticket_name', '')
        status = params_dict.get('status', '')
        ticket_number = params_dict.get('ticket_number', '')
        add_text = params_dict.get('add_text', '')

        # Формируем сообщение для отправки
        message = f'''
<a href='{link}'><b>Escadro Support #{ticket_number}: {ticket_name}</b></a>

Статус: {status}

Автор: {user_name}
{add_text}'''

        print(f'''message:
              {message}''')
        # Отправка сообщений
        actives = await bot.aids()
        print(f'Active IDS from bot.py: {actives}')
        await bot.send_msg(message, actives)

        print(
            '------------------------------Message sent-----------------------------------')

        return message, 200
    except Exception as e:
        return f'Error: {str(e)}', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
