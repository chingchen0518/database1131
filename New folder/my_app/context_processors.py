# my_app/context_processors.py

def session_processor(request):
    return {
        'session': request.session
    }