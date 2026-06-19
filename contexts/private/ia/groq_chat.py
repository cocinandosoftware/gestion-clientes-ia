from django.conf import settings
from groq import Groq


class GroqChatError(Exception):
    pass


def chat_with_groq(user_message):
    
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise GroqChatError('La API key de Groq no está configurada.')

    client = Groq(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': 'Eres un asistente útil. Responde en español de forma clara y breve.',
                },
                {
                    'role': 'user',
                    'content': user_message,
                },
            ],
            temperature=0.7,
        )
    except Exception as error:
        raise GroqChatError('No se pudo obtener respuesta de Groq.') from error

    reply = completion.choices[0].message.content
    if not reply:
        raise GroqChatError('Groq devolvió una respuesta vacía.')

    return reply.strip()
