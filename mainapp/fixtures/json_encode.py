import json

data = [
    {"city": "Москва",
     "phone": "+7-888-888-8888",
     "email": "info@geekshop.ru",
     "address": "В пределах МКАД"},

    {"city": "Екатеринбург",
     "phone": "+7-777-777-7777",
     "email": "info_yekaterinburg@geekshop.ru",
     "address": "Близко к центру"},

    {"city": "Владивосток",
     "phone": "+7-999-999-9999",
     "email": "info_vladivostok@geekshop.ru",
     "address": "Близко к океану"},
]

with open('locations_contact.json', 'x', encoding='utf-8') as f:
    json.dump(data, f)
