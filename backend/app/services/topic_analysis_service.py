from typing import Any

from bertopic import BERTopic


def perform_topic_analysis(texts: list[str]) -> dict[str, Any]:
    """BERTopicを使用して、指定されたテキストのトピック分析を実行する"""
    topic_model = BERTopic(
        language="multilingual",
        min_topic_size=5,
    )
    topics, probs = topic_model.fit_transform(texts)
    topic_info_df = topic_model.get_topic_info()
    topic_info = topic_info_df.to_dict(orient="records")

    return {
        "topic_distribution": topics,  # 各ドキュメントに割り当てられたトピックのラベル
        "topic_info": topic_info,  # トピックごとの詳細情報
    }
