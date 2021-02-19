#!/usr/bin/env python3

import logging
import os
import praw
import signal
import sys
import time


MESSAGE = """
Fuck Off CoolDownBot Do you not fucking understand that the fucking world is fucking never going to fucking be a perfect fucking happy place? Seriously, some people fucking use fucking foul language, is that really fucking so bad? People fucking use it for emphasis or sometimes fucking to be hateful. It is never fucking going to go away though. This is fucking just how the fucking world, and the fucking internet is. Oh, and your fucking PSA? Don't get me fucking started. Don't you fucking
realize that fucking people can fucking multitask and fucking focus on multiple fucking things? People don't fucking want to focus on the fucking important shit 100% of the fucking time. Sometimes it's nice to just fucking sit back and fucking relax. Try it sometimes, you might fucking enjoy it. I am a fucking bot.
"""

formatter = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(format=formatter, level=logging.INFO)
logger = logging.getLogger('bot')


def signal_handler(signal, frame):
        logger.info('You pressed Ctrl+C! Quitting...')
        sys.exit(0)


class FuckCoolDownBot(object):
    def __init__(self):
        # defined in ~/.config/praw.ini
        self.reddit = praw.Reddit("FuckCoolDownBot2", user_agent = "fCDB2")
        self.target = self.reddit.redditor("CoolDownBot")

    def already_replied(self, comment: praw.models.Comment) -> bool:
        """
        Check if we've already replied to a comment.

        Returns:
            True if already replied, False otherwise
        """
        try:
            comment.refresh()
        except praw.exceptions.ClientException:
            logger.warning("ClientException after comment.refresh()")
            return False

        for reply in comment.replies:
            if reply.author == self.reddit.user.me():
                logger.debug(f"Already replied to {comment.id}")
                return True

        return False

    def reply_to_comment(self, comment: praw.models.Comment):
        """
        Reply to a comment with our message.

        Args:
            comment: comment object to reply to
        """
        comment.reply(MESSAGE)
        logger.info(f"Replied to {comment.id}")

    def run(self):
        """
        Main loop
        """
        ignore = 0
        for comment in self.target.stream.comments():
            if ignore < 99:
                ignore += 1
                continue
            try:

                if comment is None:
                    continue

                if not self.already_replied(comment):
                    self.reply_to_comment(comment)

                time.sleep(5)
            except praw.exceptions.APIException as e:
                    if "DELETED_COMMENT" in str(e):
                        logger.warning("Comment deleted")
                        continue

                    elif "THREAD_LOCKED" in str(e):
                        logger.warning("Thread locked")
                        continue

                    elif "RATELIMIT" in str(e):
                        logger.warning("Ratelimit - Sleeping for 10 minutes")
                        logger.warning(e)
                        time.sleep(610)

                    else:
                        logger.warning("Other API exception occured")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    bot = FuckCoolDownBot()
    bot.run()
