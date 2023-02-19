commands = {
            'focus_up': True, 'focus_down': True, 'change_lang': True, 'invoke': True,
            'delete_word': True, 'delete_entry': True, 'keyboard_on': True, 'keyboard_off': True
        }

COMMANDS_MEANING = {
    'focus_up': 'ниже', 'focus_down': 'выше', 'change_lang': 'смени язык', 'invoke': 'нажми',
    'delete_word': 'удали', 'delete_entry': 'удали все',
    'keyboard_on': 'включи клавиатуру', 'keyboard_off': 'выключи клавиатуру'
}

result = '\n'.join(COMMANDS_MEANING[command] for command, boolean in commands.items() if boolean)


print(result)
