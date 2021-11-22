from telebot import types
from config import host, user, password, db_name
import config
import telebot #pip pytelegrambotapi
import time
#import asyncio
import datetime
import glob
import os.path
import pymysql #pip pymysql
from multiprocessing import *
import schedule #pip schedule
import random
import requests

def connection_mysql():
	return pymysql.connect(host=host,port=3306,user=user,password=password,database=db_name,cursorclass=pymysql.cursors.DictCursor,)

bot = telebot.TeleBot(config.TOKEN)

tconv = lambda x: time.strftime("%d.%m.%Y / %H:%M:%S", time.localtime(x))
timenow = lambda x: time.strftime("%H:%M", time.localtime(x))
timenowsec = lambda x: time.strftime("%H:%M:%S", time.localtime(x))
datenow = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))

def start_process():#Запуск Process
	p1 = Process(target=P_schedule.start_schedule, args=()).start()

class P_schedule(): # Class для работы с schedule

	def start_schedule(): #Запуск schedule
		######Параметры для schedule######
		#schedule.every().day.at("19:00").do(P_schedule.send_message1)
		#schedule.every().day.at("00:01").do(P_schedule.send_message3)
		schedule.every(2).hours.do(P_schedule.send_message2)
		schedule.every(10).seconds.do(P_schedule.check_dialog)
		##################################
		
		while True: #Запуск цикла
			schedule.run_pending()
			time.sleep(1)

	####Функции для выполнения заданий по времени  
	def send_message1():
		return
		'''
		try:
			bot.send_message('', 'Бот работает')
		except:
			print('Пользователя нет')
		'''
	def send_message2():
		return
		'''
		try:
			bot.send_message('', 'Бот работает')
		except:
			print('Пользователя нет')
		'''
	def check_dialog():
		try:
			#bot.clear_step_handler_by_chat_id(message.chat.id)
			connection = connection_mysql()
			with connection.cursor() as cursor:
				cursor.execute("SELECT count(*) FROM `awaiting`")
				result = cursor.fetchone()
				result = result['count(*)']
				if result > 0:
					i = 0
					cursor.execute("SELECT * FROM `awaiting`")
					rows = cursor.fetchall()
					#print(rows)
					idd = []
					chat_id = []
					msg_id = []
					sex = []
					prefer_sex = []
					wait_time = []
					for row in rows:
						idd.append(row['id'])
						chat_id.append(row['chat_id'])
						msg_id.append(row['msg_id'])
						sex.append(row['sex'])
						prefer_sex.append(row['prefer_sex'])
						wait_time.append(row['wait_time'])

					for row in rows:
						select_id = "SELECT count(*) FROM `awaiting` WHERE chat_id={0}".format(row['chat_id'])
						cursor.execute(select_id)
						count = cursor.fetchone()
						count = count['count(*)']
						select_id = "SELECT count(*) FROM `awaiting` WHERE NOT chat_id={0}".format(row['chat_id'])
						cursor.execute(select_id)
						counts = cursor.fetchone()
						counts = counts['count(*)']

						if (row['prefer_sex'] > 0) and (count > 0):
							select_id = "SELECT count(*) FROM `awaiting` WHERE sex={0} AND NOT chat_id={1}".format(row['prefer_sex'],row['chat_id'])
							cursor.execute(select_id)
							counts = cursor.fetchone()
							counts = counts['count(*)']
							ii = 1
							if counts > 0:
								select_id = "SELECT * FROM `awaiting` WHERE sex={0} AND NOT chat_id={1}".format(row['prefer_sex'],row['chat_id'])
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								idd2 = []
								chat_id2 = []
								msg_id2 = []
								sex2 = []
								prefer_sex2 = []
								wait_time2 = []
								for row2 in rows2:
									idd2.append(row2['id'])
									chat_id2.append(row2['chat_id'])
									msg_id2.append(row2['msg_id'])
									sex2.append(row2['sex'])
									prefer_sex2.append(row2['prefer_sex'])
									wait_time2.append(row2['wait_time'])
								choose = random.choice(list(idd2))

								print(choose)
								ii = ii + 1
								idd_main = row['id']
								chat_id_main = row['chat_id']
								msg_id_main = row['msg_id']
								sex_main = row['sex']
								prefer_sex_main = row['prefer_sex']
								wait_time_main = row['wait_time']
								select_id = "SELECT age FROM `users` WHERE chat_id="+str(chat_id_main)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									age_main = row2['age']
								select_id = "SELECT chat_id FROM `awaiting` WHERE id="+str(choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									chat_id_choose = row2['chat_id']
								select_id = "SELECT age FROM `users` WHERE chat_id="+str(chat_id_choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									age_choose = row2['age']
								select_id = "SELECT msg_id FROM `awaiting` WHERE id="+str(choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									msg_id_choose = row2['msg_id']
								select_id = "SELECT sex FROM `awaiting` WHERE id="+str(choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									sex_choose = row2['sex']
								select_id = "SELECT rating FROM `users` WHERE chat_id="+str(chat_id_main)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									rating_main = row2['rating']

								select_id = "SELECT rating FROM `users` WHERE chat_id="+str(chat_id_choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									rating_choose = row2['rating']
								insert_query = "DELETE FROM `awaiting` WHERE chat_id={0}".format(chat_id_main)
								cursor.execute(insert_query)
								connection.commit()

								insert_query = "DELETE FROM `awaiting` WHERE chat_id={0}".format(chat_id_choose)
								cursor.execute(insert_query)
								connection.commit()

								cursor.execute("SELECT count(*) FROM `current_dialogs`")
								dial = cursor.fetchone()
								dial1 = dial['count(*)']
								dialogs = dial1 + 1

								insert_query = "INSERT INTO `current_dialogs` (id,chat_id1,chat_id2) VALUES ({0},{1},{2});".format(str(dialogs),str(chat_id_main),str(chat_id_choose))
								cursor.execute(insert_query)
								connection.commit()

								bot.clear_step_handler_by_chat_id(chat_id_main)
								bot.clear_step_handler_by_chat_id(chat_id_choose)

								bot.delete_message(chat_id_main, msg_id_main)
								bot.delete_message(chat_id_choose, msg_id_choose)

								txt1 = "Собеседник найден!\nРейтинг собеседника: {0}\nВозраст собеседника: {1}\nИ это {2}. \nЕсли хотите заверишить разговор, напишите /stop".format(str(rating_main),str(age_main),check_sex(sex_main))
								txt2 = "Собеседник найден!\nРейтинг собеседника: {0}\nВозраст собеседника: {1}\nИ это {2}. \nЕсли хотите заверишить разговор, напишите /stop".format(str(rating_choose),str(age_choose),check_sex(sex_choose))
								keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
								keyboard.add('/stop')

								bot.send_message(chat_id_main, txt1,reply_markup=keyboard)
								bot.send_message(chat_id_choose, txt2,reply_markup=keyboard)
						elif (row['prefer_sex'] == 0) and (count > 0) and (counts > 0):
							select_id = "SELECT count(*) FROM `awaiting` WHERE NOT chat_id={0} AND NOT prefer_sex=1 AND NOT prefer_sex=2".format(row['chat_id'])
							cursor.execute(select_id)
							countss = cursor.fetchone()
							countss = countss['count(*)']
							if countss > 0:
								select_id = "SELECT * FROM `awaiting` WHERE NOT chat_id={0} AND NOT prefer_sex=1 AND NOT prefer_sex=2".format(row['chat_id'])
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								idd2 = []
								chat_id2 = []
								msg_id2 = []
								sex2 = []
								prefer_sex2 = []
								wait_time2 = []
								for row2 in rows2:
									idd2.append(row2['id'])
									chat_id2.append(row2['chat_id'])
									msg_id2.append(row2['msg_id'])
									sex2.append(row2['sex'])
									prefer_sex2.append(row2['prefer_sex'])
									wait_time2.append(row2['wait_time'])
								choose = random.choice(list(idd2))
								idd_main = row['id']
								chat_id_main = row['chat_id']
								msg_id_main = row['msg_id']
								sex_main = row['sex']
								prefer_sex_main = row['prefer_sex']
								wait_time_main = row['wait_time']
								select_id = "SELECT age FROM `users` WHERE chat_id="+str(chat_id_main)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									age_main = row2['age']
								select_id = "SELECT chat_id FROM `awaiting` WHERE id="+str(choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									chat_id_choose = row2['chat_id']
								select_id = "SELECT age FROM `users` WHERE chat_id="+str(chat_id_choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									age_choose = row2['age']
								select_id = "SELECT msg_id FROM `awaiting` WHERE id="+str(choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									msg_id_choose = row2['msg_id']
								select_id = "SELECT sex FROM `awaiting` WHERE id="+str(choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									sex_choose = row2['sex']
								select_id = "SELECT rating FROM `users` WHERE chat_id="+str(chat_id_main)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									rating_main = row2['rating']

								select_id = "SELECT rating FROM `users` WHERE chat_id="+str(chat_id_choose)
								cursor.execute(select_id)
								rows2 = cursor.fetchall()
								for row2 in rows2:
									rating_choose = row2['rating']
								insert_query = "DELETE FROM `awaiting` WHERE chat_id={0}".format(chat_id_main)
								cursor.execute(insert_query)
								connection.commit()

								insert_query = "DELETE FROM `awaiting` WHERE chat_id={0}".format(chat_id_choose)
								cursor.execute(insert_query)
								connection.commit()

								cursor.execute("SELECT count(*) FROM `current_dialogs`")
								dial = cursor.fetchone()
								dial1 = dial['count(*)']
								dialogs = dial1 + 1

								insert_query = "INSERT INTO `current_dialogs` (id,chat_id1,chat_id2) VALUES ({0},{1},{2});".format(str(dialogs),str(chat_id_main),str(chat_id_choose))
								cursor.execute(insert_query)
								connection.commit()

								bot.clear_step_handler_by_chat_id(chat_id_main)
								bot.clear_step_handler_by_chat_id(chat_id_choose)

								bot.delete_message(chat_id_main, msg_id_main)
								bot.delete_message(chat_id_choose, msg_id_choose)

								txt1 = "Собеседник найден!\nРейтинг собеседника: {0}\nВозраст собеседника: {1}\nИ это {2}. \nЕсли хотите заверишить разговор, напишите /stop".format(str(rating_main),str(age_main),check_sex(sex_main))
								txt2 = "Собеседник найден!\nРейтинг собеседника: {0}\nВозраст собеседника: {1}\nИ это {2}. \nЕсли хотите заверишить разговор, напишите /stop".format(str(rating_choose),str(age_choose),check_sex(sex_choose))
								keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
								keyboard.add('/stop')

								bot.send_message(chat_id_main, txt1,reply_markup=keyboard)
								bot.send_message(chat_id_choose, txt2,reply_markup=keyboard)



					select_id = "SELECT * FROM `awaiting`"
					cursor.execute(select_id)
					rows = cursor.fetchall()
					for row in rows:
						iddd = row['id']
						chat_id = row['chat_id']
						wait_time = row['wait_time']
						wait_time = wait_time + 10
						if wait_time == 120:
							insert_query = "DELETE FROM `awaiting` WHERE id={0}".format(iddd)
							cursor.execute(insert_query)
							connection.commit()
							txt = "К сожалению, никого не нашлось. Попробуй позже"
							msg = bot.send_message(chat_id, txt, parse_mode="html")
							time.sleep(1)
							welcome(msg)
						else:
							insert_query = "UPDATE `awaiting` SET wait_time = {0} WHERE id = {1}".format(wait_time,iddd)
							cursor.execute(insert_query)
							connection.commit()
							txt = "<i>...время твоего ожидания около </i><b>{0}</b> <i>секунд</i>".format(str(wait_time))
							bot.send_message(chat_id, txt, parse_mode="html")
				cursor.execute("SELECT count(*) FROM `current_dialogs`")
				result = cursor.fetchone()
				result = result['count(*)']
				y = result + 1
				if result > 0:
					cursor.execute("SELECT * FROM `current_dialogs`")
					dialogs = cursor.fetchall()
					for row in dialogs:
						i = row['id']
						last_msg1 = row['last_msg1']
						last_msg2 = row['last_msg2']
						chat_id1 = row['chat_id1']
						chat_id2 = row['chat_id2']
						if last_msg1 >= 120:
							insert_query = "DELETE FROM `current_dialogs` WHERE chat_id1={0}".format(chat_id1)
							cursor.execute(insert_query)
							connection.commit()

							text1 = 'Собеседник вышел из чата\nТы можешь поставь ему оценку'
							text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

							markup1 = types.InlineKeyboardMarkup()
							button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(chat_id1))
							button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(chat_id1))
							markup1.add(button1, button2)
							markup2 = types.InlineKeyboardMarkup()
							button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(chat_id1))
							button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
							markup2.add(button3)
							markup2.add(button4)

							bot.send_message(chat_id2, text1, parse_mode="html", reply_markup=markup1)

							time.sleep(1)

							bot.send_message(chat_id2, text2, parse_mode="html", reply_markup=markup2)

							text = 'Ты вышел из чата\nПоставь оценку собеседнику'
							text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

							markup1 = types.InlineKeyboardMarkup()
							button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(chat_id2))
							button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(chat_id2))
							markup1.add(button1, button2)
							markup2 = types.InlineKeyboardMarkup()
							button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(chat_id2))
							button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
							markup2.add(button3)
							markup2.add(button4)
									
							bot.send_message(chat_id1, text, parse_mode="html", reply_markup=markup1)

							time.sleep(1)

							bot.send_message(chat_id1, text2, parse_mode="html", reply_markup=markup2)
						elif last_msg2 >= 120:
							insert_query = "DELETE FROM `current_dialogs` WHERE chat_id1={0}".format(chat_id2)
							cursor.execute(insert_query)
							connection.commit()

							text1 = 'Собеседник вышел из чата\nТы можешь поставь ему оценку'
							text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

							markup1 = types.InlineKeyboardMarkup()
							button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(chat_id2))
							button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(chat_id2))
							markup1.add(button1, button2)
							markup2 = types.InlineKeyboardMarkup()
							button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(chat_id2))
							button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
							markup2.add(button3)
							markup2.add(button4)

							bot.send_message(chat_id1, text1, parse_mode="html", reply_markup=markup1)

							time.sleep(1)

							bot.send_message(chat_id1, text2, parse_mode="html", reply_markup=markup2)

							text = 'Ты вышел из чата\nПоставь оценку собеседнику'
							text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

							markup1 = types.InlineKeyboardMarkup()
							button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(chat_id1))
							button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(chat_id1))
							markup1.add(button1, button2)
							markup2 = types.InlineKeyboardMarkup()
							button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(chat_id1))
							button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
							markup2.add(button3)
							markup2.add(button4)
									
							bot.send_message(chat_id2, text, parse_mode="html", reply_markup=markup1)

							time.sleep(1)

							bot.send_message(chat_id2, text2, parse_mode="html", reply_markup=markup2)
						else:
							last_msg1 = last_msg1 + 10
							last_msg2 = last_msg2 + 10
							insert_query = "UPDATE `current_dialogs` SET last_msg1 = {0} WHERE chat_id1 = {1};".format(last_msg1,chat_id1)
							cursor.execute(insert_query)
							connection.commit()
							insert_query = "UPDATE `current_dialogs` SET last_msg2 = {0} WHERE chat_id2 = {1};".format(last_msg2,chat_id2)
							cursor.execute(insert_query)
							connection.commit()
				connection.close()
		except Exception as ex:
			print("Connection refused...")
			print(ex)

def check_sex(sex):
	if sex == 1:
		txt = "мужчина"
		return txt
	else:
		txt = "женщина"
		return txt

def printer(printing, date):
	log_file = open(logf, "a")
	print('['+tconv(date)+']: '+str(printing))
	log_file.write('['+tconv(date)+']: '+str(printing)+'\n')
	log_file.close()
	return printer


def add_ban(message, num):
	if message.text == '/start':
		bot.clear_step_handler_by_chat_id(message.chat.id)
		welcome(message)
		return
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:

			insert_query = "DELETE FROM `complains` WHERE def_id="+num
			cursor.execute(insert_query)
			connection.commit()

			text = num.replace("'", " ")
			text = text.replace("`", " ")
			text = text.replace("~", " ")
			text = text.replace("&", " ")
			text = text.replace("(", " ")
			text = text.replace(")", " ")
			text = text.replace(",", " ")
			text = text.replace(";", " ")
			text = text.replace("{", " ")
			text = text.replace("}", " ")
			text = text.replace('"', ' ')
			text = text.replace(".", " ")
			text = text.replace(":", " ")
			text = text.replace("/", " ")
			insert_query = "INSERT INTO `banlist` (user_id,reason) VALUES ({0},'{1}');".format(num,message.text)
			cursor.execute(insert_query)
			connection.commit()

			connection.close()

			bot.send_message(message.chat.id, "Пользователь заблокирован",parse_mode="html", reply_markup=None)
			time.sleep(1)
			admin_answer(message)
	except Exception as ex:
		print("Connection refused...")
		print(ex)	

	bot.clear_step_handler_by_chat_id(message.chat.id)
	txt = "Функция сработала + "+num
	msg = bot.send_message(message.chat.id, txt,reply_markup=None)


def podbor(message):
	check_chat = False
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			select_id = "SELECT * FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
			#chat_id = 0
			chat = cursor.execute(select_id)
			if chat == 0:
				bot.clear_step_handler_by_chat_id(message.chat.id)
				select_id = "SELECT * FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
				chat = cursor.execute(select_id)
				if chat == 1:
					if message.text == '/start':
						bot.clear_step_handler_by_chat_id(message.chat.id)
						welcome(message)
						insert_query = "DELETE FROM `awaiting` WHERE chat_id="+str(message.chat.id)
						cursor.execute(insert_query)
						connection.commit()
						connection.close()
						return
					select_id = "SELECT chat_id1 FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
					rows = cursor.fetchall()
					for row in rows:
						chat_id = row['chat_id1']
					bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
					insert_query = "INSERT INTO `messages` (id_sender, id_recipient , msg_id) VALUES ({0},{1},{2});".format(message.chat.id,chat_id,message.message_id)
					cursor.execute(insert_query)
					connection.commit()
					insert_query = "UPDATE `current_dialogs` SET last_msg2 = 0 WHERE chat_id2 = {0};".format(message.chat.id)
					cursor.execute(insert_query)
					connection.commit()
				else:
					if message.text == '/start':
						bot.clear_step_handler_by_chat_id(message.chat.id)
						welcome(message)
						insert_query = "DELETE FROM `awaiting` WHERE chat_id="+str(message.chat.id)
						cursor.execute(insert_query)
						connection.commit()
						connection.close()
						return
					bot.clear_step_handler_by_chat_id(message.chat.id)
					msg = bot.send_message(message.chat.id, "Идёт подбор")
					bot.register_next_step_handler(msg, podbor)
			elif chat == 1:
				if message.text == '/start':
					bot.clear_step_handler_by_chat_id(message.chat.id)
					welcome(message)
					insert_query = "DELETE FROM `awaiting` WHERE chat_id="+str(message.chat.id)
					cursor.execute(insert_query)
					connection.commit()
					connection.close()
					return
				bot.clear_step_handler_by_chat_id(message.chat.id)
				select_id = "SELECT chat_id2 FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
				rows = cursor.fetchall()
				for row in rows:
					chat_id = row['chat_id2']
				bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
				insert_query = "INSERT INTO `messages` (id_sender, id_recipient , msg_id) VALUES ({0},{1},{2});".format(message.chat.id,chat_id,message.message_id)
				cursor.execute(insert_query)
				connection.commit()
				insert_query = "UPDATE `current_dialogs` SET last_msg1 = 0 WHERE chat_id1 = {0};".format(message.chat.id)
				cursor.execute(insert_query)
				connection.commit()
			else:
				if message.text == '/start':
					bot.clear_step_handler_by_chat_id(message.chat.id)
					welcome(message)
					insert_query = "DELETE FROM `awaiting` WHERE chat_id="+str(message.chat.id)
					cursor.execute(insert_query)
					connection.commit()
					connection.close()
					return
				bot.clear_step_handler_by_chat_id(message.chat.id)
				msg = bot.send_message(message.chat.id, "Идёт подбор")
				bot.register_next_step_handler(msg, podbor)
			connection.close()
	except Exception as ex:
		print("Connection refused...")
		print(ex)

def need_sex(message):
	if message.text == '/start':
		bot.clear_step_handler_by_chat_id(message.chat.id)
		welcome(message)
		return
	user_id = message.chat.id
	markup1 = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton("М", callback_data='formen')
	button2 = types.InlineKeyboardButton("Ж", callback_data='forwomen')
	markup1.add(button1, button2)
	bot.clear_step_handler_by_chat_id(message.chat.id)
	msg = bot.send_message(message.chat.id, "Сначала нужно указать свой пол",reply_markup=markup1)
	bot.register_next_step_handler(msg, need_sex)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def need_age(message):
	chat_id = message.chat.id
	text = message.text
	cc = len(message.text)
	if text == '/start':
		welcome(message)
		return
	if not is_integer(text):#(15000<float(text)<25) Если это НЕ ЧИСЛО
		bot.clear_step_handler_by_chat_id(message.chat.id)
		msg = bot.send_message(chat_id, 'Что-то пошло не так. Нужно ввести число')
		bot.register_next_step_handler(msg, need_age)
		return
	elif (int(text) < 12) or (int(text) > 80):
		bot.clear_step_handler_by_chat_id(message.chat.id)
		msg = bot.send_message(chat_id, 'Возраст не подходит')
		bot.register_next_step_handler(msg, need_age)
		return
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			insert_query = "UPDATE `users` SET age = {0} WHERE chat_id = {1};".format(text,message.chat.id)
			cursor.execute(insert_query)
			connection.commit()
			insert_query = "UPDATE `users_start` SET newuser = 0 WHERE chat_id = {0};".format(message.chat.id)
			cursor.execute(insert_query)
			connection.commit()
			connection.close()
	except Exception as ex:
		print("Connection refused...")
		print(ex)
	welcome(message)


def add_vip_msg(message):
	#print(message.forward_from)
	try:
		neww = "ID Пользователя: {0}\nИмя: {1}\nИмя пользователя: {2}".format(message.forward_from.id,message.forward_from.first_name, message.forward_from.username)
		bot.send_message(message.chat.id, neww, parse_mode="html")
		markup1 = types.InlineKeyboardMarkup()
		texxt = "Если всё верно, нажми ДА"
		button1 = types.InlineKeyboardButton("ДА", callback_data='vipconfirm'+str(message.forward_from.id))
		button2 = types.InlineKeyboardButton("Нет, вернуться в админ-панель", callback_data='adminpanel')
		markup1.add(button1)
		markup1.add(button2)
		bot.send_message(message.chat.id, texxt, parse_mode="html",reply_markup=markup1)

	except Exception as ex:
		bot.send_message(message.chat.id, "Не удалось определить пользователя", parse_mode="html")
		print(ex)


@bot.message_handler(commands=['start'])
def welcome(message):
	bot.clear_step_handler_by_chat_id(message.chat.id)
	user_id = message.chat.id
	#printer('START', message.date)
	newuser = 1
	rating = 0
	sex = 0
	age = 0
	time.sleep(1)
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			select_id = "SELECT chat_id FROM `users_start` WHERE chat_id="+str(user_id)
			checkUsername = 0
			checkUsername = cursor.execute(select_id)
			if checkUsername != 0:
				print('Пользователь есть')
			else:
				insert_query = "INSERT INTO `users_start` (chat_id,f_name) VALUES ({0},'{1.first_name}');".format(user_id,message.chat)
				cursor.execute(insert_query)
				connection.commit()
			
			select_id = "SELECT newuser FROM `users_start` WHERE chat_id="+str(user_id)
			cursor.execute(select_id)
			rows = cursor.fetchall()
			for row in rows:
				newuser = row['newuser']
			connection.close()
			
	except Exception as ex:
		print("Connection refused...")
		print(ex)
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			if not newuser:
				select_id = "SELECT rating FROM `users` WHERE chat_id="+str(user_id)
				cursor.execute(select_id)
				rows = cursor.fetchall()
				for row in rows:
					rating = row['rating']
				select_id = "SELECT age FROM `users` WHERE chat_id="+str(user_id)
				cursor.execute(select_id)
				rows = cursor.fetchall()
				for row in rows:
					age = row['age']
				select_id = "SELECT sex FROM `users` WHERE chat_id="+str(user_id)
				cursor.execute(select_id)
				rows = cursor.fetchall()
				for row in rows:
					sex = row['sex']
				if sex == 1:
					sex = "Мужчина"
				else:
					sex = "Женщина"

				select_id = "SELECT user_id FROM `users_vip` WHERE user_id="+str(user_id)
				checkUsername = 0
				checkUsername = cursor.execute(select_id)
				if checkUsername != 0:
					txt = "VIP пользователь\nТвой пол: {0}\nТвой возраст: {1}\nТвой рейтинг: {2}".format(sex,str(age),str(rating))
					markup1 = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("Подобрать собеседника (любой пол)", callback_data='awaiting'+'0')
					button2 = types.InlineKeyboardButton("Подобрать собеседника (только м)", callback_data='awaiting'+'1')
					button3 = types.InlineKeyboardButton("Подобрать собеседника (только ж)", callback_data='awaiting'+'2')
					button4 = types.InlineKeyboardButton("Изменить свои данные", callback_data='data')
					markup1.add(button1)
					markup1.add(button2)
					markup1.add(button3)
					markup1.add(button4)
					bot.send_message(message.chat.id, txt,reply_markup=None)
					time.sleep(1)
					msg = bot.send_message(message.chat.id, "Какое действие нужно сделать?",reply_markup=markup1)

				else:
					txt = "Зарегистрированный пользователь\nТвой пол: {0}\nТвой возраст: {1}\nТвой рейтинг: {2}".format(sex,str(age),str(rating))
					markup1 = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("Подобрать собеседника", callback_data='awaiting'+'0')
					button2 = types.InlineKeyboardButton("Изменить свои данные", callback_data='data')
					button3 = types.InlineKeyboardButton("Купить VIP", callback_data='vip')
					markup1.add(button1, button2)
					markup1.add(button3)
					bot.send_message(message.chat.id, txt,reply_markup=None)
					time.sleep(1)
					msg = bot.send_message(message.chat.id, "Какое действие нужно сделать?",reply_markup=markup1)
			else:
				markup1 = types.InlineKeyboardMarkup()
				button1 = types.InlineKeyboardButton("Подобрать собеседника", callback_data='awaiting'+'0')
				button2 = types.InlineKeyboardButton("Купить VIP", callback_data='vip')
				markup1.add(button1, button2)
				msg = bot.send_message(message.chat.id, "Незарегистрированный пользователь",reply_markup=markup1)
			connection.close()
	except Exception as ex:
		print("Connection refused...")
		print(ex)


@bot.message_handler(commands=['adminkwork'])
def admin_answer(message):
	markup1 = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton("Статистика", callback_data='stats')
	button2 = types.InlineKeyboardButton("Посмотреть жалобы", callback_data='listcomplains')
	button3 = types.InlineKeyboardButton("Добавить пользователя в VIP", callback_data='vipadd')
	markup1.add(button1, button2)
	markup1.add(button3)
	txt = "Админ-панель"
	bot.send_message(message.chat.id, txt,reply_markup=None)
	time.sleep(1)
	txt =  "Выбери пункт меню:"
	msg = bot.send_message(message.chat.id, txt,reply_markup=markup1)



@bot.message_handler(commands=['stop'])
def stop(message):
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			select_id = "SELECT * FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
			chat = cursor.execute(select_id)
			if chat == 0:
				select_id = "SELECT * FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
				chat = cursor.execute(select_id)
				if chat == 1:
					select_id = "SELECT chat_id1 FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
					rows = cursor.fetchall()
					for row in rows:
						chat_id = row['chat_id1']

					insert_query = "DELETE FROM `current_dialogs` WHERE chat_id2={0}".format(str(message.chat.id))
					cursor.execute(insert_query)
					connection.commit()

					text1 = 'Собеседник вышел из чата\nТы можешь поставь ему оценку'
					text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

					markup1 = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(message.chat.id))
					button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(message.chat.id))
					markup1.add(button1, button2)
					markup2 = types.InlineKeyboardMarkup()
					button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(message.chat.id))
					button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
					markup2.add(button3)
					markup2.add(button4)

					bot.send_message(chat_id, text1, parse_mode="html", reply_markup=markup1)

					time.sleep(1)

					bot.send_message(chat_id, text2, parse_mode="html", reply_markup=markup2)

					text = 'Ты вышел из чата\nПоставь оценку собеседнику'
					text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

					markup1 = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(chat_id))
					button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(chat_id))
					markup1.add(button1, button2)
					markup2 = types.InlineKeyboardMarkup()
					button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(chat_id))
					button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
					markup2.add(button3)
					markup2.add(button4)
					
					bot.send_message(message.chat.id, text, parse_mode="html", reply_markup=markup1)

					time.sleep(1)

					bot.send_message(message.chat.id, text2, parse_mode="html", reply_markup=markup2)


					#bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
			elif chat == 1:
				select_id = "SELECT chat_id2 FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
				rows = cursor.fetchall()
				for row in rows:
					chat_id = row['chat_id2']

				insert_query = "DELETE FROM `current_dialogs` WHERE chat_id1={0}".format(str(message.chat.id))
				cursor.execute(insert_query)
				connection.commit()

				text1 = 'Собеседник вышел из чата\nТы можешь поставь ему оценку'
				text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

				markup1 = types.InlineKeyboardMarkup()
				button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(message.chat.id))
				button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(message.chat.id))
				markup1.add(button1, button2)
				markup2 = types.InlineKeyboardMarkup()
				button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(message.chat.id))
				button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
				markup2.add(button3)
				markup2.add(button4)
				bot.send_message(chat_id, text1, parse_mode="html", reply_markup=markup1)

				time.sleep(1)

				bot.send_message(chat_id, text2, parse_mode="html", reply_markup=markup2)

				text = 'Ты вышел из чата\nПоставь оценку собеседнику'
				text2 = 'Для отправки жалобы администраторам бота жми кнопку "Пожаловаться"'

				markup1 = types.InlineKeyboardMarkup()
				button1 = types.InlineKeyboardButton("👍 +1", callback_data='ratingup'+str(chat_id))
				button2 = types.InlineKeyboardButton("👎 -1", callback_data='ratingdown'+str(chat_id))
				markup1.add(button1, button2)
				markup2 = types.InlineKeyboardMarkup()
				button3 = types.InlineKeyboardButton("Пожаловаться", callback_data='complain'+str(chat_id))
				button4 = types.InlineKeyboardButton("Начать новый чат", callback_data='awaiting'+'0')
				markup2.add(button3)
				markup2.add(button4)
					
				bot.send_message(message.chat.id, text, parse_mode="html", reply_markup=markup1)

				time.sleep(1)

				bot.send_message(message.chat.id, text2, parse_mode="html", reply_markup=markup2)
				#bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
			connection.close()

	except Exception as ex:
		print("Connection refused...")
		print(ex)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			user_id = call.message.chat.id
			#print(call)
			if call.data[:10] == "vipconfirm":
				num = call.data[10:]
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						insert_query = "INSERT INTO `users_vip` (user_id) VALUES ({0});".format(num)
						cursor.execute(insert_query)
						connection.commit()
						connection.close()
						bot.send_message(call.message.chat.id, "Пользователь добавлен", parse_mode="html")
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			if call.data == "formen":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						insert_query = "UPDATE `users` SET sex = 1 WHERE chat_id = {0};".format(call.message.chat.id)
						cursor.execute(insert_query)
						connection.commit()
						rating = 0
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=temp_text, parse_mode='html',
				#reply_markup=None)
				bot.clear_step_handler_by_chat_id(call.message.chat.id)
				msg = bot.send_message(call.message.chat.id, "Укажи свой возраст")
				bot.register_next_step_handler(msg, need_age)
			elif call.data == "forwomen":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						insert_query = "UPDATE `users` SET sex = 2 WHERE chat_id = {0};".format(call.message.chat.id)
						cursor.execute(insert_query)
						connection.commit()
						rating = 0
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
				bot.clear_step_handler_by_chat_id(call.message.chat.id)
				
				msg = bot.send_message(call.message.chat.id, "Укажи свой возраст")
				bot.register_next_step_handler(msg, need_age)
			elif call.data[:14] == "complaindelete":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				num = call.data[14:]
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:

						insert_query = "DELETE FROM `complains` WHERE id="+num
						cursor.execute(insert_query)
						connection.commit()

						connection.close()

						bot.send_message(call.message.chat.id, "Жалоба удалена",parse_mode="html", reply_markup=None)
						time.sleep(1)
						admin_answer(call.message)
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data == "vipadd":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				msg = bot.send_message(call.message.chat.id, "Нужно переслать в бота любое сообщение от пользователя, которого нужно добавить")
				bot.register_next_step_handler(msg, add_vip_msg)

			elif call.data[:7] == "banuser":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				num = call.data[7:]
				bot.clear_step_handler_by_chat_id(call.message.chat.id)
				msg = bot.send_message(call.message.chat.id, "Укажи причину бана. Она будет отображаться пользователю при попытке найти собеседника")
				bot.register_next_step_handler(msg, add_ban, num)

			elif call.data[:12] == "messageslist":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				num = call.data[12:]
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						select_id = "SELECT def_id FROM `complains` WHERE id="+str(num)
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							def_id = row['def_id']
						select_id = "SELECT plf_id FROM `complains` WHERE id="+str(num)
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							plf_id = row['plf_id']

						select_id = "SELECT timee FROM `complains` WHERE id="+str(num)
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							timee = row['timee']


						select_id = "SELECT msg_id FROM `messages` WHERE id_sender={0} AND id_recipient={1} ORDER BY id".format(def_id,plf_id)
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							msg = row['msg_id']
							bot.copy_message(chat_id=call.message.chat.id, from_chat_id=def_id, message_id=msg)
							#print(str(num))
							time.sleep(1)
						bot.send_message(call.message.chat.id, "<i>...bot...</i><b>Конец сообщений</b>\nЧто делаем дальше?",parse_mode="html", reply_markup=None)
						time.sleep(1)
						markup1 = types.InlineKeyboardMarkup()
						texxt = "Номер жалобы: {0}\nuserID: {1}\nДата обращения: {2}".format(num,def_id,timee)
						button1 = types.InlineKeyboardButton("Жалоба просмотрена, нарушений нет", callback_data='complaindelete'+num)
						button2 = types.InlineKeyboardButton("Заблокировать пользователя", callback_data='banuser'+str(def_id))
						button3 = types.InlineKeyboardButton("Вернуться в список жалоб", callback_data='listcomplains')
						markup1.add(button1)
						markup1.add(button2)
						markup1.add(button3)
						bot.send_message(call.message.chat.id, texxt,parse_mode="html", reply_markup=markup1)
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)	
			elif call.data == "adminpanel":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				admin_answer(call.message)
			elif call.data[:13] == "complaincheck":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				num = call.data[13:]
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						select_id = "SELECT def_id FROM `complains` WHERE id="+str(num)
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							def_id = row['def_id']
						select_id = "SELECT timee FROM `complains` WHERE id="+str(num)
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							timee = row['timee']
						markup1 = types.InlineKeyboardMarkup()
						texxt = "Номер жалобы: {0}\nuserID: {1}\nДата обращения: {2}".format(num,def_id,timee)
						button1 = types.InlineKeyboardButton("Посмотреть все сообщения пользователя", callback_data='messageslist'+str(num))
						button2 = types.InlineKeyboardButton("Назад", callback_data='listcomplains')
						markup1.add(button1, button2)
						bot.send_message(call.message.chat.id, texxt, reply_markup=markup1)
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data == "listcomplains":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				timee = ""
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						cursor.execute("SELECT count(*) FROM `complains`")
						number = cursor.fetchone()
						number = number['count(*)']
						markup1 = types.InlineKeyboardMarkup()
						if number == 0:
							texxt = "Жалоб нет"
							time.sleep(1)
							bot.send_message(call.message.chat.id, texxt)
						else:
							button = []
							cursor.execute("SELECT * FROM `complains`")
							complains = cursor.fetchall()
							for row in complains:
								i = row['id']
								def_id = row['def_id']
								timee = row['timee']
								texxt = "Номер: {0}, userID: {1}, дата: {2}".format(i,def_id,timee)
								butt = types.InlineKeyboardButton(texxt, callback_data='complaincheck'+str(i))
								markup1.add(butt)

						texxt = "ВЕРНУТЬСЯ В АДМИН ПАНЕЛЬ"
						butt = types.InlineKeyboardButton(texxt, callback_data='adminpanel')
						markup1.add(butt)
						bot.send_message(call.message.chat.id, "Выберите: ", reply_markup=markup1)
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data == "stats":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						cursor.execute("SELECT count(*) FROM `users_start`")
						users_start = cursor.fetchone()
						users_start = users_start['count(*)']
						cursor.execute("SELECT count(*) FROM `users`")
						users = cursor.fetchone()
						users = users['count(*)']
						cursor.execute("SELECT count(*) FROM `messages`")
						messages = cursor.fetchone()
						messages = messages['count(*)']
						cursor.execute("SELECT count(*) FROM `complains`")
						complains = cursor.fetchone()
						complains = complains['count(*)']
						txt = "СТАТИСТИКА\nВсего пользователей, которые зашли в бота: {0}\nПользователи прошли регистрацию: {1}\nВсего отправлено сообщений: {2}\nТекущие жалобы: {3}".format(users_start,users,messages,complains)
						bot.send_message(call.message.chat.id, txt)
						time.sleep(1)
						markup1 = types.InlineKeyboardMarkup()
						button1 = types.InlineKeyboardButton("Статистика", callback_data='stats')
						button2 = types.InlineKeyboardButton("Посмотреть жалобы", callback_data='listcomplains')
						button3 = types.InlineKeyboardButton("Добавить пользователя в VIP", callback_data='vipadd')
						markup1.add(button1, button2)
						markup1.add(button3)
						txt =  "Выбери пункт меню:"
						msg = bot.send_message(call.message.chat.id, txt,reply_markup=markup1)
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data == "cancel":
				bot.clear_step_handler_by_chat_id(call.message.chat.id)
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:

						insert_query = "DELETE FROM `awaiting` WHERE chat_id="+str(call.message.chat.id)
						cursor.execute(insert_query)
						connection.commit()
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
				welcome(call.message)
			elif call.data[:8] == "complain":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						insert_query = "INSERT INTO `complains` (plf_id,def_id) VALUES ({0},{1});".format(call.message.chat.id,call.data[8:])
						cursor.execute(insert_query)
						connection.commit()
						bot.send_message(call.message.chat.id, "Жалоба на пользователя отправлена",reply_markup=None)
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data[:8] == "ratingup":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						select_id = "SELECT rating FROM `users` WHERE chat_id="+call.data[8:]
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							rating = row['rating']
						rating = rating + 1
						insert_query = "UPDATE `users` SET rating = {0} WHERE chat_id = {1};".format(str(rating),call.data[8:])
						cursor.execute(insert_query)
						connection.commit()
						connection.close()
						bot.send_message(call.message.chat.id, "Спасибо за оценку",reply_markup=None)
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data[:10] == "ratingdown":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						select_id = "SELECT rating FROM `users` WHERE chat_id="+call.data[10:]
						cursor.execute(select_id)
						rows = cursor.fetchall()
						for row in rows:
							rating = row['rating']
						rating = rating - 1
						insert_query = "UPDATE `users` SET rating = {0} WHERE chat_id = {1};".format(str(rating),call.data[10:])
						cursor.execute(insert_query)
						connection.commit()
						connection.close()
						bot.send_message(call.message.chat.id, "Спасибо за оценку",reply_markup=None)
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data[:8] == "awaiting":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				rating = 0
				age = 0
				sex = 0
				prefer = call.data[8:]
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						select_id = "SELECT user_id FROM `banlist` WHERE user_id="+str(user_id)
						checkban = 0
						checkban = cursor.execute(select_id)
						if checkban != 0:
							select_id = "SELECT reason FROM `banlist` WHERE user_id="+str(user_id)
							cursor.execute(select_id)
							rows = cursor.fetchall()
							for row in rows:
								reason = row['reason']
							txt = "К сожалению, ты был(а) заблокирован(а) администрацией. Причина блокировки: "+reason
							bot.send_message(call.message.chat.id, txt)
							connection.close()
							return
						select_id = "SELECT chat_id FROM users WHERE chat_id="+str(user_id)
						checkUsername = 0
						checkUsername = cursor.execute(select_id)
						if checkUsername != 0:
							print('Пользователь есть')
							select_id = "SELECT rating FROM users WHERE chat_id="+str(user_id)
							cursor.execute(select_id)
							rows = cursor.fetchall()
							for row in rows:
								rating = row['rating']
							select_id = "SELECT age FROM users WHERE chat_id="+str(user_id)
							cursor.execute(select_id)
							rows = cursor.fetchall()
							for row in rows:
								age = row['age']
							if age == 0:
								markup1 = types.InlineKeyboardMarkup()
								button1 = types.InlineKeyboardButton("М", callback_data='formen')
								button2 = types.InlineKeyboardButton("Ж", callback_data='forwomen')
								markup1.add(button1, button2)
								msg = bot.send_message(call.message.chat.id, "Укажи свой пол",reply_markup=markup1)
								bot.clear_step_handler_by_chat_id(call.message.chat.id)
								bot.register_next_step_handler(msg, need_sex)
								connection.close()
								return
							markup1 = types.InlineKeyboardMarkup()
							button1 = types.InlineKeyboardButton("Отменить подбор", callback_data='cancel')
							markup1.add(button1)
							select_id = "SELECT sex FROM users WHERE chat_id="+str(user_id)
							cursor.execute(select_id)
							rows = cursor.fetchall()
							for row in rows:
								sex = row['sex']

							msg = bot.send_message(call.message.chat.id, "<i>...подбор собеседника...</i>",parse_mode="html",reply_markup=markup1)
							insert_query = "INSERT INTO `awaiting` (chat_id,msg_id,sex,prefer_sex) VALUES ({0},{1},{2},{3});".format(user_id,msg.message_id,sex,prefer)
							cursor.execute(insert_query)
							connection.commit()
							bot.clear_step_handler_by_chat_id(call.message.chat.id)
							bot.register_next_step_handler(msg, podbor)
							connection.close()
						else:
							markup1 = types.InlineKeyboardMarkup()
							button1 = types.InlineKeyboardButton("М", callback_data='formen')
							button2 = types.InlineKeyboardButton("Ж", callback_data='forwomen')
							markup1.add(button1, button2)
							msg = bot.send_message(call.message.chat.id, "Укажи свой пол",reply_markup=markup1)
							bot.clear_step_handler_by_chat_id(call.message.chat.id)
							bot.register_next_step_handler(msg, need_sex)
							insert_query = "INSERT INTO `users` (f_name,l_name,chat_id,username) VALUES ('{0.first_name}','{1.last_name}',{2},'{3.username}');".format(call.message.chat,call.message.chat,user_id,call.message.chat)
							cursor.execute(insert_query)
							connection.commit()
							select_id = "SELECT rating FROM users WHERE chat_id="+str(user_id)
							cursor.execute(select_id)
							rows = cursor.fetchall()
							for row in rows:
								rating = row['rating']
							connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data == "data":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				bot.send_message(call.message.chat.id, "Изменение данных",reply_markup=None)
				time.sleep(1)
				rating = 0
				age = 0
				sex = 0
				try:
					connection = connection_mysql()
					with connection.cursor() as cursor:
						markup1 = types.InlineKeyboardMarkup()
						button1 = types.InlineKeyboardButton("М", callback_data='formen')
						button2 = types.InlineKeyboardButton("Ж", callback_data='forwomen')
						markup1.add(button1, button2)
						msg = bot.send_message(call.message.chat.id, "Укажи свой пол",reply_markup=markup1)
						bot.register_next_step_handler(msg, need_sex)
						connection.close()
				except Exception as ex:
					print("Connection refused...")
					print(ex)
			elif call.data == "vip":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				bot.send_message(call.message.chat.id, "Сообщение о покупке VIP",reply_markup=None)
	except Exception as e:
		print(repr(e))



@bot.message_handler(content_types=["photo", "voice", "sticker", "video", "video_note", "audio", "document" ])
def answer_media(message):
	check_chat = False
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			select_id = "SELECT * FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
			#chat_id = 0
			chat = cursor.execute(select_id)
			if chat == 0:
				select_id = "SELECT * FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
				chat = cursor.execute(select_id)
				if chat == 1:
					select_id = "SELECT chat_id1 FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
					rows = cursor.fetchall()
					for row in rows:
						chat_id = row['chat_id1']
					bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
					insert_query = "INSERT INTO `messages` (id_sender, id_recipient , msg_id) VALUES ({0},{1},{2});".format(message.chat.id,chat_id,message.message_id)
					cursor.execute(insert_query)
					connection.commit()
					insert_query = "UPDATE `current_dialogs` SET last_msg2 = 0 WHERE chat_id2 = {0};".format(message.chat.id)
					cursor.execute(insert_query)
					connection.commit()
			elif chat == 1:
				select_id = "SELECT chat_id2 FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
				rows = cursor.fetchall()
				for row in rows:
					chat_id = row['chat_id2']
				bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
				insert_query = "INSERT INTO `messages` (id_sender, id_recipient , msg_id) VALUES ({0},{1},{2});".format(message.chat.id,chat_id,message.message_id)
				cursor.execute(insert_query)
				connection.commit()
				insert_query = "UPDATE `current_dialogs` SET last_msg1 = 0 WHERE chat_id1 = {0};".format(message.chat.id)
				cursor.execute(insert_query)
				connection.commit()
			connection.close()
	except Exception as ex:
		print("Connection refused...")
		print(ex)


@bot.message_handler(content_types=["text"])
def answer_text(message):
	check_chat = False
	try:
		connection = connection_mysql()
		with connection.cursor() as cursor:
			select_id = "SELECT * FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
			#chat_id = 0
			chat = cursor.execute(select_id)
			if chat == 0:
				select_id = "SELECT * FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
				chat = cursor.execute(select_id)
				if chat == 1:
					select_id = "SELECT chat_id1 FROM `current_dialogs` WHERE chat_id2="+str(message.chat.id)
					rows = cursor.fetchall()
					for row in rows:
						chat_id = row['chat_id1']
					bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
					insert_query = "INSERT INTO `messages` (id_sender, id_recipient , msg_id) VALUES ({0},{1},{2});".format(message.chat.id,chat_id,message.message_id)
					cursor.execute(insert_query)
					connection.commit()
					insert_query = "UPDATE `current_dialogs` SET last_msg2 = 0 WHERE chat_id2 = {0};".format(message.chat.id)
					cursor.execute(insert_query)
					connection.commit()
					
			elif chat == 1:
				select_id = "SELECT chat_id2 FROM `current_dialogs` WHERE chat_id1="+str(message.chat.id)
				rows = cursor.fetchall()
				for row in rows:
					chat_id = row['chat_id2']
				bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
				insert_query = "INSERT INTO `messages` (id_sender, id_recipient , msg_id) VALUES ({0},{1},{2});".format(message.chat.id,chat_id,message.message_id)
				cursor.execute(insert_query)
				connection.commit()
				insert_query = "UPDATE `current_dialogs` SET last_msg1 = 0 WHERE chat_id1 = {0};".format(message.chat.id)
				cursor.execute(insert_query)
				connection.commit()
			connection.close()
	except Exception as ex:
		print("Connection refused...")
		print(ex)


if __name__ == '__main__':
	while True:
		start_process()
		try:#добавляем try для бесперебойной работы
			print('start bot')
			try:
				connection = connection_mysql()
				with connection.cursor() as cursor:
					insert_query = "TRUNCATE `awaiting`"
					cursor.execute(insert_query)
					connection.commit()
					insert_query = "TRUNCATE `current_dialogs`"
					cursor.execute(insert_query)
					connection.commit()
					connection.close()
			except Exception as ex:
				print("Connection refused...")
				print(ex)
			bot.polling(none_stop=True)#запуск бота
		except:
			print('restarting bot')
			time.sleep(5)#в случае падения