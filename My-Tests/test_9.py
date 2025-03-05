#### This will Only Work with API With Header: Accept-Language ####

from flask import Flask, request;

from flask_babel import Babel, gettext;

app = Flask(__name__);

app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
# app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'


babel = Babel();

def get_locale():
    return request.accept_languages.best_match(['ar', 'en'], default='en');
    # return "ar";

babel.init_app(app=app, locale_selector=get_locale, default_translation_directories='translations');

# translations = Translations.load(dirname='translations', locales=['en', 'ar']);
# translations.install();
@app.route('/')
def index():
    return gettext('Salam Alekoum');

# print(text_here);
with app.app_context():
    print(babel.list_translations());
    print(babel.default_locale);

app.run(host='0.0.0.0', port=5001);