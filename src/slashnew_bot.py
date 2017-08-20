#!/usr/bin/env python3

'''slashnew_bot.py pulls and returns submissions from a given subreddit

The following environment variables must be set:
SN_client_id : Reddit API client id
SN_client_secret : Reddit API secret
SN_refresh_token : Reddit API refresh token

'''

import praw
import sys
import os
import logging

class Slashnew_Bot:
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name

        self.reddit = praw.Reddit(
            user_agent = 'slashnew (by /u/jordanjlopez)',
            client_id = os.environ.get('SN_client_id'),
            client_secret = os.environ.get('SN_client_secret'),
            refresh_token = os.environ.get('SN_refresh_token')
            )
        self.subreddit = self.reddit.subreddit(self.subreddit_name)

    def get_subreddit_name(self):
        return self.subreddit_name

    def handle_api_exception(api_ex_inst):
        error_type, message, field = api_ex_inst.args
        logging.error("PRAW API ERROR:")
        logging.error("ERROR_TYPE: " + error_type)
        logging.error("MESSAGE: " + message)
        logging.error("FIELD: " + field)
        logging.error("TRACEBACK: " + api_ex_inst.with_traceback())
        return None

    def handle_client_exception(client_ex_inst):
        logging.error("PRAW CLIENT ERROR: ")
        logging.error("TRACEBACK: " + client_ex_inst.with_traceback())
        return -1


    def get_controversial_submissions(self, limit_num):
        try:
            submissions = self.subreddit.controversial(limit = limit_num)
        except praw.exceptions.APIException as api_ex_inst:
            submissions = handle_api_exception(api_ex_inst)
        except praw.exections.ClientException as client_ex_inst:
            submissions = handle_client_exception(client_ex_inst)
        return submissions

    def get_gilded_submissions(self, limit_num):
        try:
            submissions = self.subreddit.gilded(limit = limit_num)
        except praw.exceptions.APIException as api_ex_inst:
            submissions = handle_api_exception(api_ex_inst)
        except praw.exections.ClientException as client_ex_inst:
            submissions = handle_client_exception(client_ex_inst)
        return submissions

    def get_hot_submissions(self, limit_num):
        try:
            submissions = self.subreddit.hot(limit = limit_num)
        except praw.exceptions.APIException as api_ex_inst:
            submissions = handle_api_exception(api_ex_inst)
        except praw.exections.ClientException as client_ex_inst:
            submissions = handle_client_exception(client_ex_inst)
        return submissions

    def get_new_submissions(self, limit_num):
        try:
            submissions = self.subreddit.new(limit = limit_num)
        except praw.exceptions.APIException as api_ex_inst:
            submissions = handle_api_exception(api_ex_inst)
        except praw.exections.ClientException as client_ex_inst:
            submissions = handle_client_exception(client_ex_inst)
        return submissions

    def get_rising_submissions(self, limit_num):
        try:
            submissions = self.subreddit.rising(limit = limit_num)
        except praw.exceptions.APIException as api_ex_inst:
            submissions = handle_api_exception(api_ex_inst)
        except praw.exections.ClientException as client_ex_inst:
            submissions = handle_client_exception(client_ex_inst)
        return submissions

    def get_top_submissions(self, limit_num):
        try:
            submissions = self.subreddit.top(limit = limit_num)
        except praw.exceptions.APIException as api_ex_inst:
            submissions = handle_api_exception(api_ex_inst)
        except praw.exections.ClientException as client_ex_inst:
            submissions = handle_client_exception(client_ex_inst)
        return submissions

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        subreddit_name = 'all'
    else:
        subreddit_name = sys.argv[1]

    bot = Slashnew_Bot(subreddit_name)
    submissions = bot.get_top_submissions(10)
    for submission in submissions:
        print(submission.title + ' ' + str(submission.score))
    sys.exit(0)


