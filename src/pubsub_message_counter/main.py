import os
import logging
import signal
import sys
from google.cloud import pubsub_v1
from collections import Counter
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageCounter:
    def __init__(self):
        self.counter = Counter()

    def callback(self, message):
        try:
            data = message.data.decode('utf-8')
            self.counter[data] += 1
            logger.info(f"受信メッセージ: {data}")
            logger.info(f"'{data}'の現在のカウント: {self.counter[data]}")
            logger.info(f"総受信メッセージ数: {sum(self.counter.values())}")
            # message.ack()
            message.nack()
        except Exception as e:
            logger.error(f"メッセージ処理エラー: {e}")
            message.nack()

def run_counter():
    load_dotenv()

    # 環境変数の取得と検証
    project_id = os.getenv("PROJECT_ID")
    subscription_id = os.getenv("SUBSCRIPTION_ID")
    topic_id = os.getenv("TOPIC_ID")

    if not all([project_id, subscription_id, topic_id]):
        raise ValueError("必要な環境変数が設定されていません")

    subscriber = pubsub_v1.SubscriberClient()

    # サブスクリプションの作成
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # メッセージ受信の開始
    counter = MessageCounter()
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=counter.callback
    )

    logger.info(f"メッセージ受信待機中: {subscription_path}")

    try:
        streaming_pull_future.result()
    except Exception as e:
        streaming_pull_future.cancel()
        logger.error(f"エラーが発生しました: {e}")

def signal_handler(signum, frame):
    logger.info("終了シグナルを受信しました。プログラムを終了します。")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        run_counter()
    except KeyboardInterrupt:
        logger.info("プログラムを終了します")
    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
