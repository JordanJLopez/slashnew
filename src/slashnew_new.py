#!/usr/bin/env python3

'''slashnew_new.py examines the newest posts on reddit and stores information.

The following environment variables must be set:

'''

import praw
import sys
import os
import logging
import slashnew_bot
import pprint
import atexit
import time

import mysql.connector
from mysql.connector import errorcode


class Slashnew_New:

    def __init__(self, subreddit_name=None, db_connect=True):
        if subreddit_name is None:
            self.bot = slashnew_bot.Slashnew_Bot('all')
        else:
            self.bot = slashnew_bot.Slashnew_Bot(subreddit_name)
        if db_connect == True:
            try:
                self.db_conn = mysql.connector.connect(
                    user='slashnew_new',
                    password= os.environ.get('SN_slashnew_new_pw'),
                    host= os.environ.get('SN_slashnew_db'),
                    database='slashnew'
                )
                self.cursor = self.db_conn.cursor()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    logger.error(
                        "USERNAME/PASSWORD INVALID")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    logger.error("DATABASE DOES NOT EXIST")
                else:
                    logger.error(err)
        else:
            self.db_conn = None
        self.last_max_submission_id = -1

    def print_results(self, limit_num):
        submissions = self.bot.get_new_submissions(limit_num)
        delim = ","
        print("post_id,subreddit_id,subreddit_name_prefixed,created_utc,author,fullname,over_18")
        for submission in submissions:
            line = (
                str(submission.id),
                str(submission.subreddit_id),
                str(submission.created_utc),
                str(submission.author),
                str(submission.fullname),
                str(submission.over_18)
            )
            print(delim.join(line))
            pprint.pprint(submission)

    def print_results_csv(self, limit_num, csv_name):
        submissions = self.bot.get_new_submissions(limit_num)
        delim = ","
        f = open(csv_name, 'w')
        f.write("post_id,subreddit_id,created_utc,author,fullname,over_18")
        for submission in submissions:

            line = (
                str(submission.id),
                str(submission.subreddit_id),
                str(submission.created_utc),
                str(submission.author),
                str(submission.fullname),
                str(submission.over_18)
            )
            f.write(delim.join(line))
        f.close()

    def push_results(self, limit_num):
        if(self.db_conn is None):
            logger.error("DB_CONN IS NONE, NOT PUSHING")
            return -1
        sn_new_sql = ("INSERT IGNORE INTO slashnew.sn_new "
                      "(submission_id, subreddit_id, created_utc)"
                      "VALUES (%s, %s, FROM_UNIXTIME(%s))")

        current_max_submission_id = -1
        submissions_pushed = 0
        submissions = self.bot.get_new_submissions(limit_num)
        for submission in submissions:

            if(submission.id <= str(self.last_max_submission_id)):
                print("SUBMISSION.ID < LAST_MAX_SUBREDDIT_ID")
                break
            if(current_max_submission_id == -1):
                current_max_submission_id = submission.id

            submission_id = str(submission.id)
            subreddit_id = str(submission.subreddit_id)[3:] # Trim "t5_"
            created_utc = str(submission.created_utc)
            sn_new_sql_data = (submission_id, subreddit_id, created_utc)

            self.cursor.execute(sn_new_sql, sn_new_sql_data)
            submissions_pushed += 1
        self.last_max_submission_id = max(str(self.last_max_submission_id),
                                          str(current_max_submission_id))
        print("Finished processing, committing DB changes")
        self.db_conn.commit()
        print("DB changes committed, " + str(submissions_pushed) + " pushed")

    def close_connections(self):
        print("CLOSING CONNECTIONS")
        self.cursor.close()
        self.db_conn.close()

if __name__ == '__main__':
    print("STARTING")
    sn_new = Slashnew_New()
    atexit.register(sn_new.close_connections)
    # sn_new.print_results(20)
    while True:
        sn_new.push_results(100)
        time.sleep(2)
    print("FINISHED")

    sys.exit(0)
