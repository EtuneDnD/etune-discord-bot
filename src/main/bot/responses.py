from main.logic.usecases.legacy.register_character.response import Response


def get_payday_response(response, mention):
    if response.status == "payday_claimed_succesfully":
        return f"¡Buen trabajo {mention}!\n¿Quién dirria que ibas a sobrevivir otra semana? Desde luego no yo JA\nA " \
               f"tus personajes les espera su paga en el cuerpo de Investigaci" \
               f"ón.\n\n{list_character_level_money(response)} "
    elif response.status == "new_claimer_inserted":
        return f"Veo que es tu primera paga...\nBienvenido al ***Cuerpo de Investigación*** {mention}.\n¡No te la " \
               f"gastes de golpe chico!... O sí, tu verás.\n\n{list_character_level_money(response)} "


def get_payday_response_user_has_no_characters(mention):
    return f"Emmmmm... ¿Acasooo tte cconozco {mention}?\nNo parrece que tengas ningún personaje asignado a tu nombre...\nVuelve" \
           " después de haber creado un personaje. "


def get_payday_response_payday_already_claimed(mention):
    return f"¡Maldita sea {mention}!\n¡¿Cuántas veces quierrres cobrrar en una semana?!\nLargate de aquí antes de" \
           " que te de una patada en el culo. "


def get_register_character_response(response: Response):
    if response.status == "inserted_new_user":
        return f"Bienvenid@ <@{str(response.user_character.user.user_id)}>!\nCuida muy bien de " \
               f"***{response.user_character.character.name} [LvL {str(response.user_character.character.level)}]***. "
    elif response.status == "added_new_character":
        return f"Añadiré a ***{response.user_character.character.name} " \
               f"[LvL {str(response.user_character.character.level)}]*** a la lista de personajes de " \
               f"<@{str(response.user_character.user.user_id)}>."


def get_register_character_response_character_already_exists():
    return f"Amigo, creo que has bebido mucho en la taberna Matojo Despojo... Ese personaje ya existe para ese usuario."


def get_report_mission(mission_title: str, response, time_played: int, report: str):
    if response.status == "rewards_added":
        msg = f"La misión ***{mission_title}*** ha durado ***{time_played} minutos***.\n\nLos participantes han sido:\n"

        for character_user_reward in response.character_user_rewards:
            msg += f"-> ***{character_user_reward.character_name}*** (<@{character_user_reward.user.user_id}>) " \
                   f"[ACPS: {character_user_reward.acps} | TCPS: {character_user_reward.tcps}]\n"

        msg += f'***\nReporte de misión***:\n*"{report}"*'

        return msg
    elif response.status == "character_not_exists":
        return f"¡Maldita sea! ¿¡Me estoy volviendo loco o uno de estos personajes no existe!?"
    elif response.status == "characters_from_same_user":
        return f"No seré yo quien te diga que no, pero... ¿No crees que es un poco raro que varios " \
               f"personajes sean de un mismo usuario? " \
               f"¡Malditos llanerrros y su abundante oxígeno, un usuario ha enloquecido!" \


def list_character_level_money(claim_result):
    msg = ""
    for element in claim_result['characters']:
        msg += f"-> {element['character_name']} | LvL {element['level']} | {element['money']} cps\n"

    return msg
