def get_payday_response(claim_result, mention):
    if claim_result["status"] == "payday_already_claimed":
        return f"¡Maldita sea {mention}!\n¡¿Cuántas veces quierrres cobrrar en una semana?!\nLargate de aquí antes de" \
               f" que te de una patada en el culo. "
    elif claim_result["status"] == "payday_claimed_succesfully":
        return f"¡Buen trabajo {mention}!\n¿Quién dirria que ibas a sobrevivir otra semana? Desde luego no yo JA\nA " \
               f"tus personajes les espera su paga en el cuerpo de Investigaci" \
               f"ón.\n\n{list_character_level_money(claim_result)} "
    elif claim_result["status"] == "user_has_no_characters":
        return f"Emmmmm... ¿Acaso te conozco?\nNo parrece que tengas ningún personaje asignado a tu nombre...\nVuelve" \
               f" después de haber creado un personaje. "
    elif claim_result["status"] == "new_claimer_inserted":
        return f"Veo que es tu primera paga...\nBienvenido al ***Cuerpo de Investigación*** {mention}.\n¡No te la " \
               f"gastes de golpe chico!... O sí, tu verás.\n\n{list_character_level_money(claim_result)} "


def get_report_mission(mission_title: str, characters, time_played: int, report: str):
    msg = f"La misión ***{mission_title}*** ha durado ***{time_played} minutos***.\n\nLos participantes han sido:\n"

    for character in characters:
        msg += f"-> ***{character.character_name}*** (<@{character.user.user_id}>)\n"

    msg += f'***\nReporte de misión***:\n*"{report}"*'

    return msg


def list_character_level_money(claim_result):
    msg = ""
    for element in claim_result['characters']:
        msg += f"-> {element['character_name']} | LvL {element['level']} | {element['money']} cps\n"

    return msg
