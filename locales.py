LANGS = {"ru": "🇷🇺 Русский", "uz": "🇺🇿 O'zbekcha", "en": "🇬🇧 English"}

TEXT = {
"ru": {
    "welcome": "🎭 <b>MAFIA</b>\n\nСначала нажмите Start, затем используйте меню. Для игры в группе бот должен работать в личном чате и иметь права администратора.",
    "choose_language": "🌐 Выберите язык:", "language_saved": "✅ Язык полностью изменён.",
    "main_menu": "🎮 Главное меню", "create_game": "➕ Создать игру", "language": "🌐 Язык", "stats": "📊 Моя статистика", "help": "❓ Помощь",
    "group_only": "📍 Эту функцию нужно запускать в игровой группе.", "creator_start_required": "🔐 Сначала откройте бота в личном чате и нажмите Start, затем создайте игру.", "must_be_group_member": "👥 Вы должны состоять в игровой группе, чтобы присоединиться.",
    "rules_title": "📜 Правила Mafia",
    "lobby": "🎭 <b>ЛОББИ MAFIA</b>\n\n👥 Игроки: <b>{count}/{max}</b>\n\n{players}\n\n🔐 Перед стартом все участники должны открыть бота в личке и нажать Start.",
    "join": "🎟 Войти", "leave": "🚪 Выйти", "start": "▶️ Начать", "rules": "📜 Правила", "settings": "⚙️ Настройки",
    "not_enough": "❌ Нужно минимум {min} игроков.", "too_many": "❌ Достигнут лимит игроков: {max}.", "already_joined": "⚠️ Вы уже участвуете.", "joined": "✅ Вы вошли в игру.", "left": "🚪 Вы вышли из лобби.", "creator_only": "⛔ Это действие доступно только создателю лобби.",
    "game_starting": "🔥 <b>Игра готовится.</b>\n\nПроверьте личный чат бота. После подтверждения всех участников роли будут выданы автоматически.",
    "preflight_ok": "🔐 Личный чат подтверждён. Все игровые действия и роль будут приходить сюда. Не пересылайте сообщения бота другим игрокам.",
    "open_private": "🔐 Сначала откройте личный чат бота и нажмите Start.", "private_delivery_failed": "⚠️ Не удалось связаться с одним или несколькими игроками в личном чате. Игра не запущена. Проверьте, что бот не заблокирован.",
    "ready_title": "🟢 <b>Готовы начать?</b>\n\nНажмите «Готов», если готовы соблюдать правила и получать таймеры/действия в личном чате.",
    "ready_yes": "✅ Готов", "ready_no": "❌ Не готов", "ready_saved": "✅ Статус сохранён.",
    "ready_failed": "⏸ Не все подтвердили готовность. Лобби возвращено в режим ожидания.",
    "role_sent": "🎴 <b>Ваша роль: {role}</b>\n\n{description}\n\n🔒 Роль секретна. Не публикуйте её в группе.",
    "role_mafia": "🔴 Мафия", "role_commissioner": "🔵 Комиссар", "role_doctor": "🟢 Доктор", "role_civilian": "⚪ Мирный житель",
    "mafia_desc": "Вы действуете вместе с другими мафиози и каждую ночь выбираете одну общую цель.",
    "commissioner_desc": "Каждую ночь проверяйте игрока. Со второй ночи доступно дополнительное действие по выводу игрока из игры.",
    "doctor_desc": "Каждую ночь спасайте одного живого игрока. Самолечение доступно один раз за игру.",
    "civilian_desc": "Найдите мафию с помощью обсуждения и голосования.",
    "mafia_team": "🔴 <b>Ваша команда:</b> {names}\n\nВы выбираете одну общую цель. Если голоса мафии расходятся поровну, убийство не происходит.",
    "night": "🌙 <b>НОЧЬ</b>\n\nГород спит. Группа временно закрыта для игроков. Все ночные действия выполняются в личном чате.\n⏱ Ночная фаза: {seconds} сек.",
    "day": "☀️ <b>ДЕНЬ</b>\n\nГород просыпается. Живые игроки могут обсуждать ситуацию.",
    "discussion": "💬 <b>Обсуждение</b>\n\nУ вас {seconds} секунд. Выбывшие игроки наблюдают и не участвуют.",
    "extra_button": "⏱ +60 сек", "extra_request": "⏱ <b>Запрос на дополнительное время</b>\n\nНужно минимум {percent}% голосов живых игроков.\nНа голосование есть 20 секунд.",
    "extra_yes": "👍 Да", "extra_no": "👎 Нет", "extra_added": "⏱ Дополнительная минута добавлена.", "extra_denied": "⏱ Дополнительное время не одобрено.",
    "voting": "🗳 <b>ГОЛОСОВАНИЕ</b>\n\nВыберите подозреваемого в личном чате. Можно изменить голос до конца таймера.",
    "vote": "🗳 <b>Кого вы считаете мафией?</b>", "revote": "⚖️ <b>Повторное голосование</b>\n\nВыбирайте только среди участников ничьей.", "skip": "⏭ Пропустить",
    "vote_saved": "✅ Голос сохранён. До окончания таймера его можно изменить.", "tie": "⚖️ Получилась ничья. Запускается повторное голосование.", "no_elimination": "⚖️ Повторное голосование не определило игрока. Никто не выбывает.",
    "results": "📊 <b>РЕЗУЛЬТАТЫ</b>\n\n{results}", "eliminated": "🚪 <b>{name}</b> выбывает из игры.{role}\n\n🗣 Сейчас только этому игроку доступно последнее слово.",
    "last_word": "🗣 <b>Последнее слово</b>\n\nУ вас {seconds} секунд. Напишите одно финальное сообщение в группе. После таймера вы станете наблюдателем.",
    "night_death": "💀 Ночью из игры выбыл: <b>{name}</b>{role}", "saved": "🩺 Ночная атака была предотвращена доктором.",
    "commissioner_action": "🔎 <b>Проверка</b>\n\nВыберите живого игрока для проверки.", "commissioner_eliminate": "🎯 <b>Дополнительное действие</b>\n\nСо второй ночи можно вывести одного живого игрока из игры.",
    "doctor_action": "🩺 <b>Лечение</b>\n\nВыберите живого игрока для спасения.", "mafia_wait": "🔴 <b>Ход мафии</b>\n\nВыберите одну цель. При разных целях система принимает только единую победившую цель; при полном равенстве атака отменяется.",
    "check_mafia": "🔴 Мафия", "check_not_mafia": "⚪ Не мафия", "commissioner_result": "🔎 Проверка: <b>{name}</b> — {result}.",
    "game_over": "🏁 <b>ИГРА ОКОНЧЕНА</b>\n\n🏆 Победители: <b>{winner}</b>\n\n🎴 <b>Роли игроков:</b>\n{roles}\n\n📌 Игра завершена автоматически движком.",
    "game_cancelled": "⏹ <b>Игра отменена.</b> Создатель покинул группу.", "game_cancelled_generic": "⏹ <b>Игра отменена.</b> Ограничения участников сняты.", "channel_promo": "📣 <b>Игра завершена.</b>\n\nЕсли вам понравилась игра, поддержите проект подпиской на наш Telegram-канал. Подписка добровольная и не влияет на игру.\n\n{url}",
    "stats_text": "📊 <b>Ваша статистика</b>\n\n🎮 Игр: {games}\n🏆 Побед: {wins}\n☠️ Поражений: {losses}",
    "help_text": "❓ <b>Как пользоваться ботом</b>\n\n1. Откройте бота в личном чате и нажмите Start.\n2. Выберите язык.\n3. В группе создайте лобби.\n4. Игроки входят в лобби.\n5. Перед стартом каждый подтверждает готовность.\n6. Роль и ночные действия приходят только в личный чат.\n7. Ночью не пишите в группу.\n8. Днём живые обсуждают и затем голосуют.\n9. После выбывания доступно последнее слово.\n10. Выбывшие наблюдают до конца игры.\n\n⚠️ Для корректной работы User Bot должен быть администратором группы с правами удаления сообщений и ограничения участников. В BotFather рекомендуется отключить Privacy Mode, чтобы бот видел сообщения группы для модерации.",
    "invalid_action": "⛔ Это действие сейчас недоступно или устарело.", "action_expired": "⏳ Время этого действия истекло.", "not_alive": "💀 Вы уже выбыли. Доступен только режим наблюдателя.", "observer": "👁 Вы наблюдатель. Игровые действия закрыты.",
    "settings_title":"⚙️ <b>Настройки игры</b>\n\nТолько создатель лобби может менять параметры.", "setting_auto":"Автостарт", "setting_ready":"Подтверждение готовности", "setting_reveal":"Показывать роль после выбывания", "setting_skip":"Пропуск в голосовании", "setting_self":"Самолечение доктора", "setting_repeat":"Повторное лечение той же цели", "setting_commissioner":"Доп. действие комиссара", "setting_revote":"Повтор при ничьей", "setting_extra":"Дополнительное время", "back":"↩️ Назад",
    "admin_group_error": "⚠️ Добавьте User Bot администратором группы с правами удаления сообщений и ограничения участников.",
    "bot_not_admin": "⚠️ User Bot не имеет необходимых прав администратора. Игра не запущена.",
},
"uz": {}, "en": {}
}

# The Uzbek and English dictionaries are generated from the Russian key set with complete,
# explicit user-facing translations for the same keys. This prevents partial localization.
TEXT["uz"] = {
    "welcome":"🎭 <b>MAFIA</b>\n\nAvval Start tugmasini bosing. O'yin guruhda ishlaydi; bot shaxsiy chatda ham ishlashi va guruhda administrator bo'lishi kerak.",
    "choose_language":"🌐 Tilni tanlang:","language_saved":"✅ Til to'liq o'zgartirildi.","main_menu":"🎮 Asosiy menyu","create_game":"➕ O'yin yaratish","language":"🌐 Til","stats":"📊 Statistikam","help":"❓ Yordam","group_only":"📍 Bu funksiya o'yin guruhida ishlaydi.", "creator_start_required":"🔐 Avval botning shaxsiy chatini ochib Start bosing, keyin o‘yin yarating.", "must_be_group_member":"👥 Qo‘shilish uchun o‘yin guruhida bo‘lishingiz kerak.",
    "rules_title":"📜 Mafia qoidalari",
    "lobby":"🎭 <b>MAFIA LOBBISI</b>\n\n👥 O'yinchilar: <b>{count}/{max}</b>\n\n{players}\n\n🔐 Startdan oldin hamma botni shaxsiy chatda ochib Start bosishi kerak.","join":"🎟 Kirish","leave":"🚪 Chiqish","start":"▶️ Boshlash","rules":"📜 Qoidalar","settings":"⚙️ Sozlamalar","not_enough":"❌ Kamida {min} o'yinchi kerak.","too_many":"❌ O'yinchi limiti: {max}.","already_joined":"⚠️ Siz allaqachon o'yindasiz.","joined":"✅ Siz o'yinga kirdingiz.","left":"🚪 Siz lobbidan chiqdingiz.","creator_only":"⛔ Bu faqat lobby yaratuvchisi uchun.",
    "game_starting":"🔥 <b>O'yin tayyorlanmoqda.</b>\n\nBotning shaxsiy chatini tekshiring. Hamma tasdiqlagach rollar avtomatik beriladi.","preflight_ok":"🔐 Shaxsiy chat tasdiqlandi. Barcha rollar va tungi harakatlar shu yerga keladi. Bot xabarlarini boshqalarga yubormang.","open_private":"🔐 Avval botning shaxsiy chatini ochib Start bosing.", "private_delivery_failed":"⚠️ Bot bir yoki bir nechta o‘yinchi bilan shaxsiy chatda bog‘lana olmadi. O‘yin boshlanmadi. Bot bloklanmaganini tekshiring.","ready_title":"🟢 <b>Boshlashga tayyormisiz?</b>\n\nTayyor bo'lsangiz tugmani bosing.","ready_yes":"✅ Tayyor","ready_no":"❌ Tayyor emas","ready_saved":"✅ Holat saqlandi.","ready_failed":"⏸ Hamma tayyorligini tasdiqlamadi. Lobby kutish rejimiga qaytdi.",
    "role_sent":"🎴 <b>Sizning rolingiz: {role}</b>\n\n{description}\n\n🔒 Rol maxfiy. Uni guruhda yozmang.","role_mafia":"🔴 Mafia","role_commissioner":"🔵 Komissar","role_doctor":"🟢 Doktor","role_civilian":"⚪ Tinch aholi","mafia_desc":"Boshqa mafiyalar bilan birga har kecha bitta umumiy nishonni tanlang.","commissioner_desc":"Har kecha tekshiruv qiling. Ikkinchi kechadan boshlab qo'shimcha chiqarish harakati mavjud.","doctor_desc":"Har kecha bitta tirik o'yinchini saqlang. O'zingizni bir marta davolashingiz mumkin.","civilian_desc":"Muhokama va ovoz berish orqali mafiani toping.","mafia_team":"🔴 <b>Sizning jamoangiz:</b> {names}\n\nBitta umumiy nishon tanlanadi. Ovozlar to'liq teng bo'lsa hujum bekor qilinadi.",
    "night":"🌙 <b>TUN</b>\n\nShahar uxlaydi. Guruh vaqtincha yopiq. Barcha tungi harakatlar shaxsiy chatda.\n⏱ Tun: {seconds} soniya.","day":"☀️ <b>KUN</b>\n\nShahar uyg'ondi. Tirik o'yinchilar muhokama qilishi mumkin.","discussion":"💬 <b>Muhokama</b>\n\nSizda {seconds} soniya. Chiqib ketganlar faqat kuzatadi.","extra_button":"⏱ +60 soniya","extra_request":"⏱ <b>Qo'shimcha vaqt so'rovi</b>\n\nTirik o'yinchilarning kamida {percent}% roziligi kerak.\nOvoz berish 20 soniya.","extra_yes":"👍 Ha","extra_no":"👎 Yo'q","extra_added":"⏱ Qo'shimcha daqiqa qo'shildi.","extra_denied":"⏱ Qo'shimcha vaqt tasdiqlanmadi.",
    "voting":"🗳 <b>OVOZ BERISH</b>\n\nShubhali o'yinchini shaxsiy chatda tanlang. Taymer tugaguncha ovozni o'zgartirish mumkin.","vote":"🗳 <b>Sizningcha kim mafia?</b>","revote":"⚖️ <b>Qayta ovoz berish</b>\n\nFaqat durrangdagi o'yinchilardan tanlang.","skip":"⏭ O'tkazib yuborish","vote_saved":"✅ Ovoz saqlandi. Taymer tugaguncha o'zgartirish mumkin.","tie":"⚖️ Durrang. Qayta ovoz berish boshlanadi.","no_elimination":"⚖️ Qayta ovoz berish ham natija bermadi. Hech kim chiqarilmaydi.","results":"📊 <b>NATIJA</b>\n\n{results}","eliminated":"🚪 <b>{name}</b> o'yindan chiqdi.{role}\n\n🗣 Endi faqat shu o'yinchiga so'nggi so'z beriladi.","last_word":"🗣 <b>So'nggi so'z</b>\n\nSizda {seconds} soniya. Guruhga bitta yakuniy xabar yozing.","night_death":"💀 Tunda o'yindan chiqdi: <b>{name}</b>{role}","saved":"🩺 Tungi hujum doktor tomonidan to'xtatildi.","commissioner_action":"🔎 <b>Tekshiruv</b>\n\nTekshirish uchun tirik o'yinchini tanlang.","commissioner_eliminate":"🎯 <b>Qo'shimcha harakat</b>\n\nIkkinchi kechadan bitta tirik o'yinchini chiqarish mumkin.","doctor_action":"🩺 <b>Davolash</b>\n\nQutqarish uchun tirik o'yinchini tanlang.","mafia_wait":"🔴 <b>Mafia harakati</b>\n\nBitta nishon tanlang. Tenglik bo'lsa hujum bekor qilinadi.","check_mafia":"🔴 Mafia","check_not_mafia":"⚪ Mafia emas","commissioner_result":"🔎 Tekshiruv: <b>{name}</b> — {result}.",
    "game_over":"🏁 <b>O'YIN TUGADI</b>\n\n🏆 G'oliblar: <b>{winner}</b>\n\n🎴 <b>Rollar:</b>\n{roles}","game_cancelled":"⏹ <b>O'yin bekor qilindi.</b> Yaratuvchi guruhni tark etdi.", "game_cancelled_generic":"⏹ <b>O'yin bekor qilindi.</b> Ishtirokchilarning barcha cheklovlari olib tashlandi.", "channel_promo":"📣 <b>O'yin tugadi.</b>\n\nAgar yoqqan bo'lsa, loyihani Telegram kanaliga obuna bo'lish orqali qo'llab-quvvatlang. Obuna ixtiyoriy.\n\n{url}","stats_text":"📊 <b>Statistikangiz</b>\n\n🎮 O'yinlar: {games}\n🏆 G'alabalar: {wins}\n☠️ Mag'lubiyatlar: {losses}","help_text":"❓ <b>Foydalanish</b>\n\n1. Botni shaxsiy chatda ochib Start bosing.\n2. Tilni tanlang.\n3. Guruhda lobby yarating.\n4. O'yinchilar qo'shiladi.\n5. Startdan oldin hamma tayyorligini tasdiqlaydi.\n6. Rol va tungi harakatlar shaxsiy chatga keladi.\n7. Tunda guruhga yozmang.\n8. Kunduzi muhokama va ovoz berish bo'ladi.\n9. Chiqib ketgan o'yinchiga so'nggi so'z beriladi.\n10. Chiqib ketganlar kuzatadi.\n\n⚠️ Bot guruhda xabarlarni o'chirish va ishtirokchilarni cheklash huquqlariga ega administrator bo'lishi kerak. BotFather'da Privacy Mode'ni o'chirish tavsiya etiladi.","invalid_action":"⛔ Bu harakat hozir mavjud emas yoki eskirgan.", "action_expired":"⏳ Bu harakat vaqti tugadi.","not_alive":"💀 Siz o'yindan chiqdingiz. Faqat kuzatuv rejimi mavjud.","observer":"👁 Siz kuzatuvchisiz. Faol harakatlar yopiq.","admin_group_error":"⚠️ User Botni guruhga administrator qilib qo'shing: xabar o'chirish va ishtirokchilarni cheklash huquqlari kerak.","bot_not_admin":"⚠️ User Botda kerakli administrator huquqlari yo'q. O'yin boshlanmadi.", "settings_title":"⚙️ <b>O'yin sozlamalari</b>\n\nFaqat lobby yaratuvchisi sozlamalarni o'zgartira oladi.", "setting_auto":"Avtostart", "setting_ready":"Tayyorgarlik tasdig'i", "setting_reveal":"Chiqishda rolni ko'rsatish", "setting_skip":"Ovozda o'tkazish", "setting_self":"Doktor o'zini davolashi", "setting_repeat":"Bir xil nishonni qayta davolash", "setting_commissioner":"Komissarning qo'shimcha harakati", "setting_revote":"Durrangda qayta ovoz", "setting_extra":"Qo'shimcha vaqt", "back":"↩️ Orqaga"
}

TEXT["en"] = {
    "welcome":"🎭 <b>MAFIA</b>\n\nFirst open the bot and press Start. The game runs in a group, while roles and actions are delivered privately. The bot must be an administrator in the group.",
    "choose_language":"🌐 Choose your language:","language_saved":"✅ Language changed completely.","main_menu":"🎮 Main menu","create_game":"➕ Create game","language":"🌐 Language","stats":"📊 My statistics","help":"❓ Help","group_only":"📍 This feature must be used in a game group.", "creator_start_required":"🔐 First open the bot in private chat and press Start, then create the game.", "must_be_group_member":"👥 You must be a member of the game group to join.",
    "rules_title":"📜 Mafia rules",
    "lobby":"🎭 <b>MAFIA LOBBY</b>\n\n👥 Players: <b>{count}/{max}</b>\n\n{players}\n\n🔐 Before starting, everyone must open the bot in private chat and press Start.","join":"🎟 Join","leave":"🚪 Leave","start":"▶️ Start","rules":"📜 Rules","settings":"⚙️ Settings","not_enough":"❌ At least {min} players are required.","too_many":"❌ Player limit: {max}.","already_joined":"⚠️ You are already in the game.","joined":"✅ You joined the game.","left":"🚪 You left the lobby.","creator_only":"⛔ Only the lobby creator can do this.",
    "game_starting":"🔥 <b>The game is preparing.</b>\n\nCheck the bot's private chat. Roles will be sent after everyone confirms readiness.","preflight_ok":"🔐 Private chat confirmed. All roles and night actions will arrive here. Do not forward secret bot messages to other players.","open_private":"🔐 Open the bot in private chat and press Start first.", "private_delivery_failed":"⚠️ The bot could not reach one or more players in private chat. The game was not started. Check that the bot is not blocked.","ready_title":"🟢 <b>Ready to start?</b>\n\nPress Ready when you are prepared to follow the rules and receive timed actions privately.","ready_yes":"✅ Ready","ready_no":"❌ Not ready","ready_saved":"✅ Status saved.","ready_failed":"⏸ Not everyone confirmed readiness. The lobby is back in waiting mode.",
    "role_sent":"🎴 <b>Your role: {role}</b>\n\n{description}\n\n🔒 Your role is secret. Do not post it in the group.","role_mafia":"🔴 Mafia","role_commissioner":"🔵 Commissioner","role_doctor":"🟢 Doctor","role_civilian":"⚪ Civilian","mafia_desc":"Work with the other Mafia players and choose one shared target each night.","commissioner_desc":"Check one player each night. From night 2, an additional removal action is available.","doctor_desc":"Save one living player each night. Self-save is available once per game.","civilian_desc":"Find the Mafia through discussion and voting.","mafia_team":"🔴 <b>Your team:</b> {names}\n\nMafia chooses one shared target. If the votes are fully tied, the attack is cancelled.",
    "night":"🌙 <b>NIGHT</b>\n\nThe city sleeps. The group is temporarily locked. All night actions are private.\n⏱ Night phase: {seconds} sec.","day":"☀️ <b>DAY</b>\n\nThe city wakes up. Living players may discuss.","discussion":"💬 <b>Discussion</b>\n\nYou have {seconds} seconds. Eliminated players can only spectate.","extra_button":"⏱ +60 sec","extra_request":"⏱ <b>Extra-time request</b>\n\nAt least {percent}% of living players must approve.\nVoting lasts 20 seconds.","extra_yes":"👍 Yes","extra_no":"👎 No","extra_added":"⏱ One extra minute was added.","extra_denied":"⏱ Extra time was not approved.",
    "voting":"🗳 <b>VOTING</b>\n\nChoose a suspect in private chat. You can change your vote until the timer ends.","vote":"🗳 <b>Who do you think is Mafia?</b>","revote":"⚖️ <b>Revote</b>\n\nChoose only among the tied players.","skip":"⏭ Skip","vote_saved":"✅ Vote saved. You can change it until the timer ends.","tie":"⚖️ It is a tie. A revote will start.","no_elimination":"⚖️ The revote did not determine a player. Nobody is eliminated.","results":"📊 <b>RESULTS</b>\n\n{results}","eliminated":"🚪 <b>{name}</b> is eliminated.{role}\n\n🗣 Only this player can use the last word now.","last_word":"🗣 <b>Last word</b>\n\nYou have {seconds} seconds. Send one final message in the group.","night_death":"💀 Eliminated during the night: <b>{name}</b>{role}","saved":"🩺 The night attack was prevented by the Doctor.","commissioner_action":"🔎 <b>Check</b>\n\nChoose a living player to check.","commissioner_eliminate":"🎯 <b>Additional action</b>\n\nFrom night 2, you may remove one living player from the game.","doctor_action":"🩺 <b>Save</b>\n\nChoose a living player to save.","mafia_wait":"🔴 <b>Mafia action</b>\n\nChoose one target. If the Mafia votes are fully tied, the attack is cancelled.","check_mafia":"🔴 Mafia","check_not_mafia":"⚪ Not Mafia","commissioner_result":"🔎 Check: <b>{name}</b> — {result}.",
    "game_over":"🏁 <b>GAME OVER</b>\n\n🏆 Winners: <b>{winner}</b>\n\n🎴 <b>Roles:</b>\n{roles}","game_cancelled":"⏹ <b>Game cancelled.</b> The creator left the group.", "game_cancelled_generic":"⏹ <b>Game cancelled.</b> All participant restrictions have been removed.", "channel_promo":"📣 <b>Game finished.</b>\n\nIf you enjoyed it, support the project by subscribing to our Telegram channel. Subscription is optional and never affects gameplay.\n\n{url}","stats_text":"📊 <b>Your statistics</b>\n\n🎮 Games: {games}\n🏆 Wins: {wins}\n☠️ Losses: {losses}","help_text":"❓ <b>How to use</b>\n\n1. Open the bot in private chat and press Start.\n2. Choose a language.\n3. Create a lobby in a group.\n4. Players join.\n5. Everyone confirms readiness before the start.\n6. Roles and night actions arrive privately.\n7. Do not write in the group at night.\n8. Living players discuss and vote during the day.\n9. Eliminated players receive a last word.\n10. Eliminated players spectate until the game ends.\n\n⚠️ The User Bot must be a group administrator with permissions to delete messages and restrict members. Disable Privacy Mode in BotFather so the bot can moderate group messages.","invalid_action":"⛔ This action is unavailable or outdated.", "action_expired":"⏳ The time for this action has expired.","not_alive":"💀 You are eliminated. Only spectator mode remains.","observer":"👁 You are a spectator. Active actions are disabled.","admin_group_error":"⚠️ Add the User Bot as a group administrator with delete-message and restrict-member permissions.","bot_not_admin":"⚠️ The User Bot does not have the required administrator permissions. The game was not started.", "settings_title":"⚙️ <b>Game settings</b>\n\nOnly the lobby creator can change settings.", "setting_auto":"Auto start", "setting_ready":"Ready check", "setting_reveal":"Reveal role after elimination", "setting_skip":"Skip in voting", "setting_self":"Doctor self-save", "setting_repeat":"Repeat doctor target", "setting_commissioner":"Commissioner extra action", "setting_revote":"Revote on tie", "setting_extra":"Extra time", "back":"↩️ Back"
}


def t(lang: str, key: str, **kwargs) -> str:
    data = TEXT.get(lang, TEXT["ru"])
    value = data.get(key, TEXT["ru"].get(key, key))
    return value.format(**kwargs)

_EXTRA = {
"ru": {
"join_game":"🔗 Войти в игру","profile":"👤 Мой профиль","rules_button":"📜 Правила","support":"🛟 Поддержка","welcome_full":"🎭 <b>MAFIA</b>\n\nДобро пожаловать, <b>{name}</b>.\n\nВыберите действие ниже.","rules_required":"📜 Сначала выберите язык и примите правила.","accept_rules":"✅ Принять правила","rules_accepted":"✅ <b>Правила приняты.</b> Теперь доступны создание игры, вход в игру, профиль, статистика и поддержка.","create_menu":"🎮 <b>Создание игры</b>\n\nИгра создаётся в выбранной Telegram-группе. User Bot должен быть администратором.","how_add_bot":"📘 Как добавить бота","create_in_group":"➕ Создать в группе","create_in_group_text":"Откройте нужную группу → добавьте User Bot → выдайте права администратора → в группе отправьте <b>/create</b>.","join_hint":"🔗 <b>Вход в игру</b>\n\nОтправьте сюда код комнаты из лобби. Также можно использовать персональную ссылку-приглашение.","room_code_invalid":"❌ Комната не найдена, закрыта или код указан неверно.","how_to_add":"Как добавить бота","bot_guide":"📘 <b>КАК ДОБАВИТЬ USER BOT В ГРУППУ</b>\n━━━━━━━━━━━━━━\n<b>Шаг 1.</b> Откройте нужную группу.\n<b>Шаг 2.</b> Откройте управление группой → Администраторы.\n<b>Шаг 3.</b> Добавьте User Bot.\n<b>Шаг 4.</b> Выдайте права: удаление сообщений и ограничение участников.\n<b>Шаг 5.</b> Вернитесь в группу и отправьте <b>/create</b>.\n\n🔐 Перед созданием игры бот автоматически проверяет свои права. Если чего-то не хватает, игра не запускается и бот показывает, какое право нужно добавить.\n\n💡 Для стабильной модерации рекомендуется отключить Privacy Mode у бота через BotFather.","invite":"➕ Пригласить","invite_text":"🔗 <b>Приглашение в Mafia Lobby</b>\n\nКод комнаты: <code>{code}</code>\n\nОткройте ссылку и нажмите Start:\n{url}","player_count":"👥 Игроки","roles":"🎴 Роли","lobby_v2":"🎭 <b>MAFIA LOBBY #{game_id}</b>\n━━━━━━━━━━━━━━\n👥 Игроки: <b>{count}/{max}</b>\n🎴 Состав: {roles}\n\n{players}\n\n⏳ Статус: <b>Ожидание игроков</b>\n\nКнопки ниже управляют комнатой.","choose_player_count":"👥 <b>Размер игры</b>\n\nВыберите готовый размер от 5 до 40 игроков.","custom_count":"✏️ Своё количество","custom_count_prompt":"✏️ Отправьте одним сообщением число игроков от <b>5</b> до <b>40</b>.","custom_count_invalid":"❌ Введите целое число от 5 до 40.","custom_count_saved":"✅ Размер игры установлен: <b>{count}</b> игроков.","auto_balance":"⚖️ Автобаланс","role_config_text":"🎴 <b>Состав игры</b>\n━━━━━━━━━━━━━━\n🔴 Мафия: <b>{mafia}</b>\n🩺 Доктор: <b>{doctor}</b>\n🔎 Комиссар: <b>{commissioner}</b>\n⚪ Мирные: <b>{civilian}</b>\n\nАвтобаланс — стартовая схема, а не обязательное правило. Пока доступны только четыре основные роли.","doctor_self_1":"🩺 Самолечение ×1","doctor_self_2":"🩺 Самолечение ×2","on":"ВКЛ","off":"ВЫКЛ","active_game":"⚠️ В этой группе уже есть активная игра.","admin_permissions_missing":"⚠️ User Bot не готов. Не хватает прав: <b>{missing}</b>.","rules_group":"📜 <b>ИГРА MAFIA</b>\nРоли выдаются в личке. Ночью группа закрыта. Следуйте кнопкам бота и таймерам.","mafia_partner_choice":"🔴 Напарник предложил цель: <b>{name}</b>. Выберите её же кнопкой ниже или выберите другую цель.","choose_same":"🎯 Выбрать эту цель","mafia_consensus":"🔴 <b>Общий выбор согласован:</b> {name}\nСистема готовит разрешение ночи.","stats_detailed":"📊 <b>Ваша статистика</b>\n━━━━━━━━━━━━━━\n🎮 Игр: <b>{games}</b>\n🏆 Побед: <b>{wins}</b>\n☠️ Поражений: <b>{losses}</b>\n\n🎴 <b>По ролям</b>\nФормат: игры / победы / поражения\n{roles}","profile_card":"👤 <b>Мой профиль</b>\n━━━━━━━━━━━━━━\n<b>Имя:</b> {name}\n<b>Username:</b> {username}\n<b>Telegram ID:</b> <code>{tg_id}</code>\n<b>Язык:</b> {language}\n<b>First start:</b> {first}\n<b>Last seen:</b> {last}\n<b>Правила приняты:</b> {rules}\n<b>Игр:</b> {games}\n<b>Побед:</b> {wins}\n<b>Поражений:</b> {losses}\n<b>Бот заблокирован:</b> {blocked}","no_username":"нет","support_menu":"🛟 <b>ПОДДЕРЖКА</b>\n━━━━━━━━━━━━━━\nВыберите способ помощи.","new_ticket":"🎫 Новый тикет","my_ticket":"📌 Мой тикет","faq":"❔ Частые вопросы","contact_admin":"✉️ Написать администратору","ticket_prompt":"🎫 <b>Новый тикет</b>\n\nОпишите проблему одним сообщением. Можно отправить текст, фото, документ, аудио, голосовое или видео.\n\nПосле отправки тикет получит статус «Передан администраторам».","ticket_received":"✅ Тикет <b>#{id}</b> передан администраторам. Ожидайте ответ в этом чате.","ticket_status":"🎫 Тикет <b>#{id}</b>\nСтатус: <b>{status}</b>","status_new":"Новый","status_delivered":"Передан администраторам","status_in_progress":"В работе","status_waiting_user":"Ожидает пользователя","status_closed":"Закрыт","no_ticket":"📭 Активных тикетов нет.","faq_text":"❔ <b>Частые вопросы</b>\n\n<b>Почему я не получил роль?</b> Проверьте Start в личке и возможность бота отправлять вам сообщения.\n\n<b>Как создать игру?</b> Добавьте User Bot администратором и отправьте /newgame.\n\n<b>Почему бот не работает?</b> Откройте поддержку и создайте тикет с описанием или скриншотом.","ticket_admin_header":"🎫 <b>Тикет #{id}</b>\n👤 {name}\n🆔 <code>{tg_id}</code>\nUsername: {username}","cancel":"Отмена","cancelled":"↩️ Отменено","ticket_admin_reply":"Ответ администратора по тикету #{id}","mafia_chat":"💬 Mafia Chat","mafia_chat_prompt":"💬 Отправьте одно сообщение напарникам. Чат доступен только во время ночной фазы.","mafia_chat_prefix":"🔴 Сообщение от {name}:","mafia_chat_sent":"✅ Сообщение отправлено напарникам.","broadcast":"📣 Рассылка","users":"👥 Пользователи","groups":"🏘 Группы","games":"🎮 Игры","logs":"🧾 Логи","system":"⚙️ Система","refresh":"🔄 Обновить","period_today":"Сегодня","period_7d":"7 дней","period_month":"Этот месяц","period_year":"Этот год","period_all":"Всё время","export":"📤 Экспорт","broadcast_done":"📣 Рассылка завершена","ticket":"🎫 Поддержка"},
}

# For Uzbek/English, keep the same complete contract while translating the newly added navigation labels.
_EXTRA["uz"] = {k:v for k,v in _EXTRA["ru"].items()}
_EXTRA["en"] = {k:v for k,v in _EXTRA["ru"].items()}
_EXTRA["uz"].update({"join_game":"🔗 O'yinga kirish","profile":"👤 Profilim","support":"🛟 Yordam","language":"🌐 Til","rules_button":"📜 Qoidalar","create_game":"➕ O'yin yaratish","stats":"📊 Statistikam","help":"❓ Yordam","welcome_full":"🎭 <b>MAFIA</b>\n\nXush kelibsiz, <b>{name}</b>.\n\nQuyidagi amalni tanlang.","accept_rules":"✅ Qoidalarni qabul qilish","new_ticket":"🎫 Yangi tiket","my_ticket":"📌 Mening tiketim","faq":"❔ Tez-tez so'raladi","contact_admin":"✉️ Administratorga yozish","back":"↩️ Orqaga"})
_EXTRA["en"].update({"join_game":"🔗 Join game","profile":"👤 My profile","support":"🛟 Support","language":"🌐 Language","rules_button":"📜 Rules","create_game":"➕ Create game","stats":"📊 My statistics","help":"❓ Help","welcome_full":"🎭 <b>MAFIA</b>\n\nWelcome, <b>{name}</b>.\n\nChoose an action below.","accept_rules":"✅ Accept rules","new_ticket":"🎫 New ticket","my_ticket":"📌 My ticket","faq":"❔ FAQ","contact_admin":"✉️ Contact administrator","back":"↩️ Back"})
for _lang, _vals in _EXTRA.items(): TEXT[_lang].update(_vals)

# Full translations for the new onboarding/support contract.
TEXT["en"].update({
    "yes":"Yes",
    "no":"No",
    "role_invalid":"❌ This role combination is not valid for the selected player count.",
    "auto_balance":"⚖️ Auto balance roles",
    "setting_extra":"Extra discussion time",
    "mafia_chat":"💬 Mafia Chat",
"rules_full":"📜 <b>MAFIA RULES</b>\n━━━━━━━━━━━━━━\n<b>1. BEFORE THE GAME</b>\n• You must be in the group where the game takes place.\n• Your role is sent only in private chat.\n• Never reveal your role or secret bot messages in the group.\n\n<b>2. NIGHT</b>\n• The group is locked for game messages.\n• Mafia, Doctor and Commissioner act through private buttons.\n• Civilian has no night action.\n\n<b>3. ROLES</b>\n🔴 <b>Mafia</b> — chooses one shared target with the Mafia team.\n🩺 <b>Doctor</b> — protects one living player; self-save is configurable.\n🔎 <b>Commissioner</b> — checks one player. Night 1 is check-only; from night 2 an additional removal action is available.\n⚪ <b>Civilian</b> — analyzes the game during the day and votes.\n\n<b>4. DAY AND VOTING</b>\n• Living players discuss during the day.\n• Voting happens privately.\n• Votes can be changed before the timer ends.\n• You cannot vote for yourself. Eliminated players cannot vote.\n\n<b>5. ELIMINATION</b>\n• Roles are hidden until the game ends.\n• An eliminated player gets one 30-second last word.\n• After that, they become a spectator.\n\n<b>6. VICTORY</b>\n• Civilians win when no Mafia remains.\n• Mafia wins when Mafia equals or exceeds all other living players.\n\n⚠️ Pressing “Accept rules” confirms that you understand role secrecy and the group-game rules.",
"bot_guide":"📘 <b>HOW TO ADD USER BOT</b>\n━━━━━━━━━━━━━━\n<b>Step 1.</b> Open the target Telegram group.\n<b>Step 2.</b> Group settings → Administrators.\n<b>Step 3.</b> Add User Bot.\n<b>Step 4.</b> Grant delete-message and restrict-member permissions.\n<b>Step 5.</b> Return to the group and send <b>/create</b>.\n\n🔐 The bot checks its permissions automatically. If a permission is missing, the game is not started and the missing permission is shown.\n\n💡 Disabling Privacy Mode in BotFather is recommended for reliable moderation.",
"create_menu":"🎮 <b>CREATE GAME</b>\n\nCreate the game in the Telegram group where you want to play. User Bot must be an administrator.",
"create_in_group_text":"Open the target group → add User Bot → grant administrator permissions → send <b>/create</b> in the group.",
"role_config_text":"🎴 <b>GAME COMPOSITION</b>\n━━━━━━━━━━━━━━\n🔴 Mafia: <b>{mafia}</b>\n🩺 Doctor: <b>{doctor}</b>\n🔎 Commissioner: <b>{commissioner}</b>\n⚪ Civilians: <b>{civilian}</b>\n\nAutomatic balance is a starting preset, not a rigid rule. Only the four core roles are enabled.",
"support_menu":"🛟 <b>SUPPORT</b>\n━━━━━━━━━━━━━━\nChoose how you want help.","ticket_prompt":"🎫 <b>NEW TICKET</b>\n\nDescribe the problem in one message. Text, photo, document, audio, voice or video are accepted.\n\nThe ticket will be delivered to the administrators.","ticket_received":"✅ Ticket <b>#{id}</b> was delivered to the administrators. Wait for a reply here.","ticket_status":"🎫 Ticket <b>#{id}</b>\nStatus: <b>{status}</b>","faq_text":"❔ <b>FAQ</b>\n\n<b>Why did I not receive a role?</b> Check that you pressed Start and the bot is not blocked.\n\n<b>How do I create a game?</b> Add User Bot as an administrator and send /newgame.\n\n<b>Why is the bot not working?</b> Open Support and send a ticket with a description or screenshot.","custom_count_prompt":"✏️ Send the number of players as one message, from <b>5</b> to <b>40</b>.","custom_count_invalid":"❌ Enter an integer from 5 to 40.","custom_count_saved":"✅ Game size set to <b>{count}</b> players.","mafia_partner_choice":"🔴 Your Mafia partner proposed: <b>{name}</b>. Choose the same target or propose another one.","choose_same":"🎯 Choose this target","mafia_consensus":"🔴 <b>Common target agreed:</b> {name}\nThe night is being resolved.","mafia_chat":"💬 Mafia Chat","mafia_chat_prompt":"💬 Send one message to your Mafia teammates. Chat is available only during the night.","mafia_chat_prefix":"🔴 Message from {name}:","mafia_chat_sent":"✅ Message sent to your teammates."
})
TEXT["uz"].update({
"rules_full":"📜 <b>MAFIA QOIDALARI</b>\n━━━━━━━━━━━━━━\n<b>1. O'YINDAN OLDIN</b>\n• O'yin o'tadigan guruhda bo'lishingiz kerak.\n• Rol faqat shaxsiy chatga yuboriladi.\n• Rol yoki maxfiy bot xabarlarini guruhda oshkor qilmang.\n\n<b>2. TUN</b>\n• Guruh o'yin xabarlari uchun yopiladi.\n• Mafia, Doktor va Komissar shaxsiy tugmalar orqali harakat qiladi.\n• Tinch fuqaroning tungi harakati yo'q.\n\n<b>3. ROLLAR</b>\n🔴 <b>Mafia</b> — jamoa bilan bitta umumiy nishonni tanlaydi.\n🩺 <b>Doktor</b> — bitta tirik o'yinchini himoya qiladi; o'zini davolash sozlanadi.\n🔎 <b>Komissar</b> — bitta o'yinchini tekshiradi. 1-tunda faqat tekshiradi; 2-tundan qo'shimcha chiqarish harakati mavjud.\n⚪ <b>Tinch fuqaro</b> — kunduzi tahlil qiladi va ovoz beradi.\n\n<b>4. KUN VA OVOZ</b>\n• Tirik o'yinchilar kunduzi muhokama qiladi.\n• Ovoz berish shaxsiy tugmalar orqali o'tadi.\n• Taymer tugaguncha ovozni o'zgartirish mumkin.\n• O'zingizga ovoz bera olmaysiz. Chiqib ketganlar ovoz bermaydi.\n\n<b>5. CHIQISH</b>\n• Rollar o'yin oxirigacha yashiriladi.\n• Chiqib ketgan o'yinchiga 30 soniyalik so'nggi so'z beriladi.\n• Keyin u kuzatuvchiga aylanadi.\n\n<b>6. G'ALABA</b>\n• Mafia qolmaganda tinch aholi g'alaba qiladi.\n• Mafia soni boshqa tirik o'yinchilarga teng yoki ko'p bo'lsa Mafia g'alaba qiladi.\n\n⚠️ «Qoidalarni qabul qilish» tugmasi rol maxfiyligi va guruh o'yini qoidalarini tushunganingizni bildiradi.",
"bot_guide":"📘 <b>USER BOTNI GURUHGA QO'SHISH</b>\n━━━━━━━━━━━━━━\n<b>1-qadam.</b> Kerakli Telegram guruhini oching.\n<b>2-qadam.</b> Guruh sozlamalari → Administratorlar.\n<b>3-qadam.</b> User Botni qo'shing.\n<b>4-qadam.</b> Xabarlarni o'chirish va ishtirokchilarni cheklash huquqlarini bering.\n<b>5-qadam.</b> Guruhga qaytib <b>/newgame</b> yuboring.\n\n🔐 Bot administrator huquqlarini avtomatik tekshiradi. Kerakli huquq yetishmasa, o'yin boshlanmaydi va nima qo'shish kerakligi ko'rsatiladi.\n\n💡 Ishonchli moderatsiya uchun BotFather'da Privacy Mode'ni o'chirish tavsiya etiladi.",
"create_menu":"🎮 <b>O'YIN YARATISH</b>\n\nO'yinni kerakli Telegram guruhida yarating. User Bot administrator bo'lishi kerak.","create_in_group_text":"Kerakli guruhni oching → User Botni qo'shing → administrator huquqlarini bering → guruhda <b>/newgame</b> yuboring.","role_config_text":"🎴 <b>O'YIN TARKIBI</b>\n━━━━━━━━━━━━━━\n🔴 Mafia: <b>{mafia}</b>\n🩺 Doktor: <b>{doctor}</b>\n🔎 Komissar: <b>{commissioner}</b>\n⚪ Tinch aholi: <b>{civilian}</b>\n\nAvtobalans boshlang'ich sxema, qat'iy qoida emas.","support_menu":"🛟 <b>YORDAM</b>\n━━━━━━━━━━━━━━\nYordam usulini tanlang.","ticket_prompt":"🎫 <b>YANGI TIKET</b>\n\nMuammoni bitta xabarda yozing. Matn, foto, hujjat, audio, voice yoki video yuborishingiz mumkin.","ticket_received":"✅ #{id} tiket administratorlarga yuborildi. Javobni shu chatda kuting.","ticket_status":"🎫 #{id} tiket\nHolat: <b>{status}</b>","faq_text":"❔ <b>FAQ</b>\n\n<b>Nega rol kelmadi?</b> Start bosilganini va bot bloklanmaganini tekshiring.\n\n<b>O'yinni qanday yarataman?</b> User Botni administrator qiling va /newgame yuboring.\n\n<b>Bot ishlamayapti?</b> Yordam bo'limida tiket yuboring.","custom_count_prompt":"✏️ 5 dan 40 gacha o'yinchi sonini bitta xabarda yuboring.","custom_count_invalid":"❌ 5 dan 40 gacha butun son kiriting.","custom_count_saved":"✅ O'yin hajmi <b>{count}</b> o'yinchi qilib o'rnatildi.","mafia_partner_choice":"🔴 Mafia sherigingiz <b>{name}</b> nishonini taklif qildi. Shu nishonni tanlang yoki boshqasini taklif qiling.","choose_same":"🎯 Shu nishonni tanlash","mafia_consensus":"🔴 <b>Umumiy nishon tanlandi:</b> {name}\nTun yakunlanmoqda.","mafia_chat":"💬 Mafia Chat","mafia_chat_prompt":"💬 Mafia sheriklaringizga bitta xabar yuboring. Chat faqat tunda ishlaydi.","mafia_chat_prefix":"🔴 {name} dan xabar:","mafia_chat_sent":"✅ Xabar sheriklarga yuborildi."
})
TEXT["en"].update({"join_hint":"🔗 <b>Join a game</b>\n\nSend the room code from the lobby here. You can also use a personal invitation link.","room_code_invalid":"❌ Room not found, closed, or the code is incorrect.","invite_text":"🔗 <b>Mafia Lobby invitation</b>\n\nRoom code: <code>{code}</code>\n\nOpen the link and press Start:\n{url}","on":"ON","off":"OFF"})
TEXT["uz"].update({"join_hint":"🔗 <b>O'yinga kirish</b>\n\nLobbydagi xona kodini shu yerga yuboring. Shaxsiy taklif havolasidan ham foydalanishingiz mumkin.","room_code_invalid":"❌ Xona topilmadi, yopilgan yoki kod noto'g'ri.","invite_text":"🔗 <b>Mafia Lobby taklifi</b>\n\nXona kodi: <code>{code}</code>\n\nHavolani ochib Start bosing:\n{url}","on":"YOQILGAN","off":"O'CHIRILGAN"})

# Final compact one-message rules for onboarding and /rules. Plain text by design.
TEXT["ru"]["rules_full"] = """📜 ПРАВИЛА MAFIA
━━━━━━━━━━━━━━
1. ДО ИГРЫ
• Будьте в Telegram-группе, где проходит игра.
• Откройте User Bot и нажмите Start.
• Роль и секретные действия приходят только в личный чат. Не раскрывайте их в группе.

2. НОЧЬ
• Группа закрывается для обычных игровых сообщений.
• Мафия, Доктор и Комиссар действуют через личные кнопки.
• Мирный ночью ничего не выбирает.

3. РОЛИ
🔴 Мафия — вместе выбирает одну общую цель. При большинстве одной цели она применяется по таймеру; при равенстве атака отменяется.
🩺 Доктор — защищает одного живого игрока. Самолечение и повторная защита зависят от настроек.
🔎 Комиссар — проверяет одного живого игрока. В 1-ю ночь только проверка; со 2-й ночи доступно дополнительное выведение. Результат проверки приходит сразу.
⚪ Мирный — ночью не действует, днём обсуждает и голосует.

4. ДЕНЬ И ГОЛОСОВАНИЕ
• Обсуждение — 2 минуты.
• Голосование — 1 минута.
• Голосуют только живые; за себя голосовать нельзя. Голос можно изменить до конца таймера.
• При ничьей проводится повторное голосование, если оно включено.

5. ВЫБЫВАНИЕ
• Роль выбывшего не раскрывается до конца игры.
• Одно последнее слово — 30 секунд. Затем игрок становится наблюдателем.

6. ПОБЕДА
• Мирные побеждают, когда Мафии не осталось.
• Мафия побеждает, когда её количество равно или больше числа остальных живых игроков.
• В конце раскрываются все роли и обновляется статистика.

⚠️ Нажимая «Принять правила», вы соглашаетесь с правилами игры и конфиденциальностью ролей."""
TEXT["uz"]["rules_full"] = """📜 MAFIA QOIDALARI
━━━━━━━━━━━━━━
1. O‘YINDAN OLDIN
• O‘yin o‘tadigan Telegram guruhida bo‘ling.
• User Bot’ni ochib Start bosing.
• Rol va maxfiy harakatlar faqat shaxsiy chatga keladi. Ularni guruhda oshkor qilmang.

2. TUN
• Guruh oddiy o‘yin xabarlari uchun yopiladi.
• Mafia, Doktor va Komissar shaxsiy tugmalar orqali harakat qiladi.
• Tinch fuqaro tunda harakat qilmaydi.

3. ROLLAR
🔴 Mafia — jamoa bilan bitta umumiy nishon tanlaydi. Bitta nishon ko‘pchilik ovozini olsa, taymer oxirida shu nishon qo‘llanadi; tenglikda hujum bekor qilinadi.
🩺 Doktor — bitta tirik o‘yinchini himoya qiladi. O‘zini davolash va takroriy himoya sozlamalarga bog‘liq.
🔎 Komissar — bitta tirik o‘yinchini tekshiradi. 1-tunda faqat tekshiruv; 2-tundan qo‘shimcha chiqarish mavjud. Natija darhol keladi.
⚪ Tinch fuqaro — tunda harakat qilmaydi, kunduzi muhokama qiladi va ovoz beradi.

4. KUN VA OVOZ
• Muhokama — 2 daqiqa.
• Ovoz berish — 1 daqiqa.
• Faqat tiriklar ovoz beradi; o‘zingizga ovoz bera olmaysiz. Ovoz taymer tugaguncha o‘zgartiriladi.
• Tenglikda, sozlama yoqilgan bo‘lsa, qayta ovoz beriladi.

5. CHIQISH
• Chiqib ketgan o‘yinchining roli o‘yin oxirigacha yashiriladi.
• 30 soniyalik bitta so‘nggi so‘z beriladi. Keyin u kuzatuvchiga aylanadi.

6. G‘ALABA
• Mafia qolmaganda tinch aholi g‘alaba qiladi.
• Mafia soni boshqa tirik o‘yinchilarga teng yoki ko‘p bo‘lsa Mafia g‘alaba qiladi.
• O‘yin oxirida barcha rollar ochiladi va statistika yangilanadi.

⚠️ «Qoidalarni qabul qilish» tugmasi o‘yin qoidalari va rol maxfiyligiga roziligingizni bildiradi."""
TEXT["en"]["rules_full"] = """📜 MAFIA RULES
━━━━━━━━━━━━━━
1. BEFORE THE GAME
• Be in the Telegram group where the game is played.
• Open the User Bot and press Start.
• Your role and secret actions are sent only in private chat. Do not reveal them in the group.

2. NIGHT
• The group is closed for normal game messages.
• Mafia, Doctor and Commissioner act through private buttons.
• Civilian has no night action.

3. ROLES
🔴 Mafia — agrees on one shared target. If one target has the most support, it is used when the timer ends; a tie cancels the attack.
🩺 Doctor — protects one living player. Self-heal and repeat protection depend on settings.
🔎 Commissioner — checks one living player. Night 1 is check-only; from Night 2 an additional removal is available. The result is immediate.
⚪ Civilian — has no night action, discusses during the day and votes.

4. DAY AND VOTING
• Discussion — 2 minutes.
• Voting — 1 minute.
• Only living players vote; you cannot vote for yourself. A vote can be changed before the timer ends.
• A tie starts a revote when the setting is enabled.

5. ELIMINATION
• The eliminated player's role stays hidden until the game ends.
• One 30-second last word is allowed. Then the player becomes a spectator.

6. VICTORY
• Civilians win when no Mafia remains.
• Mafia wins when Mafia equals or exceeds all other living players.
• At the end, all roles are revealed and statistics are updated.

⚠️ Pressing “Accept rules” confirms that you agree to the game rules and role secrecy."""

# --- Mafia v6 role system / polished localization overrides ---
_ROLE_TEXT = {
"ru": {
"role_lover":"💗 Любовница","role_detective":"🕵️ Детектив","role_bodyguard":"🛡 Телохранитель",
"role_info":"📖 Описание","role_no_room":"⚠️ В составе должен остаться хотя бы один мирный.",
"lobby_created":"✨ Лобби создано! Настройте размер, роли и параметры игры. Когда будете готовы — нажмите «Начать».",
"role_config_text":"🎴 <b>НАСТРОЙКА РОЛЕЙ</b>\n━━━━━━━━━━━━━━\n{roles}\n\n👥 Всего мест: <b>{total}</b>\n\n🔒 Мафия и Доктор обязательны. Остальные роли можно включать и выключать. Мирные автоматически занимают оставшиеся места.",
"role_mafia_desc":"Командная роль. Ночью мафия выбирает общую цель. Днём скрывайте свою роль и убеждайте город ошибиться.",
"role_doctor_desc":"Защитная роль. Каждую ночь выбирайте живого игрока. Если на него направлена ночная атака, лечение спасает его. Самолечение работает по настройкам.",
"role_commissioner_desc":"Расследователь. Ночью проверяйте игрока и сразу получайте, является ли он мафией. Со 2-й ночи может быть доступно дополнительное выведение.",
"role_lover_desc":"Контрольная роль. Ночью выберите игрока — его ночное действие будет заблокировано. Нельзя выбирать себя.",
"role_detective_desc":"Расследователь. Ночью проверьте игрока и получите результат по фракции: мафия или не мафия. Дополнительного убийства нет.",
"role_bodyguard_desc":"Защитник. Ночью выберите игрока. Если мафия или комиссар атакует защищённую цель, атака не сработает.",
"role_civilian_desc":"Мирная роль. Ночью у вас нет действия. Ваша сила — обсуждение, анализ и дневное голосование.",
"mafia_guide":"📕 <b>ИНСТРУКЦИЯ — МАФИЯ</b>\n\n🎯 <b>Цель:</b> довести количество мафии до паритета с остальными живыми игроками.\n🌙 <b>Ночью:</b> выберите цель. Ваши напарники увидят ваше предложение. Система определит общий выбор.\n☀️ <b>Днём:</b> убеждайте город, не раскрывая роль.\n💬 <b>Командный чат:</b> доступен ночью.\n⚠️ Если предложения мафии делятся поровну, атака отменяется.",
"doctor_guide":"📕 <b>ИНСТРУКЦИЯ — ДОКТОР</b>\n\n🎯 <b>Цель:</b> помогать мирной стороне выживать.\n🌙 <b>Ночью:</b> выберите живого игрока для лечения.\n🩺 Лечение защищает от ночного убийства.\n🔁 Повторная цель и самолечение зависят от настроек лобби.",
"commissioner_guide":"📕 <b>ИНСТРУКЦИЯ — КОМИССАР</b>\n\n🎯 <b>Цель:</b> находить мафию.\n🌙 <b>Ночью:</b> выберите игрока для проверки. Результат приходит сразу.\n🔎 В первую ночь доступна проверка. Со второй ночи может появиться дополнительное действие, если создатель его включил.",
"lover_guide":"📕 <b>ИНСТРУКЦИЯ — ЛЮБОВНИЦА</b>\n\n🎯 <b>Цель:</b> мешать опасным ночным действиям.\n🌙 Выберите одного игрока. Его ночное действие будет заблокировано.\n⚠️ Нельзя выбрать себя. Вы не узнаёте роль цели.",
"detective_guide":"📕 <b>ИНСТРУКЦИЯ — ДЕТЕКТИВ</b>\n\n🎯 <b>Цель:</b> получать информацию о подозреваемых.\n🌙 Выберите игрока для проверки. Результат показывает только фракцию: мафия или не мафия.\n🔐 Вы не раскрываете свою роль группе.",
"bodyguard_guide":"📕 <b>ИНСТРУКЦИЯ — ТЕЛОХРАНИТЕЛЬ</b>\n\n🎯 <b>Цель:</b> защищать ключевых игроков.\n🌙 Выберите одного живого игрока. Атака на защищённую цель ночью отменяется.\n⚠️ Ваша задача — предугадывать, кого попытаются убрать.",
"civilian_guide":"📕 <b>ИНСТРУКЦИЯ — МИРНЫЙ ЖИТЕЛЬ</b>\n\n🎯 <b>Цель:</b> вычислить мафию и сохранить большинство города.\n🌙 Ночного действия нет.\n☀️ Анализируйте речь, голосования и поведение игроков.\n🗳 Днём голосуйте обдуманно.",
"lover_action":"💗 <b>Ход Любовницы</b>\n\nВыберите игрока, чьё ночное действие хотите заблокировать.",
"detective_action":"🕵️ <b>Ход Детектива</b>\n\nВыберите игрока для проверки фракции.",
"bodyguard_action":"🛡 <b>Ход Телохранителя</b>\n\nВыберите игрока, которого будете защищать этой ночью.",
"detective_mafia":"🔴 Мафия","detective_not_mafia":"⚪ Не мафия","detective_result":"🕵️ Проверка: <b>{name}</b> — {result}.",
},
"en": {
"role_lover":"💗 Lover","role_detective":"🕵️ Detective","role_bodyguard":"🛡 Bodyguard","role_info":"📖 Info","role_no_room":"⚠️ At least one Civilian must remain.",
"lobby_created":"✨ Lobby created! Configure the player count, roles and game settings. When everything is ready, press Start.",
"role_config_text":"🎴 <b>ROLE SETUP</b>\n━━━━━━━━━━━━━━\n{roles}\n\n👥 Player slots: <b>{total}</b>\n\n🔒 Mafia and Doctor are mandatory. Other roles can be enabled or disabled. Civilians automatically fill the remaining slots.",
"role_mafia_desc":"Team role. Mafia chooses a shared target at night. During the day, hide your role and persuade the town.","role_doctor_desc":"Protective role. Choose a living player at night. If they are attacked, the protection saves them. Self-heal follows lobby settings.","role_commissioner_desc":"Investigator. Check a player at night and immediately learn whether they are Mafia. From Night 2, an extra elimination may be enabled.","role_lover_desc":"Control role. Choose a player at night and block their night action. You cannot target yourself.","role_detective_desc":"Investigator. Check a player at night and receive only their faction result: Mafia or not Mafia.","role_bodyguard_desc":"Defender. Protect one player at night. An attack against the protected target is cancelled.","role_civilian_desc":"Town role. You have no night action. Your power is discussion, analysis and voting.",
"mafia_guide":"📕 <b>ROLE GUIDE — MAFIA</b>\n\n🎯 <b>Goal:</b> reach parity with all other living players.\n🌙 <b>Night:</b> choose a target. Your teammates see your proposal and the system resolves the shared decision.\n☀️ <b>Day:</b> persuade the town without revealing your role.\n💬 Mafia chat is available at night.\n⚠️ A tied Mafia decision cancels the attack.",
"doctor_guide":"📕 <b>ROLE GUIDE — DOCTOR</b>\n\n🎯 <b>Goal:</b> keep the town alive.\n🌙 Choose one living player to protect.\n🩺 Protection blocks a night kill.\n🔁 Repeat targets and self-heal depend on lobby settings.",
"commissioner_guide":"📕 <b>ROLE GUIDE — COMMISSIONER</b>\n\n🎯 <b>Goal:</b> identify Mafia.\n🌙 Check one player. The result is delivered immediately.\n🔎 Night 1 is check-only. From Night 2 an extra removal may be available.",
"lover_guide":"📕 <b>ROLE GUIDE — LOVER</b>\n\n🎯 <b>Goal:</b> disrupt dangerous night actions.\n🌙 Choose one player. Their night action is blocked.\n⚠️ You cannot target yourself and you do not learn the target's role.",
"detective_guide":"📕 <b>ROLE GUIDE — DETECTIVE</b>\n\n🎯 <b>Goal:</b> gather information.\n🌙 Check one player. The result reveals only the faction: Mafia or not Mafia.\n🔐 Keep your role secret.",
"bodyguard_guide":"📕 <b>ROLE GUIDE — BODYGUARD</b>\n\n🎯 <b>Goal:</b> protect important players.\n🌙 Choose one living player. A night attack against them is cancelled.\n⚠️ Predict who the attackers will target.",
"civilian_guide":"📕 <b>ROLE GUIDE — CIVILIAN</b>\n\n🎯 <b>Goal:</b> find Mafia and keep the town majority.\n🌙 No night action.\n☀️ Analyze statements, votes and behavior.\n🗳 Vote carefully during the day.",
"lover_action":"💗 <b>Lover's turn</b>\n\nChoose the player whose night action you want to block.","detective_action":"🕵️ <b>Detective's turn</b>\n\nChoose a player to check.","bodyguard_action":"🛡 <b>Bodyguard's turn</b>\n\nChoose the player you will protect tonight.","detective_mafia":"🔴 Mafia","detective_not_mafia":"⚪ Not Mafia","detective_result":"🕵️ Check: <b>{name}</b> — {result}.",
},
"uz": {
"role_lover":"💗 Ma’shuqa","role_detective":"🕵️ Detektiv","role_bodyguard":"🛡 Qo‘riqchi","role_info":"📖 Ma’lumot","role_no_room":"⚠️ Kamida bitta Tinch fuqaro qolishi kerak.",
"lobby_created":"✨ Lobby yaratildi! O‘yinchilar soni, rollar va sozlamalarni tanlang. Hammasi tayyor bo‘lsa, Boshlash tugmasini bosing.",
"role_config_text":"🎴 <b>ROLLARNI SOZLASH</b>\n━━━━━━━━━━━━━━\n{roles}\n\n👥 O‘yinchi joylari: <b>{total}</b>\n\n🔒 Mafia va Doktor majburiy. Boshqa rollarni yoqish yoki o‘chirish mumkin. Qolgan joylarni Tinch fuqarolar to‘ldiradi.",
"role_mafia_desc":"Jamoaviy rol. Mafia tunda umumiy nishonni tanlaydi. Kunduzi rolingizni yashiring va shaharni ishontiring.","role_doctor_desc":"Himoya roli. Tunda tirik o‘yinchini davolang. Hujum bo‘lsa, himoya uni saqlaydi.","role_commissioner_desc":"Tekshiruvchi. Tunda o‘yinchini tekshiring va uning Mafia ekanini darhol biling. 2-kechadan qo‘shimcha chiqarish bo‘lishi mumkin.","role_lover_desc":"Nazorat roli. Tunda o‘yinchini tanlang — uning tungi harakati bloklanadi. O‘zingizni tanlay olmaysiz.","role_detective_desc":"Tekshiruvchi. Tunda o‘yinchini tekshiring va faqat fraksiyasini bilib oling: Mafia yoki Mafia emas.","role_bodyguard_desc":"Himoyachi. Tunda bitta o‘yinchini himoya qiling. Himoyalangan nishonga hujum bekor qilinadi.","role_civilian_desc":"Tinch rol. Tunda harakat yo‘q. Sizning kuchingiz — muhokama, tahlil va ovoz berish.",
"mafia_guide":"📕 <b>ROL YO‘RIQNOMASI — MAFIA</b>\n\n🎯 Maqsad: tirik Mafia sonini qolgan tirik o‘yinchilarga tenglashtirish.\n🌙 Tunda umumiy nishonni tanlang.\n☀️ Kunduzi rolingizni yashiring.\n💬 Mafia chati faqat tunda ishlaydi.","doctor_guide":"📕 <b>ROL YO‘RIQNOMASI — DOKTOR</b>\n\n🌙 Tunda bitta tirik o‘yinchini himoya qiling.\n🩺 Himoya tungi hujumni to‘xtatadi.\n🔁 O‘zini davolash va takroriy nishon sozlamalarga bog‘liq.","commissioner_guide":"📕 <b>ROL YO‘RIQNOMASI — KOMISSAR</b>\n\n🌙 O‘yinchini tekshiring. Natija darhol keladi.\n🔎 1-kechada faqat tekshiruv, 2-kechadan qo‘shimcha harakat bo‘lishi mumkin.","lover_guide":"📕 <b>ROL YO‘RIQNOMASI — MA’SHUQA</b>\n\n🌙 Bitta o‘yinchini tanlang. Uning tungi harakati bloklanadi.\n⚠️ O‘zingizni tanlay olmaysiz.","detective_guide":"📕 <b>ROL YO‘RIQNOMASI — DETEKTIV</b>\n\n🌙 Bitta o‘yinchini tekshiring. Natija faqat fraksiyani ko‘rsatadi: Mafia yoki Mafia emas.","bodyguard_guide":"📕 <b>ROL YO‘RIQNOMASI — QO‘RIQCHI</b>\n\n🌙 Bitta tirik o‘yinchini himoya qiling. Unga tungi hujum bekor qilinadi.","civilian_guide":"📕 <b>ROL YO‘RIQNOMASI — TINCH FUQARO</b>\n\n🌙 Tungi harakat yo‘q.\n☀️ Nutq, ovoz va xatti-harakatlarni tahlil qiling.\n🗳 Kunduzi ovoz bering.",
"lover_action":"💗 <b>Ma’shuqa harakati</b>\n\nTungi harakatini bloklamoqchi bo‘lgan o‘yinchini tanlang.","detective_action":"🕵️ <b>Detektiv harakati</b>\n\nTekshirish uchun o‘yinchini tanlang.","bodyguard_action":"🛡 <b>Qo‘riqchi harakati</b>\n\nBugun tunda himoya qiladigan o‘yinchini tanlang.","detective_mafia":"🔴 Mafia","detective_not_mafia":"⚪ Mafia emas","detective_result":"🕵️ Tekshiruv: <b>{name}</b> — {result}."}
}
for _lang, _vals in _ROLE_TEXT.items(): TEXT[_lang].update(_vals)

_TEXT_UI_EN = {
"invite":"➕ Invite","player_count":"👥 Players","roles":"🎴 Roles","lobby_v2":"🎭 <b>MAFIA LOBBY #{game_id}</b>\n━━━━━━━━━━━━━━\n👥 Players: <b>{count}/{max}</b>\n🎴 Roles: {roles}\n\n{players}\n\n⏳ Status: <b>Waiting for players</b>\n\nUse the buttons below to configure the room.",
"choose_player_count":"👥 <b>Game size</b>\n\nChoose a preset from 5 to 40 players.","custom_count":"✏️ Custom size","custom_count_prompt":"✏️ Send one number from <b>5</b> to <b>40</b>.","custom_count_invalid":"❌ Enter a whole number from 5 to 40.","custom_count_saved":"✅ Game size set to <b>{count}</b> players.","auto_balance":"⚖️ Auto balance","active_game":"⚠️ This group already has an active game.","admin_permissions_missing":"⚠️ User Bot is not ready. Missing permissions: <b>{missing}</b>.","rules_group":"📜 <b>MAFIA GAME</b>\nRoles are delivered privately. The group is locked during the night. Follow the bot buttons and timers.","creator_only":"⛔ Only the lobby creator can use this action.","group_only":"📍 This command must be used in a game group.","open_private":"🔐 Open the User Bot in private chat and press Start first.","joined":"✅ You joined the game.","already_joined":"⚠️ You are already in the lobby.","too_many":"❌ The player limit is {max}.","private_delivery_failed":"⚠️ The bot could not reach one or more players in private chat. The game was not started.","ready_title":"🟢 <b>Ready to play?</b>\n\nPress Ready when you are prepared for the game.","ready_yes":"✅ Ready","ready_no":"❌ Not ready","ready_saved":"✅ Ready status saved.","ready_failed":"⏸ Not everyone confirmed. The lobby returned to waiting mode.","game_starting":"🔥 <b>The game is starting.</b>\n\nCheck your private chat. Roles and actions will be delivered there.","preflight_ok":"🔐 Private chat confirmed. Your role and secret actions will be delivered here.","role_sent":"🎴 <b>Your role: {role}</b>\n\n{description}\n\n🔒 Your role is secret.","settings_title":"⚙️ <b>Game settings</b>\n\nOnly the lobby creator can change settings.","setting_auto":"Auto start","setting_ready":"Ready check","setting_skip":"Skip vote","setting_self":"Doctor self-heal","setting_repeat":"Repeat doctor target","setting_commissioner":"Commissioner extra action","setting_revote":"Revote on tie","back":"↩️ Back","cancel":"Cancel","ticket_admin_header":"🎫 <b>Ticket #{id}</b>\n👤 {name}\n🆔 <code>{tg_id}</code>\nUsername: {username}","status_new":"New","status_delivered":"Delivered","status_in_progress":"In progress","status_waiting_user":"Waiting for user","status_closed":"Closed","no_ticket":"📭 No active tickets.","rules_required":"📜 Choose a language and accept the rules first."}
_TEXT_UI_UZ = {
"invite":"➕ Taklif qilish","player_count":"👥 O‘yinchilar","roles":"🎴 Rollar","lobby_v2":"🎭 <b>MAFIA LOBBY #{game_id}</b>\n━━━━━━━━━━━━━━\n👥 O‘yinchilar: <b>{count}/{max}</b>\n🎴 Rollar: {roles}\n\n{players}\n\n⏳ Holat: <b>O‘yinchilar kutilmoqda</b>\n\nQuyidagi tugmalar orqali xonani sozlang.","choose_player_count":"👥 <b>O‘yin hajmi</b>\n\n5 dan 40 gacha tayyor variantni tanlang.","custom_count":"✏️ Maxsus son","custom_count_prompt":"✏️ 5 dan 40 gacha bitta son yuboring.","custom_count_invalid":"❌ 5 dan 40 gacha butun son kiriting.","custom_count_saved":"✅ O‘yin hajmi <b>{count}</b> o‘yinchi qilib o‘rnatildi.","auto_balance":"⚖️ Avtobalans","active_game":"⚠️ Bu guruhda faol o‘yin allaqachon mavjud.","admin_permissions_missing":"⚠️ User Bot tayyor emas. Yetishmayotgan huquqlar: <b>{missing}</b>.","rules_group":"📜 <b>MAFIA O‘YINI</b>\nRollar shaxsiy chatga yuboriladi. Tunda guruh yopiladi. Bot tugmalari va taymerlarga amal qiling.","creator_only":"⛔ Bu amal faqat lobby yaratuvchisi uchun.","group_only":"📍 Bu buyruq o‘yin guruhida ishlatilishi kerak.","open_private":"🔐 Avval User Bot shaxsiy chatini ochib Start bosing.","joined":"✅ Siz o‘yinga qo‘shildingiz.","already_joined":"⚠️ Siz allaqachon lobbydasiz.","too_many":"❌ O‘yinchilar limiti: {max}.","private_delivery_failed":"⚠️ Bot bir yoki bir nechta o‘yinchiga shaxsiy xabar yubora olmadi. O‘yin boshlanmadi.","ready_title":"🟢 <b>O‘ynashga tayyormisiz?</b>\n\nTayyor bo‘lsangiz tugmani bosing.","ready_yes":"✅ Tayyor","ready_no":"❌ Tayyor emas","ready_saved":"✅ Holat saqlandi.","ready_failed":"⏸ Hamma tasdiqlamadi. Lobby kutish rejimiga qaytdi.","game_starting":"🔥 <b>O‘yin boshlanmoqda.</b>\n\nShaxsiy chatni tekshiring. Rollar va harakatlar shu yerga yuboriladi.","preflight_ok":"🔐 Shaxsiy chat tasdiqlandi. Rol va maxfiy harakatlar shu yerga keladi.","role_sent":"🎴 <b>Sizning rolingiz: {role}</b>\n\n{description}\n\n🔒 Rolingiz maxfiy.","settings_title":"⚙️ <b>O‘yin sozlamalari</b>\n\nFaqat lobby yaratuvchisi o‘zgartira oladi.","setting_auto":"Avtostart","setting_ready":"Tayyorlik","setting_skip":"Ovozda o‘tkazish","setting_self":"Doktor o‘zini davolashi","setting_repeat":"Doktor bir xil nishoni","setting_commissioner":"Komissarning qo‘shimcha harakati","setting_revote":"Durrangda qayta ovoz","back":"↩️ Orqaga","cancel":"Bekor qilish","status_new":"Yangi","status_delivered":"Yetkazildi","status_in_progress":"Jarayonda","status_waiting_user":"Foydalanuvchi javobi kutilmoqda","status_closed":"Yopiq","no_ticket":"📭 Faol tiketlar yo‘q.","rules_required":"📜 Avval tilni tanlang va qoidalarni qabul qiling."}
TEXT["en"].update(_TEXT_UI_EN)
TEXT["uz"].update(_TEXT_UI_UZ)
TEXT["uz"].update({"yes":"Ha", "no":"Yo‘q", "role_invalid":"❌ Bu rollar kombinatsiyasi tanlangan o‘yinchilar soni uchun mos emas.", "auto_balance":"⚖️ Rollarni avtobalanslash", "setting_extra":"Qo‘shimcha muhokama vaqti", "mafia_chat":"💬 Mafia chati"})


# Final localization overrides: these keys were previously copied from Russian.
TEXT["ru"].update({"language_change_error": "⚠️ Не удалось изменить язык. Попробуйте ещё раз.", "yes":"Да", "no":"Нет", "role_invalid":"❌ Такая комбинация ролей недопустима для выбранного количества игроков.", "auto_balance":"⚖️ Автобаланс ролей", "setting_extra":"Дополнительное время", "mafia_chat":"💬 Чат мафии"})

TEXT["en"].update({
    "language_change_error": "⚠️ The language could not be changed. Please try again.",
    "rules_accepted": "✅ <b>Rules accepted.</b> Game creation, joining, profile, statistics and support are now available.",
    "how_add_bot": "📘 How to add the bot",
    "create_in_group": "➕ Create in a group",
    "how_to_add": "How to add the bot",
    "doctor_self_1": "🩺 Self-save ×1",
    "doctor_self_2": "🩺 Self-save ×2",
    "stats_detailed": "📊 <b>Your statistics</b>\n━━━━━━━━━━━━━━\n🎮 Games: <b>{games}</b>\n🏆 Wins: <b>{wins}</b>\n☠️ Losses: <b>{losses}</b>\n\n🎴 <b>By role</b>\nFormat: games / wins / losses\n{roles}",
    "profile_card": "👤 <b>My profile</b>\n━━━━━━━━━━━━━━\n<b>Name:</b> {name}\n<b>Username:</b> {username}\n<b>Telegram ID:</b> <code>{tg_id}</code>\n<b>Language:</b> {language}\n<b>First start:</b> {first}\n<b>Last seen:</b> {last}\n<b>Rules accepted:</b> {rules}\n<b>Games:</b> {games}\n<b>Wins:</b> {wins}\n<b>Losses:</b> {losses}\n<b>Bot blocked:</b> {blocked}",
    "no_username": "none",
    "cancelled": "↩️ Cancelled",
    "ticket_admin_reply": "Administrator reply to ticket #{id}",
    "broadcast": "📣 Broadcast",
    "users": "👥 Users",
    "groups": "🏘 Groups",
    "games": "🎮 Games",
    "logs": "🧾 Logs",
    "system": "⚙️ System",
    "refresh": "🔄 Refresh",
    "period_today": "Today",
    "period_7d": "7 days",
    "period_month": "This month",
    "period_year": "This year",
    "period_all": "All time",
    "export": "📤 Export",
    "broadcast_done": "📣 Broadcast finished",
    "ticket": "🎫 Support",
})
TEXT["uz"].update({
    "language_change_error": "⚠️ Tilni o‘zgartirib bo‘lmadi. Qayta urinib ko‘ring.",
    "rules_accepted": "✅ <b>Qoidalar qabul qilindi.</b> Endi o‘yin yaratish, o‘yinga qo‘shilish, profil, statistika va yordam mavjud.",
    "how_add_bot": "📘 Botni qanday qo‘shish",
    "create_in_group": "➕ Guruhda yaratish",
    "how_to_add": "Botni qanday qo‘shish",
    "doctor_self_1": "🩺 O‘zini davolash ×1",
    "doctor_self_2": "🩺 O‘zini davolash ×2",
    "stats_detailed": "📊 <b>Statistikangiz</b>\n━━━━━━━━━━━━━━\n🎮 O‘yinlar: <b>{games}</b>\n🏆 G‘alabalar: <b>{wins}</b>\n☠️ Mag‘lubiyatlar: <b>{losses}</b>\n\n🎴 <b>Rollar bo‘yicha</b>\nFormat: o‘yinlar / g‘alabalar / mag‘lubiyatlar\n{roles}",
    "profile_card": "👤 <b>Mening profilim</b>\n━━━━━━━━━━━━━━\n<b>Ism:</b> {name}\n<b>Username:</b> {username}\n<b>Telegram ID:</b> <code>{tg_id}</code>\n<b>Til:</b> {language}\n<b>Birinchi start:</b> {first}\n<b>Oxirgi faollik:</b> {last}\n<b>Qoidalar qabul qilingan:</b> {rules}\n<b>O‘yinlar:</b> {games}\n<b>G‘alabalar:</b> {wins}\n<b>Mag‘lubiyatlar:</b> {losses}\n<b>Bot bloklangan:</b> {blocked}",
    "no_username": "yo‘q",
    "ticket_admin_header": "🎫 <b>#{id}-tiket</b>\n👤 {name}\n🆔 <code>{tg_id}</code>\nUsername: {username}",
    "cancelled": "↩️ Bekor qilindi",
    "ticket_admin_reply": "Administratorning #{id}-tiketga javobi",
    "broadcast": "📣 Tarqatma",
    "users": "👥 Foydalanuvchilar",
    "groups": "🏘 Guruhlar",
    "games": "🎮 O‘yinlar",
    "logs": "🧾 Loglar",
    "system": "⚙️ Tizim",
    "refresh": "🔄 Yangilash",
    "period_today": "Bugun",
    "period_7d": "7 kun",
    "period_month": "Shu oy",
    "period_year": "Shu yil",
    "period_all": "Barcha vaqt",
    "export": "📤 Eksport",
    "broadcast_done": "📣 Tarqatma yakunlandi",
    "ticket": "🎫 Yordam",
})

# Command-driven lobby/join contract (v9). These keys intentionally use the
# same commands that will be registered in BotFather.
_COMMAND_TEXT = {
    "ru": {
        "join_private_only": "🔒 Используйте /join в личном чате с User Bot.",
        "invite_group_only": "📍 Используйте /invite внутри игровой группы.",
        "lobby_group_only": "📍 Используйте /lobby внутри игровой группы.",
        "no_active_lobby": "📭 В этой группе сейчас нет активного лобби.",
        "invite_sent": "✅ Код комнаты и персональная ссылка отправлены вам в личный чат.",
        "create_in_group_text": "🎮 Создание игры\n\nДобавьте User Bot в нужную группу, выдайте права администратора и выполните /create в этой группе.",
        "join_hint": "🔗 <b>Вход в игру</b>\n\nВведите код комнаты, например:\n<code>/join ABC123</code>\n\nИли отправьте только сам код сообщением.\n\nТакже можно открыть персональную ссылку-приглашение.",
        "invite_text": "🔗 <b>Приглашение в Mafia Lobby</b>\n\nКод комнаты: <code>{code}</code>\n\nПерсональная ссылка:\n{url}\n\nИгрок должен состоять в игровой группе и открыть ссылку через Start.",
    },
    "en": {
        "join_private_only": "🔒 Use /join in the private chat with the User Bot.",
        "invite_group_only": "📍 Use /invite inside the game group.",
        "lobby_group_only": "📍 Use /lobby inside the game group.",
        "no_active_lobby": "📭 There is no active lobby in this group.",
        "invite_sent": "✅ The room code and personal invite link were sent to your private chat.",
        "create_in_group_text": "🎮 Create a game\n\nAdd the User Bot to the target group, grant administrator permissions, then use /create in that group.",
        "join_hint": "🔗 <b>Join a game</b>\n\nEnter the room code, for example:\n<code>/join ABC123</code>\n\nOr send only the code as a message.\n\nYou can also open a personal invitation link.",
        "invite_text": "🔗 <b>Mafia Lobby invitation</b>\n\nRoom code: <code>{code}</code>\n\nPersonal link:\n{url}\n\nThe player must be a member of the game group and open the link through Start.",
    },
    "uz": {
        "join_private_only": "🔒 /join buyrug'ini User Bot bilan shaxsiy chatda ishlating.",
        "invite_group_only": "📍 /invite buyrug'ini o'yin guruhida ishlating.",
        "lobby_group_only": "📍 /lobby buyrug'ini o'yin guruhida ishlating.",
        "no_active_lobby": "📭 Bu guruhda hozir faol lobby yo'q.",
        "invite_sent": "✅ Xona kodi va shaxsiy taklif havolasi shaxsiy chatga yuborildi.",
        "create_in_group_text": "🎮 O'yin yaratish\n\nUser Botni kerakli guruhga qo'shing, administrator huquqlarini bering va guruhda /create buyrug'ini yuboring.",
        "join_hint": "🔗 <b>O'yinga kirish</b>\n\nXona kodini kiriting, masalan:\n<code>/join ABC123</code>\n\nYoki faqat kodni xabar sifatida yuboring.\n\nShuningdek, shaxsiy taklif havolasini ochishingiz mumkin.",
        "invite_text": "🔗 <b>Mafia Lobby taklifi</b>\n\nXona kodi: <code>{code}</code>\n\nShaxsiy havola:\n{url}\n\nO'yinchi o'yin guruhida bo'lishi va havolani Start orqali ochishi kerak.",
    },
}
for _lang, _vals in _COMMAND_TEXT.items():
    TEXT[_lang].update(_vals)

# The room code is part of the lobby itself; players no longer depend on the
# creator discovering it through a separate action.
TEXT["ru"]["lobby_v2"] = """🎭 <b>MAFIA LOBBY #{game_id}</b>
━━━━━━━━━━━━━━
🔑 Код комнаты: <code>{code}</code>
👥 Игроки: <b>{count}/{max}</b>
🎴 Состав: {roles}

{players}

⏳ Статус: <b>Ожидание игроков</b>

Игроки могут войти по коду через /join или по персональной ссылке из кнопки «Пригласить»."""
TEXT["en"]["lobby_v2"] = """🎭 <b>MAFIA LOBBY #{game_id}</b>
━━━━━━━━━━━━━━
🔑 Room code: <code>{code}</code>
👥 Players: <b>{count}/{max}</b>
🎴 Roles: {roles}

{players}

⏳ Status: <b>Waiting for players</b>

Players can join with /join using the code or use the personal link from the Invite button."""
TEXT["uz"]["lobby_v2"] = """🎭 <b>MAFIA LOBBY #{game_id}</b>
━━━━━━━━━━━━━━
🔑 Xona kodi: <code>{code}</code>
👥 O'yinchilar: <b>{count}/{max}</b>
🎴 Rollar: {roles}

{players}

⏳ Holat: <b>O'yinchilar kutilmoqda</b>

O'yinchilar /join orqali kod bilan yoki Taklif qilish tugmasidagi shaxsiy havola orqali kirishi mumkin."""

# v10 UX / rules overhaul. These overrides intentionally keep one complete,
# readable rules message under Telegram's 4096-character message limit.
_V10_USER = {
"ru": {
"rules_full": """🎭 <b>ПРАВИЛА MAFIA</b>
━━━━━━━━━━━━━━
<b>1. ДО НАЧАЛА</b>
• Сначала откройте User Bot, выберите язык и нажмите «Принять правила». До подтверждения игровые функции недоступны.
• Для игры нужен доступ к группе. Роль, ночные действия и результаты проверок приходят только в личный чат.
• Не пересылайте роль и секретные сообщения другим игрокам.

<b>2. РОЛИ</b>
🔴 <b>Мафия</b> — ночная команда. Выберите цель; предложения мафии учитываются системой. Если одна цель получает явное большинство, она становится общей. При полном равенстве атака отменяется. Мафия побеждает при паритете с остальными живыми.
🩺 <b>Доктор</b> — каждую ночь защищает одного живого игрока от ночной атаки. Самолечение и повтор цели зависят от настроек лобби.
🔎 <b>Комиссар</b> — ночью проверяет одного живого игрока и сразу получает результат «Мафия / не Мафия». В первую ночь доступна только проверка. Со второй ночи дополнительное выведение возможно, если его включил создатель.
💗 <b>Любовница</b> — ночью блокирует ночное действие выбранного игрока. Себя выбрать нельзя; роль цели не раскрывается.
🕵️ <b>Детектив</b> — ночью проверяет одного игрока и получает только результат по фракции: «Мафия / не Мафия».
🛡 <b>Телохранитель</b> — ночью защищает одного игрока. Атака на защищённую цель отменяется.
⚪ <b>Мирный житель</b> — ночного действия нет. Анализирует игроков, участвует в обсуждении и дневном голосовании.

<b>3. НОЧЬ</b>
🌙 Группа закрывается для обычных игровых сообщений. Действия выполняются кнопками в личном чате. Таймер ограничивает время хода.

<b>4. ДЕНЬ И ГОЛОСОВАНИЕ</b>
☀️ Обсуждение — 2 минуты. Затем голосование — 1 минута.
• Голосуют только живые. За себя голосовать нельзя.
• Голос можно изменить до окончания таймера.
• Пропуск и повторное голосование при ничьей зависят от настроек.

<b>5. ВЫБЫВАНИЕ</b>
🚪 Роль выбывшего не раскрывается до конца игры. Ему даётся одно последнее слово на 30 секунд, после чего он становится наблюдателем и больше не влияет на игру.

<b>6. ПОБЕДА</b>
🏆 Мирные побеждают, когда мафии не осталось.
🏆 Мафия побеждает, когда её число равно или превышает число остальных живых игроков.
В конце раскрываются все роли и обновляется статистика.

⚠️ Нажимая «Принять правила», вы подтверждаете, что прочитали правила и понимаете принцип секретности ролей.""",
"rules_required":"🔒 <b>Доступ закрыт</b>\n\nСначала выберите язык, прочитайте правила и нажмите «Принять правила». После этого откроются все игровые функции.",
"rules_accepted":"✅ <b>Правила приняты.</b>\n\n🎭 Теперь доступны игровые функции. Используйте меню ниже — у сложных кнопок есть отдельные инструкции.",
"help_text":"❓ <b>КАК ПОЛЬЗОВАТЬСЯ MAFIA</b>\n━━━━━━━━━━━━━━\n1️⃣ Откройте бота и примите правила.\n2️⃣ Добавьте User Bot в игровую группу и выдайте права администратора.\n3️⃣ В группе отправьте /create.\n4️⃣ Бот создаст лобби и покажет <b>код комнаты</b>.\n5️⃣ Игроки входят через /join КОД или по персональной ссылке.\n6️⃣ Создатель настраивает размер, роли и параметры.\n7️⃣ После старта роли и действия приходят в личку.\n8️⃣ Ночью группа закрыта; днём живые обсуждают и голосуют.\n\n💡 Непонятная кнопка? Нажмите «ℹ️ Как это работает» — бот объяснит действие прямо в личке.\n\n⚠️ Для модерации бот должен быть администратором группы с правами удаления сообщений и ограничения участников.",
"create_menu":"🎮 <b>СОЗДАНИЕ ИГРЫ</b>\n━━━━━━━━━━━━━━\nДобавьте User Bot в нужную группу и создайте лобби командой /create. После создания бот покажет код комнаты и кнопки управления.",
"create_in_group_text":"➕ <b>Создание игры</b>\n\n1. Откройте нужную группу.\n2. Добавьте User Bot в администраторы.\n3. Выдайте права удаления сообщений и ограничения участников.\n4. В группе отправьте /create.\n\n🎟 После создания появится код комнаты, которым можно делиться с игроками.",
"create_how":"🎮 <b>КАК СОЗДАТЬ ИГРУ</b>\n\n/create создаёт одно лобби в текущей группе. Создатель автоматически становится первым игроком. В лобби можно изменить размер, состав ролей и настройки.\n\n🔑 Код комнаты виден прямо в лобби.\n🔗 Кнопка «Пригласить» отправляет создателю код и персональную ссылку.\n▶️ Игра запускается только при корректном составе и доступности личных чатов участников.",
"join_hint":"🔗 <b>ВХОД В ИГРУ</b>\n\nВведите код комнаты из лобби. Например:\n<code>/join ABC123</code>\n\nМожно просто отправить код после нажатия «Войти в игру».\n\n🔗 Если у вас есть персональная ссылка, откройте её и нажмите Start.",
"join_help":"ℹ️ Как войти",
"join_help_text":"🔗 <b>КАК ВОЙТИ В ЛОББИ</b>\n\n<b>Способ 1:</b> /join ABC123\n<b>Способ 2:</b> нажмите «Войти в игру» и отправьте код ABC123.\n<b>Способ 3:</b> откройте персональную ссылку приглашения и нажмите Start.\n\n⚠️ Вы должны состоять в той Telegram-группе, где проходит игра, а правила должны быть приняты.",
"invite_text":"🔗 <b>ПРИГЛАШЕНИЕ В MAFIA LOBBY</b>\n━━━━━━━━━━━━━━\n🔑 Код: <code>{code}</code>\n\n🔗 Персональная ссылка:\n{url}\n\nОтправьте ссылку игроку. После Start бот автоматически попробует добавить его в это лобби.",
"lobby_help":"ℹ️ <b>КАК РАБОТАЕТ ЛОББИ</b>\n\n🔑 <b>Код</b> — основной способ входа.\n👥 <b>Игроки</b> — текущий состав и свободные места.\n🎴 <b>Роли</b> — настройка состава.\n⚙️ <b>Настройки</b> — дополнительные правила конкретной игры.\n➕ <b>Пригласить</b> — код + персональная ссылка создателю.\n▶️ <b>Начать</b> — запускает игру после проверки всех условий.\n\n💡 Нажатие кнопки не запускает скрытых действий: перед важными изменениями бот показывает результат.",
"how_it_works":"ℹ️ Как это работает",
"settings_help":"⚙️ <b>ЧТО ДЕЛАЮТ НАСТРОЙКИ</b>\n\n⚡ <b>Автостарт</b> — запуск при заполнении лобби.\n🟢 <b>Готовность</b> — каждый игрок отдельно подтверждает готовность.\n⏭ <b>Пропуск</b> — разрешает не выбирать игрока при голосовании.\n🩺 <b>Самолечение</b> — разрешает доктору лечить себя по лимиту.\n🔁 <b>Повтор лечения</b> — разрешает снова выбирать ту же цель.\n🔎 <b>Действие комиссара</b> — включает дополнительное выведение со 2-й ночи.\n⚖️ <b>Повтор при ничьей</b> — включает повторное голосование.\n⏱ <b>Доп. время</b> — позволяет группе запросить дополнительное время обсуждения.",
"role_config_text":"🎴 <b>СОСТАВ ИГРЫ</b>\n━━━━━━━━━━━━━━\n{roles}\n\n👥 Мест: <b>{total}</b>\n\n🔒 Мафия и Доктор обязательны. Остальные роли можно включать и выключать. Мирные автоматически занимают оставшиеся места.",
"lobby_v2":"🎭 <b>MAFIA LOBBY #{game_id}</b>\n━━━━━━━━━━━━━━\n🔑 Код комнаты: <code>{code}</code>\n👥 Игроки: <b>{count}/{max}</b>\n🎴 Состав: {roles}\n\n{players}\n\n⏳ Статус: <b>Ожидание игроков</b>\n\n💡 Используйте «ℹ️ Как это работает», если не знаете, что делает кнопка.",
"role_lover":"💗 Любовница","role_detective":"🕵️ Детектив","role_bodyguard":"🛡 Телохранитель",
"lover_guide":"📕 <b>ЛЮБОВНИЦА</b>\n\n🎯 Ночью выберите игрока. Его ночное действие будет заблокировано.\n🚫 Себя выбрать нельзя.\n🔐 Роль цели не раскрывается.",
"detective_guide":"📕 <b>ДЕТЕКТИВ</b>\n\n🎯 Ночью выберите игрока для проверки.\n🔎 Вы получите только результат по фракции: Мафия / не Мафия.\n🔐 Не раскрывайте свою роль.",
"bodyguard_guide":"📕 <b>ТЕЛОХРАНИТЕЛЬ</b>\n\n🛡 Ночью выберите игрока для защиты.\n🚫 Если на него направлена ночная атака, она отменяется.\n🎯 Выбирайте цель стратегически.",
"role_mafia_desc":"Командная роль. Ночью выбирайте общую цель с другими мафиози; днём скрывайте свою роль.",
"role_doctor_desc":"Защитная роль. Ночью лечите живого игрока и спасайте его от ночной атаки.",
"role_commissioner_desc":"Расследователь. Проверяйте игрока и сразу получайте результат по мафии; со 2-й ночи может быть дополнительное действие.",
"role_civilian_desc":"Мирная роль. Ночного действия нет. Анализируйте игроков и голосуйте днём.",
"role_lover_desc":"Блокирует ночное действие выбранного игрока. Себя выбрать нельзя.",
"role_detective_desc":"Проверяет игрока и получает только результат по фракции.",
"role_bodyguard_desc":"Защищает выбранного игрока от ночной атаки.",
"faq_text":"❔ <b>ЧАСТЫЕ ВОПРОСЫ</b>\n\n<b>Где код комнаты?</b> Прямо в сообщении лобби. Создатель также получает код через «Пригласить».\n\n<b>Как войти?</b> /join ABC123, кнопка «Войти в игру» или персональная ссылка.\n\n<b>Почему функция закрыта?</b> Сначала примите правила или проверьте, что вы живы и сейчас нужная фаза игры.\n\n<b>Почему игра не стартует?</b> Бот проверяет количество игроков, состав ролей, личные чаты и свои права в группе.",
},
"en": {}, "uz": {}
}
# English and Uzbek use compact translations of the same UX contract.
_V10_USER["en"] = {
"rules_full":"""🎭 <b>MAFIA RULES</b>\n━━━━━━━━━━━━━━\n<b>1. BEFORE THE GAME</b>\n• Open the User Bot, choose a language and accept the rules. All game functions stay locked until confirmation.\n• You must be in the game group. Roles, night actions and investigation results are private.\n• Never share your role or secret bot messages.\n\n<b>2. ROLES</b>\n🔴 <b>Mafia</b> — the night team. Each Mafia member proposes a target; the system resolves the shared decision. A clear most-supported target is used; a complete tie cancels the attack. Mafia wins at parity with the other living players.\n🩺 <b>Doctor</b> — protects one living player from a night attack. Self-heal and repeat targets depend on lobby settings.\n🔎 <b>Commissioner</b> — checks one living player and immediately receives Mafia / not Mafia. Night 1 is check-only; from Night 2 an extra elimination may be enabled by the creator.\n💗 <b>Lover</b> — blocks one player's night action. Cannot target self and does not learn the target's role.\n🕵️ <b>Detective</b> — checks one player and receives only their faction result.\n🛡 <b>Bodyguard</b> — protects one player; an attack against the protected target is cancelled.\n⚪ <b>Civilian</b> — has no night action; analyzes, discusses and votes during the day.\n\n<b>3. NIGHT</b>\n🌙 The group is closed for normal game messages. Night actions use private buttons and have timers.\n\n<b>4. DAY AND VOTING</b>\n☀️ Discussion — 2 minutes. Voting — 1 minute.\n• Only living players vote. No self-votes.\n• Votes can be changed before the timer ends.\n• Skip and revote-on-tie depend on lobby settings.\n\n<b>5. ELIMINATION</b>\n🚪 Roles stay hidden until the game ends. An eliminated player gets one 30-second last word, then becomes a spectator.\n\n<b>6. VICTORY</b>\n🏆 Civilians win when no Mafia remains.\n🏆 Mafia wins when Mafia equals or exceeds all other living players.\nAll roles are revealed and statistics are updated at the end.\n\n⚠️ Pressing “Accept rules” confirms that you read the rules and understand role secrecy.""",
"rules_required":"🔒 <b>Access locked</b>\n\nChoose a language, read the rules and press “Accept rules”. All game functions will then become available.",
"rules_accepted":"✅ <b>Rules accepted.</b>\n\n🎭 Game functions are now available. Use the menu below; complex buttons have their own instructions.",
"help_text":"❓ <b>HOW TO USE MAFIA</b>\n━━━━━━━━━━━━━━\n1️⃣ Open the bot and accept the rules.\n2️⃣ Add User Bot to the game group as administrator.\n3️⃣ Send /create in the group.\n4️⃣ The lobby shows a <b>room code</b>.\n5️⃣ Players use /join CODE or the personal invitation link.\n6️⃣ The creator configures players, roles and settings.\n7️⃣ Roles and night actions arrive privately.\n8️⃣ The group is closed at night; living players discuss and vote by day.\n\n💡 If a button is unclear, press “ℹ️ How it works”.\n\n⚠️ The bot needs delete-message and restrict-member permissions for moderation.",
"create_menu":"🎮 <b>CREATE GAME</b>\n━━━━━━━━━━━━━━\nAdd User Bot to the target group and send /create. The lobby will show the room code and controls.",
"create_in_group_text":"➕ <b>Create a game</b>\n\n1. Open the target group.\n2. Add User Bot as administrator.\n3. Grant delete-message and restrict-member permissions.\n4. Send /create.\n\n🎟 The lobby will show a shareable room code.",
"create_how":"🎮 <b>HOW TO CREATE A GAME</b>\n\n/create creates one lobby in the current group. The creator becomes the first player. Configure player count, roles and settings before starting.\n\n🔑 The room code is always shown in the lobby.\n🔗 “Invite” sends the creator the code and a personal link.\n▶️ Start runs all checks before the game begins.",
"join_hint":"🔗 <b>JOIN A GAME</b>\n\nEnter the room code from the lobby. Example:\n<code>/join ABC123</code>\n\nYou can also press “Join game” and send the code, or use a personal invitation link.",
"join_help":"ℹ️ How to join",
"join_help_text":"🔗 <b>HOW TO JOIN</b>\n\n<b>1:</b> /join ABC123\n<b>2:</b> Press “Join game” and send ABC123.\n<b>3:</b> Open the personal invitation link and press Start.\n\n⚠️ You must be a member of the game group and have accepted the rules.",
"invite_text":"🔗 <b>MAFIA LOBBY INVITATION</b>\n━━━━━━━━━━━━━━\n🔑 Code: <code>{code}</code>\n\n🔗 Personal link:\n{url}\n\nSend the link to a player. After Start, the bot will try to add them to this lobby.",
"lobby_help":"ℹ️ <b>LOBBY GUIDE</b>\n\n🔑 <b>Code</b> — main way to join.\n👥 <b>Players</b> — current players and free slots.\n🎴 <b>Roles</b> — configure the role composition.\n⚙️ <b>Settings</b> — game-specific options.\n➕ <b>Invite</b> — code + personal link to the creator.\n▶️ <b>Start</b> — starts only after all checks pass.",
"how_it_works":"ℹ️ How it works","settings_help":"⚙️ <b>GAME SETTINGS</b>\n\n⚡ <b>Auto start</b> — starts when the lobby is full.\n🟢 <b>Ready check</b> — every player confirms readiness.\n⏭ <b>Skip vote</b> — allows skipping a vote.\n🩺 <b>Doctor self-heal</b> — allows self-protection within its limit.\n🔁 <b>Repeat doctor target</b> — allows the same target again.\n🔎 <b>Commissioner action</b> — enables removal from Night 2.\n⚖️ <b>Revote on tie</b> — starts another vote after a tie.\n⏱ <b>Extra time</b> — lets the group request extra discussion time.",
"role_config_text":"🎴 <b>GAME COMPOSITION</b>\n━━━━━━━━━━━━━━\n{roles}\n\n👥 Slots: <b>{total}</b>\n\n🔒 Mafia and Doctor are mandatory. Other roles are optional; Civilians fill the remaining slots.",
"lobby_v2":"🎭 <b>MAFIA LOBBY #{game_id}</b>\n━━━━━━━━━━━━━━\n🔑 Room code: <code>{code}</code>\n👥 Players: <b>{count}/{max}</b>\n🎴 Roles: {roles}\n\n{players}\n\n⏳ Status: <b>Waiting for players</b>\n\n💡 Use “ℹ️ How it works” if a button is unclear.",
"role_lover":"💗 Lover","role_detective":"🕵️ Detective","role_bodyguard":"🛡 Bodyguard",
"lover_guide":"📕 <b>LOVER</b>\n\n🎯 Choose a player at night. Their night action is blocked.\n🚫 You cannot target yourself.\n🔐 You do not learn the target's role.",
"detective_guide":"📕 <b>DETECTIVE</b>\n\n🎯 Choose a player at night.\n🔎 You receive only Mafia / not Mafia.\n🔐 Keep your role secret.",
"bodyguard_guide":"📕 <b>BODYGUARD</b>\n\n🛡 Choose a player to protect at night.\n🚫 An attack against the protected target is cancelled.\n🎯 Choose strategically.",
"role_mafia_desc":"Team role. Choose a shared night target with other Mafia and hide your role by day.","role_doctor_desc":"Protective role. Protect a living player from a night attack.","role_commissioner_desc":"Investigator. Check a player and immediately learn Mafia / not Mafia; an extra action may be available from Night 2.","role_civilian_desc":"Town role. No night action. Analyze players and vote during the day.","role_lover_desc":"Blocks one player's night action. Cannot target self.","role_detective_desc":"Checks a player and receives only their faction result.","role_bodyguard_desc":"Protects one chosen player from a night attack.",
"faq_text":"❔ <b>FAQ</b>\n\n<b>Where is the room code?</b> It is shown directly in the lobby. The creator also gets it through “Invite”.\n\n<b>How do I join?</b> /join ABC123, the “Join game” button, or the personal link.\n\n<b>Why is a function locked?</b> Accept the rules first, or check that you are alive and the correct game phase is active.\n\n<b>Why won't the game start?</b> The bot checks player count, roles, private chats and group permissions."
}
_V10_USER["uz"] = {
"rules_full":"""🎭 <b>MAFIA QOIDALARI</b>\n━━━━━━━━━━━━━━\n<b>1. O'YINDAN OLDIN</b>\n• User Botni oching, tilni tanlang va qoidalarni qabul qiling. Tasdiqlamaguncha barcha o'yin funksiyalari yopiq.\n• O'yin guruhida bo'lishingiz kerak. Rollar, tungi harakatlar va tekshiruv natijalari faqat shaxsiy chatda keladi.\n• Rol yoki maxfiy bot xabarlarini boshqalarga yubormang.\n\n<b>2. ROLLAR</b>\n🔴 <b>Mafia</b> — tungi jamoa. Har bir mafia nishon taklif qiladi; tizim umumiy qarorni aniqlaydi. Eng ko'p qo'llab-quvvatlangan nishon tanlanadi, to'liq durangda hujum bekor qilinadi.\n🩺 <b>Doktor</b> — bitta tirik o'yinchini tungi hujumdan himoya qiladi. O'zini davolash va bir xil nishon sozlamaga bog'liq.\n🔎 <b>Komissar</b> — bitta tirik o'yinchini tekshiradi va darhol Mafia / Mafia emas natijasini oladi. 1-tunda faqat tekshiruv; 2-tundan qo'shimcha chiqarish yoqilishi mumkin.\n💗 <b>Sevishgan</b> — bitta o'yinchining tungi harakatini bloklaydi. O'zini tanlay olmaydi va nishon rolini bilmaydi.\n🕵️ <b>Detektiv</b> — bitta o'yinchini tekshiradi va faqat fraksiya natijasini oladi.\n🛡 <b>Tana qo'riqchisi</b> — bitta o'yinchini himoya qiladi; unga hujum bekor qilinadi.\n⚪ <b>Tinch fuqaro</b> — tungi harakatga ega emas; kunduz tahlil qiladi, muhokama qiladi va ovoz beradi.\n\n<b>3. TUN</b>\n🌙 Guruh oddiy o'yin xabarlari uchun yopiladi. Tungi harakatlar shaxsiy tugmalar va taymer orqali bajariladi.\n\n<b>4. KUN VA OVOZ</b>\n☀️ Muhokama — 2 daqiqa. Ovoz berish — 1 daqiqa.\n• Faqat tiriklar ovoz beradi. O'zingizga ovoz bera olmaysiz.\n• Taymer tugaguncha ovozni o'zgartirish mumkin.\n• O'tkazib yuborish va durangda qayta ovoz sozlamaga bog'liq.\n\n<b>5. CHIQISH</b>\n🚪 Rollar o'yin oxirigacha yashiriladi. Chiqib ketgan o'yinchiga 30 soniyalik so'nggi so'z beriladi, keyin u kuzatuvchiga aylanadi.\n\n<b>6. G'ALABA</b>\n🏆 Mafia qolmaganda tinchlar g'alaba qiladi.\n🏆 Mafia soni boshqa tirik o'yinchilarga teng yoki ko'p bo'lsa Mafia g'alaba qiladi.\nO'yin oxirida barcha rollar ochiladi va statistika yangilanadi.\n\n⚠️ «Qoidalarni qabul qilish» tugmasini bosish qoidalarni o'qiganingizni va rollar maxfiyligini tushunganingizni bildiradi.""",
"rules_required":"🔒 <b>Kirish yopiq</b>\n\nTilni tanlang, qoidalarni o'qing va «Qoidalarni qabul qilish» tugmasini bosing. Shundan keyin barcha o'yin funksiyalari ochiladi.",
"rules_accepted":"✅ <b>Qoidalar qabul qilindi.</b>\n\n🎭 Endi o'yin funksiyalari ochiq. Menyudan foydalaning; murakkab tugmalarda alohida ko'rsatma bor.",
"help_text":"❓ <b>MAFIA'DAN FOYDALANISH</b>\n━━━━━━━━━━━━━━\n1️⃣ Botni oching va qoidalarni qabul qiling.\n2️⃣ User Botni guruhga administrator qilib qo'shing.\n3️⃣ Guruhda /create yuboring.\n4️⃣ Lobbyda <b>xona kodi</b> ko'rsatiladi.\n5️⃣ O'yinchilar /join KOD yoki taklif havolasi orqali kiradi.\n6️⃣ Yaratuvchi o'yinchilar, rollar va sozlamalarni belgilaydi.\n7️⃣ Rollar va tungi harakatlar shaxsiy chatga keladi.\n8️⃣ Tunda guruh yopiq, kunduzi tiriklar muhokama va ovoz beradi.\n\n💡 Tushunarsiz tugma bo'lsa «ℹ️ Bu qanday ishlaydi» tugmasini bosing.",
"create_menu":"🎮 <b>O'YIN YARATISH</b>\n━━━━━━━━━━━━━━\nUser Botni kerakli guruhga qo'shing va /create yuboring. Lobbyda xona kodi va boshqaruv tugmalari chiqadi.",
"create_in_group_text":"➕ <b>O'yin yaratish</b>\n\n1. Kerakli guruhni oching.\n2. User Botni administrator qiling.\n3. Xabarlarni o'chirish va ishtirokchilarni cheklash huquqlarini bering.\n4. Guruhda /create yuboring.\n\n🎟 Lobbyda xona kodi chiqadi.",
"create_how":"🎮 <b>O'YINNI QANDAY YARATISH</b>\n\n/create joriy guruhda lobby yaratadi. Yaratuvchi birinchi o'yinchi bo'ladi. O'yinchi soni, rollar va sozlamalarni o'zgartiring.\n\n🔑 Xona kodi doim lobbyda ko'rinadi.\n🔗 «Taklif» yaratuvchiga kod va shaxsiy havolani yuboradi.\n▶️ Start barcha shartlarni tekshirgandan keyin o'yinni boshlaydi.",
"join_hint":"🔗 <b>O'YINGA KIRISH</b>\n\nLobbydagi xona kodini kiriting. Masalan:\n<code>/join ABC123</code>\n\nYoki «O'yinga kirish» tugmasini bosib kodni yuboring. Shaxsiy taklif havolasidan ham foydalanishingiz mumkin.",
"join_help":"ℹ️ Qanday kirish","join_help_text":"🔗 <b>LOBBYGA QANDAY KIRISH</b>\n\n<b>1:</b> /join ABC123\n<b>2:</b> «O'yinga kirish» tugmasini bosing va ABC123 yuboring.\n<b>3:</b> Shaxsiy taklif havolasini ochib Start bosing.\n\n⚠️ O'yin guruhida bo'lishingiz va qoidalarni qabul qilgan bo'lishingiz kerak.",
"invite_text":"🔗 <b>MAFIA LOBBY TAKLIFI</b>\n━━━━━━━━━━━━━━\n🔑 Kod: <code>{code}</code>\n\n🔗 Shaxsiy havola:\n{url}\n\nHavolani o'yinchiga yuboring. Start bosilgach, bot uni lobbyga qo'shishga urinadi.",
"lobby_help":"ℹ️ <b>LOBBY YO'RIQNOMASI</b>\n\n🔑 <b>Kod</b> — kirishning asosiy usuli.\n👥 <b>O'yinchilar</b> — hozirgi tarkib va bo'sh joylar.\n🎴 <b>Rollar</b> — rol tarkibini sozlash.\n⚙️ <b>Sozlamalar</b> — o'yin parametrlari.\n➕ <b>Taklif</b> — kod va shaxsiy havola.\n▶️ <b>Start</b> — barcha tekshiruvlardan keyin boshlaydi.",
"how_it_works":"ℹ️ Qanday ishlaydi","settings_help":"⚙️ <b>O'YIN SOZLAMALARI</b>\n\n⚡ Avtostart — lobby to'lganda boshlaydi.\n🟢 Tayyorlik — har bir o'yinchi tayyorligini tasdiqlaydi.\n⏭ O'tkazish — ovozda hech kimni tanlamaslikka ruxsat beradi.\n🩺 Doktor o'zini davolashi — sozlamadagi limit bilan o'zini himoya qiladi.\n🔁 Takroriy davolash — bir xil nishonni yana tanlashga ruxsat beradi.\n🔎 Komissar harakati — 2-tundan chiqarishni yoqadi.\n⚖️ Durangda qayta ovoz — yangi ovoz beradi.\n⏱ Qo'shimcha vaqt — muhokamaga qo'shimcha vaqt so'rashga ruxsat beradi.",
"role_config_text":"🎴 <b>O'YIN TARKIBI</b>\n━━━━━━━━━━━━━━\n{roles}\n\n👥 Joylar: <b>{total}</b>\n\n🔒 Mafia va Doktor majburiy. Qolgan rollar ixtiyoriy; qolgan joylarni tinchlar to'ldiradi.",
"lobby_v2":"🎭 <b>MAFIA LOBBY #{game_id}</b>\n━━━━━━━━━━━━━━\n🔑 Xona kodi: <code>{code}</code>\n👥 O'yinchilar: <b>{count}/{max}</b>\n🎴 Rollar: {roles}\n\n{players}\n\n⏳ Holat: <b>O'yinchilar kutilmoqda</b>\n\n💡 Tushunarsiz tugma bo'lsa «ℹ️ Qanday ishlaydi»ni bosing.",
"role_lover":"💗 Sevishgan","role_detective":"🕵️ Detektiv","role_bodyguard":"🛡 Tana qo'riqchisi",
"lover_guide":"📕 <b>SEVISHGAN</b>\n\n🎯 Tunda o'yinchini tanlang. Uning tungi harakati bloklanadi.\n🚫 O'zingizni tanlay olmaysiz.\n🔐 Nishon roli ko'rsatilmaydi.","detective_guide":"📕 <b>DETEKTIV</b>\n\n🎯 Tunda o'yinchini tanlang.\n🔎 Faqat Mafia / Mafia emas natijasini olasiz.\n🔐 Rolingizni sir tuting.","bodyguard_guide":"📕 <b>TANA QO'RIQCHISI</b>\n\n🛡 Tunda himoya qilinadigan o'yinchini tanlang.\n🚫 Unga hujum bekor qilinadi.",
"role_mafia_desc":"Jamoaviy rol. Tunda umumiy nishon tanlang, kunduzi rolingizni yashiring.","role_doctor_desc":"Himoya roli. Tunda tirik o'yinchini himoya qiling.","role_commissioner_desc":"Tekshiruvchi. O'yinchini tekshiring; 2-tundan qo'shimcha harakat yoqilishi mumkin.","role_civilian_desc":"Tinch rol. Tungi harakat yo'q; kunduzi tahlil va ovoz bering.","role_lover_desc":"Tanlangan o'yinchining tungi harakatini bloklaydi.","role_detective_desc":"O'yinchini tekshiradi va fraksiya natijasini oladi.","role_bodyguard_desc":"Tanlangan o'yinchini tungi hujumdan himoya qiladi.",
"faq_text":"❔ <b>FAQ</b>\n\n<b>Xona kodi qayerda?</b> Lobby xabarining o'zida. Yaratuvchi «Taklif» orqali ham oladi.\n\n<b>Qanday kiraman?</b> /join ABC123, «O'yinga kirish» yoki shaxsiy havola.\n\n<b>Nega funksiya yopiq?</b> Avval qoidalarni qabul qiling yoki tirikligingiz va o'yin fazasini tekshiring.\n\n<b>Nega o'yin boshlanmayapti?</b> Bot o'yinchilar soni, rollar, shaxsiy chatlar va guruh huquqlarini tekshiradi."
}
for _lang, _vals in _V10_USER.items():
    if _vals:
        TEXT[_lang].update(_vals)
