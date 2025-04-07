# PubSub Counter

Google Cloud Pub/Subを使用したメッセージカウンターアプリケーション。受信したメッセージの回数をカウントし、集計結果をリアルタイムで表示します。

## 機能

- Pub/Subメッセージの受信
- メッセージごとの受信回数カウント
- 総受信メッセージ数の表示
- 非同期処理によるメッセージ処理

## 前提条件

- Python 3.9以上
- Google Cloud Platformのアカウント
- Google Cloud Pub/Subが有効化されたプロジェクト

## セットアップ

1. PDMのインストール
```bash
pip install pdm
```

2. リポジトリのクローン
```bash
git clone https://github.com/choimake/pubsub-counter.git
cd pubsub-counter
```

3. 依存関係のインストール
```bash
pdm install
```

4. 環境変数の設定
```bash
cp .env.example .env
```

5. `.env`ファイルを編集し、以下の項目を設定
```
PROJECT_ID=your-project-id
SUBSCRIPTION_ID=your-subscription-id
TOPIC_ID=your-topic-id
```

## 実行方法

1. メッセージカウンターの起動
```bash
pdm run start
```

2. topicにメッセージを送信
```
gcloud pubsub topics publish <topic-id> --message=<any message>
```

3. (Optional）topicにattribute付きのメッセージを送信

```
gcloud pubsub topics publish <topic-id> --message=<any message> \
 --attribute="content-type=application/json" \
```

ex)
```
gcloud pubsub topics publish my-topic \
  --message='{
    "user": {
      "name": "Taro",
      "age": 30
    }
  }' \
  --attribute="content-type=application/json"

```

## 開発環境のセットアップ

開発用ツールのインストール:
```bash
pdm install -G dev
```

これにより以下のツールが利用可能になります:
- pytest: テスト実行
- black: コードフォーマット
- flake8: コード品質チェック

## プロジェクト構成

```
.
├── README.md
├── __pycache__
├── pdm.lock
├── pyproject.toml
├── src
│   └── pubsub_message_counter
│       ├── __init__.py
│       ├── __pycache__
│       └── main.py
└── tests
    ├── __init__.py
    └── __pycache__
```

## 環境変数の説明

| 変数名 | 説明 | 例 |
|--------|------|-----|
| PROJECT_ID | Google CloudのプロジェクトID | my-project-123 |
| SUBSCRIPTION_ID | Pub/Subのサブスクリプション名 | my-subscription |
| TOPIC_ID | Pub/SubのトピックID | my-topic |

## エラー対処

1. 認証エラーの場合
- サービスアカウントキーのパスが正しく設定されているか確認
- サービスアカウントに適切な権限が付与されているか確認

2. トピック/サブスクリプションが見つからない場合
- GCPコンソールでトピックとサブスクリプションが作成されているか確認
- プロジェクトIDが正しいか確認
