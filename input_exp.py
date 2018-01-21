import sqlite3
from contextlib import closing
import config
import argparse
from datetime import datetime
from datetime import timedelta
parser = argparse.ArgumentParser(description='kancolle exp manager.')
parser.add_argument('-d','--day',action='store_true')
parser.add_argument('-m','--month',action='store_true')
parser.add_argument('-e','--exp',type=int)
args = parser.parse_args()

date = '{0:%Y-%m-%d}'.format(datetime.now())
def is_today_data(c):
	sql = 'SELECT COUNT(*) FROM GET_EXP WHERE date = "{}"'.format(date)
	for row in c.execute(sql):
		return True
	return False

def set_exp(c):
	if get_first_month_exp(c) == None:
		sql = 'INSERT INTO MONTHLY_EXP VALUES ( strftime("%Y-%m","{}") , {} )'.format(date,args.exp)
		c.execute(sql)
	if not is_today_data(c):
		sql = 'INSERT INTO GET_EXP VALUES ( "{}" , {} )'.format(date,args.exp)
	else:
		sql = 'UPDATE GET_EXP SET exp = {} WHERE date = "{}"'.format(args.exp,date)
	c.execute(sql)

def get_today_exp(c):
	select_sql = 'SELECT exp FROM GET_EXP WHERE date = "{}"'.format(date)
	for row in c.execute(select_sql):
		return int(row[0])
	return None

def get_yesterday_exp(c):
	yesterday = datetime.now() - timedelta(days=1)
	select_sql = 'SELECT exp FROM GET_EXP WHERE date = "{}"'.format(yesterday)
	for row in c.execute(select_sql):
		print(row)
		return int(row[0])
	return None

def get_first_month_exp(c):
	sql = 'SELECT exp FROM MONTHLY_EXP WHERE month = strftime("%Y-%m","{}")'.format(date)
	for row in c.execute(sql):
		return int(row[0])
	return None

def clac_exp_dayly(c):
	today_exp = get_today_exp(c)
	yesterday_exp = get_yesterday_exp(c)
	today_str = '{0:%Y年%m月%d日}'.format(datetime.now())
	if not yesterday_exp:
		return
	print('{}中に取得した提督経験値は{}です'.format(today_str,today_exp - yesterday_exp))

def clac_exp_monthly(c):
	first_month_exp = get_first_month_exp(c)
	today_exp = get_today_exp(c)

	today_str = '{0:%Y年%m月%d日}'.format(datetime.now())
	month_str = '{0:%Y年%m月}'.format(datetime.now())
	if not first_month_exp:
		return
	print('{0}中に取得した提督経験値は{1}・戦果は{2}です'.format(month_str,today_exp - first_month_exp,(today_exp - first_month_exp)/10000*7))
def main():
	with closing(sqlite3.connect(config.DB_NAME)) as conn:
		c = conn.cursor()
		if args.exp:
			set_exp(c)
			conn.commit()

		if args.day and is_today_data(c):
			clac_exp_dayly(c)

		if args.month and is_today_data(c):
			clac_exp_monthly(c)
main()