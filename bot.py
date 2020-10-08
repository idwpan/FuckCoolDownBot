#!/usr/bin/env python3

import logging
import os
import praw
import signal
import sys
import time

from datetime import datetime
from logging.config import fileConfig


# Replace this if you want
MESSAGE = """
Fuck Off CoolDownBot Do you not fucking understand that the fucking world is fucking never going to fucking be a perfect fucking happy place? Seriously, some people fucking use fucking foul language, is that really fucking so bad? People fucking use it for emphasis or sometimes fucking to be hateful. It is never fucking going to go away though. This is fucking just how the fucking world, and the fucking internet is. Oh, and your fucking PSA? Don't get me fucking started. Don't you fucking realize that fucking people can fucking multitask and fucking focus on multiple fucking things? People don't fucking want to focus on the fucking important shit 100% of the fucking time. Sometimes it's nice to just fucking sit back and fucking relax. Try it sometimes, you might fucking enjoy it. I am a bot
"""

formatter = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(format=formatter, level=logging.INFO)
logger = logging.getLogger('bot')


def signal_handler(signal, frame):
        logger.info('You pressed Ctrl+C! Quitting...')
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    replied = []

    while True:
        try:
            # Replace these values!!!
            reddit = praw.Reddit(client_id="client id",
                                 client_secret="client secret",
                                 username="username",
                                 password="password",
                                 user_agent="user agent")

            CDB = reddit.redditor("CoolDownBot")

            for comment in CDB.comments.new(limit=5):
                try:
                    comment.refresh()

                    for c in comment.replies:
                        if c.author == reddit.user.me():
                            logger.debug(f"Already replied to : {comment.id}")
                            if comment.id not in replied:
                                replied.append(comment.id)
                            continue

                    if comment.id not in replied:
                        replied.append(comment.id)

                        comment.reply(MESSAGE)
                        logger.info(f"Replied to {comment.id}")
                        
                        time.sleep(5)

                except praw.exceptions.ClientException:
                    continue

                except praw.exceptions.APIException as e:
                    if "DELETED_COMMENT" in str(e):
                        logger.warning("Comment deleted")
                        continue

                    elif "THREAD_LOCKED" in str(e):
                        logger.warning("Thread locked")
                        continue

                    elif "RATELIMIT: in str(e)":
                        logger.warning("Ratelimit - Sleeping for 10 minutes")
                        logger.warning(e)
                        time.sleep(610)

                    else:
                        logger.warning("Other API exception occured")

        except Exception as e:
            logger.error(f"Other exception occured: {e}")
            logger.error("Sleeping for 10 seconds and retrying")
            time.sleep(10)
